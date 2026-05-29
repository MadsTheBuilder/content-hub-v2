/**
 * Signal definitions for the classify-message hook.
 * Adapted for Content Hub V2 — content creation, skill engine, vault management.
 */

export type Signal = {
	readonly name: string;
	readonly message: string;
	readonly patterns: readonly string[];
};

export const SIGNALS: readonly Signal[] = [
	{
		name: "DECISION",
		message:
			"DECISION detected — write a session log to Content-Hub-Vault-V2/00-Management-V2/Sessions/ and update Current_Sprint.md with [[WikiLinks]] per § 7",
		patterns: [
			"decided",
			"deciding",
			"decision",
			"we chose",
			"agreed to",
			"let's go with",
			"the call is",
			"going with",
			"picked",
			"we're using",
		],
	},
	{
		name: "GOD NODE WARNING",
		message:
			"GOD NODE WARNING — you mentioned a high-degree node. Check graphify-out/GRAPH_REPORT.md blast radius before editing. God nodes: ValidationError (741), AuthTokens (679), NotebookLMClient (644), GenerationStatus (398)",
		patterns: [
			"notebooklm",
			"validationerror",
			"authtokens",
			"generationstatus",
			"notebook client",
			"auth token",
			"clientcore",
			"sourceStatus",
		],
	},
	{
		name: "SKILL BUILD",
		message:
			"SKILL BUILD detected — check .claude/skills/ for existing skill structure. New skills need a SKILL.md. Update Current_Sprint.md when done.",
		patterns: [
			"build a skill",
			"new skill",
			"create a skill",
			"skill file",
			"skill.md",
			"add a skill",
			"update the skill",
			"skill engine",
		],
	},
	{
		name: "SPRINT UPDATE",
		message:
			"SPRINT UPDATE — update Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md and write a session log per § 7 before ending",
		patterns: [
			"sprint",
			"milestone",
			"task complete",
			"task done",
			"finished the",
			"completed the",
			"done with",
			"wrapped up",
			"shipped",
			"launched",
			"deployed",
			"merged",
		],
	},
	{
		name: "ARCHITECTURE",
		message:
			"ARCHITECTURE discussion — record in Content-Hub-Vault-V2/00-Management-V2/Plans/ and link from the session log",
		patterns: [
			"architecture",
			"system design",
			"tech spec",
			"trade-off",
			"design doc",
			"refactor",
			"restructure",
			"migration plan",
			"build plan",
		],
	},
	{
		name: "CONTENT PIPELINE",
		message:
			"CONTENT PIPELINE — check the generation pipeline in backend/content/ and ensure vault notes link to the correct skill nodes",
		patterns: [
			"content pipeline",
			"generation pipeline",
			"youtube pipeline",
			"yt pipeline",
			"short form",
			"voice cleanup",
			"twitter scout",
			"cascade skill",
			"ideation skill",
			"researcher skill",
		],
	},
	{
		name: "GRAPH UPDATE",
		message:
			"GRAPH UPDATE — if files were added or significantly changed, run /graphify --update after the session to keep the graph current",
		patterns: [
			"graphify",
			"graph update",
			"knowledge graph",
			"graph report",
			"run graphify",
			"update the graph",
		],
	},
];
