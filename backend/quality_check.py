"""Quality validation module for running tests, linting, and type checks.

Runs pytest, ruff, and mypy to ensure code quality gates pass before commits.
"""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# Import config validation (adjust path if needed)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from sync_vault import validate_config
except ImportError:
    validate_config = None


class QualityValidator:
    """Runs tests, linting, and type checks; reports structured results.

    Attributes:
        repo_path (str): Root path of the repository.
        log_dir (Path): Directory for quality check logs.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """Initialize QualityValidator with optional repo path.

        Args:
            repo_path: Root directory of the repository (defaults to current dir).
        """
        self.repo_path = repo_path
        self.log_dir = Path(repo_path) / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "quality_check.log"

    def run_checks(self, verbose: bool = False) -> dict[str, Any]:
        """Run all quality checks and return structured results.

        Executes pytest, ruff, and mypy. Returns a dict with pass/fail status
        and detailed error counts and output snippets.

        Args:
            verbose: If True, print full output to stdout; else log to file.

        Returns:
            Dictionary with keys:
                - all_passed (bool): True if all checks pass
                - tests_passed (bool): True if pytest exits with code 0
                - test_count (int): Number of tests run
                - lint_errors (int): Count of ruff errors
                - type_errors (int): Count of mypy errors
                - details (dict): Contains pytest_output, ruff_output, mypy_output
        """
        # Setup logging
        if verbose:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(self.log_file)

        logger = logging.getLogger("quality_check")
        logger.setLevel(logging.INFO)
        if logger.handlers:
            logger.handlers.clear()
        logger.addHandler(handler)

        results: dict[str, Any] = {
            "all_passed": False,
            "tests_passed": False,
            "test_count": 0,
            "lint_errors": 0,
            "type_errors": 0,
            "details": {
                "pytest_output": "",
                "ruff_output": "",
                "mypy_output": "",
                "config_issues": {},
            },
        }

        # Run pytest
        pytest_output, test_count, tests_passed = self._run_pytest(logger)
        results["pytest_output"] = pytest_output
        results["tests_passed"] = tests_passed
        results["test_count"] = test_count
        results["details"]["pytest_output"] = pytest_output[:500]

        # Run ruff
        ruff_output, lint_errors = self._run_ruff(logger)
        results["lint_errors"] = lint_errors
        results["details"]["ruff_output"] = ruff_output[:500]

        # Run mypy
        mypy_output, type_errors = self._run_mypy(logger)
        results["type_errors"] = type_errors
        results["details"]["mypy_output"] = mypy_output[:500]

        # Validate configuration
        if validate_config:
            config_validation = validate_config()
            if not config_validation["config_valid"]:
                results["details"]["config_issues"] = {
                    "missing_keys": config_validation["missing_keys"],
                    "extra_keys": config_validation["extra_keys"],
                    "issues": config_validation["issues"],
                }
                logger.warning(
                    f"Config validation failed: {len(config_validation['issues'])} issues"
                )
                for issue in config_validation["issues"]:
                    logger.warning(f"  {issue}")
            else:
                logger.info("Config validation passed")

        # Determine overall pass/fail
        results["all_passed"] = (
            tests_passed and lint_errors == 0 and type_errors == 0
        )

        logger.info(
            f"Quality check complete: "
            f"all_passed={results['all_passed']}, "
            f"tests_passed={tests_passed}, "
            f"lint_errors={lint_errors}, "
            f"type_errors={type_errors}"
        )

        return results

    def _run_pytest(self, logger: logging.Logger) -> tuple[str, int, bool]:
        """Run pytest and return output, test count, and pass status.

        Args:
            logger: Logger instance for output.

        Returns:
            Tuple of (output_string, test_count, passed_bool).
        """
        backend_tests = os.path.join(self.repo_path, "backend", "tests")
        cmd = ["pytest", backend_tests, "--tb=short", "-v"]

        logger.info(f"Running pytest: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = result.stdout + result.stderr
            passed = result.returncode == 0

            # Count tests from output
            test_count = output.count(" PASSED") + output.count(" FAILED")

            logger.info(f"pytest exit code: {result.returncode} ({test_count} tests)")
            return output, test_count, passed
        except subprocess.TimeoutExpired:
            logger.error("pytest timeout (60s)")
            return "pytest timeout", 0, False
        except FileNotFoundError:
            logger.error("pytest not found - install pytest")
            return "pytest not found", 0, False
        except Exception as e:
            logger.error(f"pytest error: {e}")
            return str(e), 0, False

    def _run_ruff(self, logger: logging.Logger) -> tuple[str, int]:
        """Run ruff linter and return output and error count.

        Args:
            logger: Logger instance for output.

        Returns:
            Tuple of (output_string, error_count).
        """
        backend_dir = os.path.join(self.repo_path, "backend")
        cmd = ["ruff", "check", backend_dir]

        logger.info(f"Running ruff: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout + result.stderr

            # Count error lines (each error is a line with format: file:line:col: error)
            error_count = len([l for l in output.split("\n") if ":" in l and l.strip()])

            logger.info(f"ruff found {error_count} issues")
            return output, error_count
        except subprocess.TimeoutExpired:
            logger.error("ruff timeout (30s)")
            return "ruff timeout", 1
        except FileNotFoundError:
            logger.error("ruff not found - install ruff")
            return "ruff not found", 1
        except Exception as e:
            logger.error(f"ruff error: {e}")
            return str(e), 1

    def _run_mypy(self, logger: logging.Logger) -> tuple[str, int]:
        """Run mypy type checker and return output and error count.

        Args:
            logger: Logger instance for output.

        Returns:
            Tuple of (output_string, error_count).
        """
        backend_dir = os.path.join(self.repo_path, "backend")
        cmd = ["mypy", backend_dir, "--ignore-missing-imports"]

        logger.info(f"Running mypy: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = result.stdout + result.stderr

            # Count error lines (mypy output format: file:line: error)
            error_count = len([l for l in output.split("\n") if " error: " in l])

            logger.info(f"mypy found {error_count} errors")
            return output, error_count
        except subprocess.TimeoutExpired:
            logger.error("mypy timeout (60s)")
            return "mypy timeout", 1
        except FileNotFoundError:
            logger.error("mypy not found - install mypy")
            return "mypy not found", 1
        except Exception as e:
            logger.error(f"mypy error: {e}")
            return str(e), 1
