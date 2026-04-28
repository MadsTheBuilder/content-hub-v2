# Graph Report - remotion-service  (2026-04-20)

## Corpus Check
- Corpus is ~791 words - fits in a single context window. You may not need a graph.

## Summary
- 6 nodes · 4 edges · 4 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Root Composition|Root Composition]]
- [[_COMMUNITY_Duration Compute|Duration Compute]]
- [[_COMMUNITY_Entry Point|Entry Point]]
- [[_COMMUNITY_Hook Body CTA|Hook Body CTA]]

## God Nodes (most connected - your core abstractions)
1. `computeDurationFrames()` - 2 edges
2. `async()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Root Composition"
Cohesion: 1.0
Nodes (0): 

### Community 1 - "Duration Compute"
Cohesion: 1.0
Nodes (2): async(), computeDurationFrames()

### Community 2 - "Entry Point"
Cohesion: 1.0
Nodes (0): 

### Community 3 - "Hook Body CTA"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Root Composition`** (2 nodes): `Root.tsx`, `RemotionRoot()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Duration Compute`** (2 nodes): `async()`, `computeDurationFrames()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Entry Point`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hook Body CTA`** (1 nodes): `HookBodyCTAComposition.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Not enough signal to generate questions. This usually means the corpus has no AMBIGUOUS edges, no bridge nodes, no INFERRED relationships, and all communities are tightly cohesive. Add more files or run with --mode deep to extract richer edges._