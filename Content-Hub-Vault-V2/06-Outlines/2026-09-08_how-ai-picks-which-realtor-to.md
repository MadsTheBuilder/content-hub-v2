---
topic: How AI picks which realtor to recommend
platform: yt-long
target_length: 8m
hook_source: Content-Hub-Vault-V2/05-Hooks/2026-09-08_how-ai-picks-which-realtor-to.md
created: 2026-09-08
---
# Outline: How AI picks which realtor to recommend

## [Stage 1: Stimulation] — 0:00–0:30

**Dopamine Goal:** Stimulation

**Hook (verbatim):**

**Spoken Line** (first 3 seconds — stop the scroll):
> "If you want AI to recommend what you built, you need the realtor problem."

**Setup** (next 10 seconds — deepen the curiosity gap):
> "Twelve thousand agents. No public ranking. No official best. The model picks one anyway, confidently, every time. That same call is being made about your product right now, in someone else's chat window."

**Promise** (next 15 seconds — what they get if they keep watching):
> "I traced the full path — retrieval, source weighting, and the one thing that gets a name spoken out loud. By the end you'll know which of those you can move, and which one is why you're getting skipped."

**Visual Cue:**
> Open tight on a chat window mid-generation, cursor blinking. Whip-pan to a node graph of thousands of grey dots. One ignites orange. Hold.

**Text Overlay:**
> WHY IT PICKS THEM, NOT YOU

`[TEXT OVERLAY: WHY IT PICKS THEM, NOT YOU — burned in over the node graph, holds through the whip zoom]`
`[TRANSITION: whip zoom out of the node graph into talking head]`

---

## [Stage 2: Captivation] — 0:30–1:20

**Dopamine Goal:** Captivation

**Talking Points:**
- Search handed you ten results. AI hands you one name. Ten links meant ten businesses got a shot at the click — one name means one does, and the other nine were never in the sentence. That swap already happened. Nobody sent a notice.
- Your stakes, precisely: there is no page two to sit on anymore. You are either the name in the answer or you are the twelve thousand. Middle-of-the-pack used to still get traffic. Now it gets silence.
- Realtors are the clean test case, not the point. No leaderboard, no benchmark, and star ratings that sit at 4.8 across the entire market — so nothing legitimate is available to rank on. Whatever the model is using instead has nowhere to hide here. And whatever's doing the work here is doing it in your category too.
- Close one gap before we go further: the model is not looking anything up in a database of best realtors. That database does not exist. It is assembling a name out of sentences other people wrote. Hold onto that — it's the whole video.

**Visual Notes:**
`[B-ROLL: 2015 search results page, ten blue links, desaturating and collapsing into a 2026 chat answer with one bolded name]`
`[TEXT OVERLAY: 10 RESULTS → 1 NAME]`
`[SHOW SCREEN: live AI answer naming a specific local business, the name highlighted orange as it generates]`

**Transition to Stage 3:**
> "So I went looking for the signal. My first three guesses were all wrong — and the wrong ones are the fastest way to see the right one."

---

## [Stage 3: Anticipation] — 1:20–3:10

**Dopamine Goal:** Anticipation

**Talking Points:**
- **Theory 1 — reviews.** Most reviews, most trust, most recommendations. Obvious, testable, wrong. I pulled review counts for every name the model produced and every name it skipped. The most-recommended agent has a double-digit review count. Agents sitting on four figures never surfaced once. `[SHOW SCREEN: bar chart sorted by review count, the three recommended names flagged orange near the bottom]`
- **Theory 2 — sales volume.** The actual top producers. Here's the part that reframes the whole problem: those numbers live inside MLS portals and brokerage dashboards. Behind a login. The model has never seen a single row of it. Being genuinely the best is stored in a place the model physically cannot read — so it cannot be what's being scored. `[TEXT OVERLAY: BEHIND A LOGIN = INVISIBLE]`
- **Theory 3 — website quality.** One of the three winners has a single-page site: headshot, phone number, nothing else. Agents with full IDX search, weekly blogs, and a video library were never named. So the site isn't the thing being read.
- Now the mechanism, one layer at a time. When you ask, the assistant doesn't answer from memory — it fires a search first. That search returns maybe eight to twelve pages. **Everything it says next comes out of those pages.** Nothing else is in the room.
- Which changes the question entirely. It's not "who's the best agent." It's: which pages get pulled, and what's written on them in a shape the model can reuse.

