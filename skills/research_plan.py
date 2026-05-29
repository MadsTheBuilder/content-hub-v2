"""Question plan with dedup, budget tracking, and adaptive follow-up generation."""

import json
import re
from pathlib import Path

FOLLOWUP_PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "research_followups.md"


class QuestionPlan:
    """Manages a question queue with dedup and budget enforcement.

    Usage (sync, e.g. yt_pipeline.py):
        plan = QuestionPlan(load_questions(), budget=12)
        while (item := plan.next_question()) is not None:
            heading, question = item
            answer = ask(question)
            plan.record(question)
            followups = asyncio.run(generate_followups(heading, question, answer))
            for fh, fq in followups:
                plan.add_followup(fh, fq)

    Usage (async, e.g. researcher.py):
        plan = QuestionPlan(questions, budget=12)
        while (item := plan.next_question()) is not None:
            heading, question = item
            answer = await client.chat.ask(nb_id, question)
            plan.record(question)
            for fh, fq in await generate_followups(heading, question, answer):
                plan.add_followup(fh, fq)
    """

    def __init__(self, questions: list[tuple[str, str]], budget: int = 12):
        self._queue: list[tuple[str, str]] = list(questions)
        self._asked_norms: list[str] = []
        self.budget = budget
        self.turns_used = 0
        self.deduped = 0
        self.followups_added = 0

    @staticmethod
    def _normalize(q: str) -> str:
        q = q.lower().strip()
        q = re.sub(r'[^\w\s]', ' ', q)
        for filler in ('please', 'can you', 'could you', 'tell me', 'what is',
                       'what are', 'list', 'give', 'describe', 'explain', 'identify'):
            q = re.sub(rf'\b{filler}\b', '', q)
        return re.sub(r'\s+', ' ', q).strip()

    def is_duplicate(self, question: str) -> bool:
        norm = self._normalize(question)
        q_words = set(norm.split())
        if not q_words:
            return False
        for prev in self._asked_norms:
            p_words = set(prev.split())
            if not p_words:
                continue
            overlap = len(q_words & p_words) / len(q_words)
            if overlap > 0.6:
                return True
        return False

    def record(self, question: str) -> None:
        self._asked_norms.append(self._normalize(question))
        self.turns_used += 1

    def add_followup(self, heading: str, question: str) -> bool:
        """Queue a follow-up if budget allows. Returns True if queued."""
        if self.budget_remaining > 0 and question.strip():
            self._queue.append((heading, question))
            self.followups_added += 1
            return True
        return False

    @property
    def budget_remaining(self) -> int:
        return self.budget - self.turns_used

    def next_question(self) -> tuple[str, str] | None:
        """Pop the next non-duplicate question within budget, or None."""
        while self._queue and self.budget_remaining > 0:
            heading, question = self._queue.pop(0)
            if self.is_duplicate(question):
                self.deduped += 1
                continue
            return heading, question
        return None

    def stats(self) -> dict:
        return {
            "questions_asked": self.turns_used,
            "questions_deduped": self.deduped,
            "followups_generated": self.followups_added,
            "budget_remaining": self.budget_remaining,
        }


async def generate_followups(
    heading: str, question: str, answer: str
) -> list[tuple[str, str]]:
    """Call AI cascade to extract 0-2 follow-up questions from a Q&A pair.

    Returns list of (heading, question) tuples. Returns [] on any failure.
    """
    try:
        from skills.utils.ai import generate
    except ImportError:
        return []

    try:
        followup_prompt = FOLLOWUP_PROMPT_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        followup_prompt = "Extract follow-up questions from research answers."

    prompt = (
        followup_prompt
        + f"\n\n---\nQuestion: {question}\n\nAnswer:\n{answer[:2000]}\n\n"
        + 'Return 0-2 follow-ups as JSON: [{"heading": "Follow-up: ...", "question": "..."}]\n'
        + "Return [] if no drilling is warranted."
    )

    result = await generate(prompt, cascade=["claude", "nim"])
    if not result["success"] or not result["text"]:
        return []

    text = result["text"].strip()
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if not match:
        return []
    try:
        items = json.loads(match.group(0))
        return [
            (item.get("heading", f"Follow-up: {heading}"), item.get("question", ""))
            for item in items
            if isinstance(item, dict) and item.get("question", "").strip()
        ]
    except (json.JSONDecodeError, TypeError):
        return []
