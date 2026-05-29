"""prompt_lab — Autonomous prompt optimization framework.

Implements the autoresearch loop: modify → score → keep-or-revert → repeat.
Scorers evaluate skill outputs and return metrics for the loop to consume.
"""