**Head Fake:**
> Plant it: "Fine — so it's SEO. Rank number one, get retrieved, get recommended. Same game, new interface." That's the obvious landing, and it's what most builders are spending money on right now.
> Subvert it: I checked. The page ranking number one for "best realtor" in my city gets retrieved on almost every run — and the model still does not name the agent sitting at the top of it. Retrieval gets you into the room. It does not get you named. Something happens *after* retrieval that throws most of that page away, and that step is where every one of us is losing.

**Visual Notes:**
`[B-ROLL: whiteboard, three theories listed, two struck through in red, the third crossed out on camera mid-sentence]`
`[SHOW SCREEN: the actual retrieval trace — the search query the model issued, then the raw list of URLs it pulled back, scrolling]`
`[TEXT OVERLAY: RETRIEVED ≠ RECOMMENDED]`

**Transition to Stage 4:**
> "So I stopped looking at rankings and read what was physically on the pages that produced those three names. All three had the same thing on them. Let me show you."

---

## [Stage 4: Validation] — 3:10–6:00

**Dopamine Goal:** Validation

**Talking Points:**

- **The test, on camera, so you can see it isn't cherry-picked.** Forty prompts. Four different phrasings, ten runs each, fresh session every time, no memory, no personalization. Three names carry the entire set. Watch the counter — by run twelve you can already predict it. `[SHOW SCREEN: prompt grid executing live, names tallying in a running counter beside it]`

- **What the three share — the describable sentence.** Each one has a short, specific, repeatable claim sitting next to their name in plain text. Not "top-rated" or "award-winning." Something like: *"works almost exclusively with first-time buyers in the older neighborhoods."* That's a **category plus a qualifier**. The model can lift that clause whole, attach it to a name, and hand it to you as a reason it picked them. The sentence is the unit being selected. The person is just what's attached to it. `[TEXT OVERLAY: NAME + CATEGORY + QUALIFIER]`

