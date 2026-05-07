"""
Git operations abstraction layer.

Provides a centralized GitManager class for all git operations needed by the
auto-commit system. Handles staging, committing, and status checking with
proper error handling and .gitignore respect.
"""

import os
from pathlib import Path
from typing import List, Dict
import git
from git.exc import GitCommandError, InvalidGitRepositoryError


class GitManager:
    """
    Abstracts all git operations for the auto-commit system.

    Provides methods to stage files respecting .gitignore patterns, commit
    changes with proper author formatting, and check repository status.
    """

    def __init__(self, repo_path: str = None):
        """
        Initialize GitManager with a repository path.

        Args:
            repo_path: Path to the git repository. Defaults to current working directory.

        Raises:
            ValueError: If the path is not a valid git repository.
        """
        if repo_path is None:
            repo_path = os.getcwd()

        try:
            self.repo = git.Repo(repo_path)
            self.repo_path = Path(repo_path)
        except InvalidGitRepositoryError:
            raise ValueError(f"Not a git repository: {repo_path}")
        except Exception as e:
            raise ValueError(f"Failed to initialize repository at {repo_path}: {str(e)}")

    def stage_files(self, patterns: List[str]) -> List[str]:
        """
        Stage files matching glob patterns, respecting .gitignore rules.

        Args:
            patterns: List of glob patterns (e.g., ['*.py', 'docs/**/*.md'])

        Returns:
            List of staged file paths (relative to repo root)

        Raises:
            ValueError: If git staging fails
        """
        if not patterns:
            return []

        staged_files = []

        try:
            for pattern in patterns:
                # Convert glob pattern to Path matching
                # Handle ** for recursive matching
                if "**" in pattern:
                    # Use rglob for recursive patterns
                    search_pattern = pattern.replace("**", "*")
                    matched = list(self.repo_path.glob(pattern))
                else:
                    matched = list(self.repo_path.glob(pattern))

                # Filter out .gitignored files and stage valid ones
                for file_path in matched:
                    if file_path.is_file():
                        try:
                            # Check if file is ignored
                            rel_path = file_path.relative_to(self.repo_path)

                            # Use git check-ignore to verify it's not ignored
                            try:
                                self.repo.git.check_ignore(str(rel_path))
                                # File is ignored, skip it
                                continue
                            except GitCommandError:
                                # File is not ignored, safe to stage
                                pass

                            # Add to git
                            self.repo.index.add([str(rel_path)])
                            staged_files.append(str(rel_path))
                        except Exception as e:
                            # Log but continue with other files
                            pass

            return staged_files

        except Exception as e:
            raise ValueError(f"Failed to stage files: {str(e)}")

    def commit(self, message: str, author: str = "Claude") -> str:
        """
        Commit staged changes with proper author formatting.

        Args:
            message: Commit message
            author: Author name (will be prefixed with "Claude + " if not already)

        Returns:
            Full commit hash (SHA-1)

        Raises:
            ValueError: If commit fails or no staged changes exist
        """
        try:
            # Check if there are staged changes by comparing index to HEAD
            staged_diffs = self.repo.index.diff("HEAD")
            if not staged_diffs:
                raise ValueError("No staged changes to commit")

            # Format author string
            if author != "Claude" and not author.startswith("Claude"):
                author_str = f"Claude + {author}"
            else:
                author_str = author

            # Create commit with author info
            commit_obj = self.repo.index.commit(
                message,
                author=git.Actor(author_str, "noreply@anthropic.com")
            )

            return commit_obj.hexsha

        except ValueError:
            # Re-raise ValueError as-is
            raise
        except GitCommandError as e:
            raise ValueError(f"Commit failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error during commit: {str(e)}")

    def get_status(self) -> Dict[str, int]:
        """
        Get repository status counts.

        Returns:
            Dictionary with keys 'staged', 'unstaged', 'untracked' containing
            counts of files in each state.
        """
        try:
            staged_count = len(self.repo.index.diff("HEAD"))
            unstaged_count = len(self.repo.index.diff(None))

            # Untracked files
            untracked_count = len(self.repo.untracked_files)

            return {
                "staged": staged_count,
                "unstaged": unstaged_count,
                "untracked": untracked_count
            }
        except Exception as e:
            raise ValueError(f"Failed to get repository status: {str(e)}")

    def get_staged_changes(self) -> List[str]:
        """
        Get list of currently staged file paths.

        Returns:
            List of staged file paths (relative to repo root)
        """
        try:
            staged_items = []
            for (path, stage), entry in self.repo.index.entries.items():
                if stage == 0:  # Normal stage, not merge conflict
                    staged_items.append(path)

            return staged_items
        except Exception as e:
            raise ValueError(f"Failed to get staged changes: {str(e)}")
