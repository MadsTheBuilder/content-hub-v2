"""twitter_scheduler — Run twitter_scout on a randomised 40-50 minute interval.

Usage:
    python scripts/twitter_scheduler.py
"""
import logging
import random
import sys
import time
from pathlib import Path

# Insert project root so imports work regardless of working directory.
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.twitter_scout import run_scout  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Twitter scheduler started. Running every 40-50 minutes.")
    while True:
        try:
            run_scout()
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user.")
            sys.exit(0)
        except Exception as exc:
            logger.error("run_scout() failed: %s", exc, exc_info=True)

        delay = random.randint(2400, 3000)
        logger.info("Sleeping %d seconds (%.1f min)...", delay, delay / 60)
        time.sleep(delay)