- **Source weighting — where that sentence has to live.** The same claim, in roughly the same words, appears across four or more *independent* places: a local news quote, two roundup listicles, a Reddit thread, a podcast transcript. Notice what's not on that list — their own website. Self-description is the weakest input in the pile, because every agent's site says they're the best and the model has learned to discount all of it equally. Third-party repetition is what promotes a claim from "words someone typed" to "thing that is true." `[SHOW SCREEN: four browser tabs side by side, the same descriptor phrase highlighted orange in each, then the agent's own site greyed out]`

- **The last gate — why a name gets spoken out loud at all.** Models hedge on naming a specific person. "Consult a licensed agent in your area" is the safe default, and it is the default for a reason. That hedge lifts only when multiple independent sources agree, because agreement makes the answer cheap to state and hard to be wrong about. **Consensus isn't how it ranks you. Consensus is what unlocks its mouth.** One excellent source gets you a hedge. Four mediocre ones saying the same thing get you named. `[TEXT OVERLAY: CONSENSUS = PERMISSION TO SAY IT]`

- **Now run the same three layers on a category you actually care about.** Same forty-prompt test, "best [your category] tool." Identical result shape. The named tools are not the best-funded and not the best-built — I checked both. They're the ones with one crisp sentence repeated across sources that don't belong to them. `[SHOW SCREEN: the identical grid test on a dev-tool category, three names dominating the tally]`

**Head Fake (second):**
> Plant it: "Okay, so I need more content. More posts, more pages, more surface area, more chances to get retrieved." Every marketing dashboard on earth is pushing you toward this.
> Subvert it: volume is the wrong axis, and it can actively hurt. I found agents with sixty blog posts who were never named once — because all sixty describe them differently. Luxury specialist on one page, family-focused on the next, investor expert on the third. Sixty descriptions is sixty weak, competing signals. **One sentence in six places beats six sentences in sixty places.** The model is hunting for agreement, and you can only agree with yourself if you say the same thing twice.

**Visual Notes:**
`[B-ROLL: two node graphs side by side — left, one node with sixty thin scattered edges going nowhere, staying grey; right, one node with six thick converging edges, igniting orange on contact]`

**Transition to Stage 5:**
> "I want to be honest about how long this took me to see, because I had it backwards in a way that cost me two years."

---

## [Stage 5: Affection] — 6:00–7:00

**Dopamine Goal:** Affection

**Talking Points:**
- I ran this exact test on my own tool before I ever ran it on realtors. Zero for forty. Not hedged, not mentioned in passing — absent. And my documentation is genuinely good: clean, thorough, current, better than most things in my category. That's precisely why it failed. My docs describe **what it does**. Feature lists, parameters, examples. There is not one sentence in there that a model could hand to a stranger as a reason to choose it.
- The part that actually stung: two people had written about the tool publicly, unprompted, and described it two completely different ways. I'd been reading that as free marketing and screenshotting it for myself. It was noise. I handed the model two conflicting stories about the same thing and it did the sensible thing — it stayed quiet.
- What I'd do differently, in order: write the sentence *first*. Before the docs, before the landing page, before the launch post. Decide the exact claim, say it identically in every place, and hand it verbatim to anyone who writes about you. I spent two years making the thing better and zero days making it describable, and only one of those two shows up in an answer.
- I don't love this and I'm not going to pretend I do. "Most describable wins" is not the meritocracy anybody was promised. But it's the system that's actually running, and refusing to play it isn't principle — it's just choosing to be invisible and calling it integrity.

**Visual Notes:**
`[TEXT OVERLAY: 0 / 40]`
`[SHOW SCREEN: two-second flash of the two conflicting third-party descriptions, side by side, contradicting phrases underlined]`
Talking head, tighter frame, no cuts through the last two points.

**Transition to Stage 6:**
> "And once I stopped arguing with it, I noticed something about those three winners that I had walked straight past four times."

---

## [Stage 6: Revelation] — 7:00–8:05

**Dopamine Goal:** Revelation

**Talking Points:**
- The three names aren't beating the other twelve thousand agents. They're not on the same axis as them. Each one **owns a phrase** — first-time buyers, historic properties, investor portfolios. They never won the "best realtor" question. They quietly split it into three narrower questions and took one each. The model isn't crowning a winner from a field. It's matching a query to whoever wrote the vocabulary that query is made of.
- That inverts the strategy completely. You are not climbing a ranking, because there is no ranking to climb. **You are supplying language.** Whoever writes a category's vocabulary becomes the default answer to every question phrased in it — not because they're preferred, but because the model has no other words available to think about it with.
- Beyond realtors, beyond your product: this is the first distribution layer in decades where the winning move is naming something precisely instead of being loudest about something broad. Budget buys reach. Budget cannot buy four independent sources agreeing on your sentence. That's a real opening for small builders, and it closes the moment enough people notice it.
- The uncomfortable version, and then I'll let you go: if you can't say in one sentence who your thing is for and what it's for, that isn't a marketing gap you'll fix later. The model is reading it as a fact about you. And it's right.

**Visual Notes:**
`[B-ROLL: the twelve-thousand-dot node graph from the hook returns — one broad question node fractures into three narrow ones, a single orange node locking onto each]`
`[TEXT OVERLAY: YOU'RE NOT RANKING. YOU'RE SUPPLYING LANGUAGE.]`

---

## [CTA] — 8:05–8:35

**Goal:** Give viewers a specific reason to watch the next video.

**Talking Points:**
- You now know what the model is scoring. You don't know what it currently says about *you* — and almost everyone guesses wrong in the direction that hurts. Next video I run the forty-prompt audit on a real product, live, and separate the three failure modes: never retrieved, retrieved but hedged, and named but described wrong. Different cause, different fix, and they look identical from the outside.
- Skip it and here's what happens: you go write the sentence, ship it, wait six weeks, and nothing changes — because the layer blocking you was the one you didn't touch.

**Visual Notes:**
`[TEXT OVERLAY: NEXT — THE 40-PROMPT AUDIT]`
`[SHOW SCREEN: two-second flash of the audit spreadsheet, the three failure columns visible]` · `[end screen graphic]`
