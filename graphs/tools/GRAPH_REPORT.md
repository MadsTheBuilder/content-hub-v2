# Graph Report - tools  (2026-04-20)

## Corpus Check
- Corpus is ~306 words - fits in a single context window. You may not need a graph.

## Summary
- 7 nodes · 7 edges · 3 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Task Routing|Task Routing]]
- [[_COMMUNITY_Haiku Delegation|Haiku Delegation]]
- [[_COMMUNITY_Advisor Execution|Advisor Execution]]

## God Nodes (most connected - your core abstractions)
1. `run_haiku_delegate()` - 3 edges
2. `execute_task_with_advisor()` - 3 edges
3. `route_task()` - 2 edges
4. `Uses Haiku to classify task complexity.` - 1 edges
5. `Sub-agent worker function invoked by Sonnet.` - 1 edges
6. `Runs the main tier with the Advisor beta tool.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `execute_task_with_advisor()` --calls--> `run_haiku_delegate()`  [EXTRACTED]
  tools\orchestrator.py → tools\orchestrator.py  _Bridges community 1 → community 2_

## Communities

### Community 0 - "Task Routing"
Cohesion: 0.67
Nodes (2): Uses Haiku to classify task complexity., route_task()

### Community 1 - "Haiku Delegation"
Cohesion: 1.0
Nodes (2): Sub-agent worker function invoked by Sonnet., run_haiku_delegate()

### Community 2 - "Advisor Execution"
Cohesion: 1.0
Nodes (2): execute_task_with_advisor(), Runs the main tier with the Advisor beta tool.

## Knowledge Gaps
- **3 isolated node(s):** `Uses Haiku to classify task complexity.`, `Sub-agent worker function invoked by Sonnet.`, `Runs the main tier with the Advisor beta tool.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Haiku Delegation`** (2 nodes): `Sub-agent worker function invoked by Sonnet.`, `run_haiku_delegate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Advisor Execution`** (2 nodes): `execute_task_with_advisor()`, `Runs the main tier with the Advisor beta tool.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_haiku_delegate()` connect `Haiku Delegation` to `Task Routing`, `Advisor Execution`?**
  _High betweenness centrality (0.333) - this node is a cross-community bridge._
- **Why does `execute_task_with_advisor()` connect `Advisor Execution` to `Task Routing`, `Haiku Delegation`?**
  _High betweenness centrality (0.333) - this node is a cross-community bridge._
- **What connects `Uses Haiku to classify task complexity.`, `Sub-agent worker function invoked by Sonnet.`, `Runs the main tier with the Advisor beta tool.` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._