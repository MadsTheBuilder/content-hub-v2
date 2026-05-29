"""Skill-specific scorer modules.

Each scorer module exports score_<skill>_output(output: str, **kwargs) -> dict[str, float].
Metrics are returned in tidy-data format for pipeline_results.tsv logging.
"""
