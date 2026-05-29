#!/usr/bin/env node
/**
 * SessionStart hook — inject Content Hub V2 context into the agent's first turn.
 *
 * Adapted from obsidian-mind for Content Hub V2 vault structure.
 * Emits: date, project context excerpt, god nodes, current sprint, recent git changes.
 */

import { readFileSync, appendFileSync, readdirSync, type Dirent } from "node:fs";
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import {
	take,
	formatDateHeader,
	formatRecentChanges,
	isSkippedPath,
} from "./lib/session-start.ts";

const cwd =
	process.env["CLAUDE_PROJECT_DIR"] ??
	process.env["CODEX_PROJECT_DIR"] ??
	process.env["GEMINI_PROJECT_DIR"] ??
	process.cwd();
process.chdir(cwd);

const envFile = process.env["CLAUDE_ENV_FILE"];
if (envFile) {
	try {
		appendFileSync(envFile, `export VAULT_PATH="${cwd}"\n`);
	} catch {
		/* best-effort */
	}
}

type CmdResult =
	| { readonly kind: "ok"; readonly stdout: string }
	| { readonly kind: "missing" }
	| { readonly kind: "failed" };

function runCmd(cmd: string, args: readonly string[], timeoutMs = 5_000): CmdResult {
	const r = spawnSync(cmd, args as string[], { encoding: "utf-8", timeout: timeoutMs });
	if (r.error && (r.error as NodeJS.ErrnoException).code === "ENOENT") return { kind: "missing" };
	if (r.status !== 0) return { kind: "failed" };
	return { kind: "ok", stdout: r.stdout ?? "" };
}

function projectContext(): string {
	try {
		const content = readFileSync(
			"Content-Hub-Vault-V2/00-Management-V2/Memory/context.md",
			{ encoding: "utf-8" },
		);
		return take(content, 40);
	} catch {
		return "(not found — read Content-Hub-Vault-V2/00-Management-V2/Memory/context.md)";
	}
}

function currentSprint(): string {
	try {
		const content = readFileSync(
			"Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md",
			{ encoding: "utf-8" },
		);
		return take(content, 35);
	} catch {
		return "(not found — read Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md)";
	}
}

function godNodes(): string {
	try {
		const report = readFileSync("graphify-out/GRAPH_REPORT.md", { encoding: "utf-8" });
		const match = report.match(/## God Nodes[\s\S]*?(?=\n## )/);
		return match ? match[0].trim() : "(graph report not found)";
	} catch {
		return "(run /graphify --update to rebuild)";
	}
}

function recentChanges(): string {
	const r = runCmd("git", ["log", "--oneline", "--since=48 hours ago", "--no-merges"]);
	if (r.kind !== "ok") return "(no git history)";
	return formatRecentChanges(r.stdout, 15);
}

const SKIP_PREFIXES: readonly string[] = [
	".git",
	".obsidian",
	".claude",
	".agents",
	".hive-mind",
	".swarm",
	".claude-flow",
	"graphify-out",
	"thinking",
	"tmp_marketingskills",
	"notebooklm-py",
	"frontend/node_modules",
	"frontend/.next",
	"backend/.venv",
	"backend/__pycache__",
];

function listMd(): string[] {
	const results: string[] = [];
	function walk(dir: string): void {
		let entries: Dirent[];
		try {
			entries = readdirSync(dir, { withFileTypes: true });
		} catch {
			return;
		}
		for (const e of entries) {
			const full = dir === "." ? e.name : join(dir, e.name);
			if (isSkippedPath(full, SKIP_PREFIXES)) continue;
			if (e.isDirectory()) walk(full);
			else if (e.isFile() && e.name.endsWith(".md")) results.push(`./${full}`);
		}
	}
	walk(".");
	return results.sort();
}

const sections = [
	"## Session Context — Content Hub V2",
	"",
	"### Date",
	formatDateHeader(new Date()),
	"",
	"### Project Context (context.md excerpt)",
	projectContext(),
	"",
	"### God Nodes (high-blast-radius — check before editing)",
	godNodes(),
	"",
	"### Current Sprint",
	currentSprint(),
	"",
	"### Recent Changes (last 48h)",
	recentChanges(),
	"",
	"### Vault Files (read on demand)",
	listMd().join("\n"),
];

process.stdout.write(sections.join("\n") + "\n");
