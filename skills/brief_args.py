"""Brief argument registration helper for all 8 skills.

Provides a single add_brief_args() function that each skill's argparse setup
can call to register optional --tone, --audience, --banned-phrase, --target-length flags.

Usage:
    import argparse
    from skills.brief_args import add_brief_args

    parser = argparse.ArgumentParser()
    parser.add_argument("topic")  # your existing args
    add_brief_args(parser)  # add brief-related optional flags
    args = parser.parse_args()
"""

import argparse


def add_brief_args(parser: argparse.ArgumentParser) -> None:
    """Register optional brief-related flags to an ArgumentParser.

    Adds:
    - --tone: override brief.md tone
    - --audience: override brief.md audience
    - --banned-phrase: repeatable flag for extra banned phrases (extends brief's list)
    - --target-length: override brief.md target_length_minutes

    Args:
        parser: ArgumentParser instance to register flags on.
    """
    parser.add_argument(
        "--tone",
        default=None,
        help="Override tone from brief.md (e.g. 'deadpan, no filler')",
    )
    parser.add_argument(
        "--audience",
        default=None,
        help="Override audience from brief.md (e.g. 'fitness enthusiasts')",
    )
    parser.add_argument(
        "--banned-phrase",
        action="append",
        dest="banned_phrase",
        help="Repeatable flag: extra banned phrases (extends brief.md list)",
    )
    parser.add_argument(
        "--target-length",
        type=int,
        default=None,
        dest="target_length_minutes",
        help="Override target video length in minutes from brief.md",
    )
