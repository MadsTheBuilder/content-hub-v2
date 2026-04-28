"""Integration tests for the scheduled general_trending job.

Tests the end-to-end flow:
- job_general_trending() loops over platforms
- scrape_general_trending() is called per platform
- Results are inserted into trending_content table
- Errors on one platform don't stop others (resilience)
"""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from backend.scheduler.jobs import job_general_trending


class TestGeneralTrendingJob:
    """Happy path: all platforms succeed, data inserted to trending_content."""

    @pytest.mark.asyncio
    async def test_happy_path_all_platforms_succeed(self, mock_supabase):
        """
        Mock scrape_general_trending to return 2 rows per platform.
        Assert job calls scrape_general_trending 3 times (tiktok, instagram, youtube).
        Assert trending_content table received 3 insert calls (one per platform).
        """
        # Mock data — 2 items per platform
        mock_results_tiktok = [
            {
                "workflow_id": None,
                "platform": "tiktok",
                "post_url": "https://tiktok.com/viral1",
                "author_username": "creator1",
                "author_followers": 100000,
                "title": "Trending on TikTok #1",
                "description": "This is trending",
                "hashtags": ["trending"],
                "view_count": 500000,
                "like_count": 50000,
                "comment_count": 5000,
                "share_count": 2000,
                "save_count": 1000,
                "organic_score": 250000.0,
                "content_age_days": 1,
                "thumbnail_url": "https://example.com/thumb1.jpg",
            },
            {
                "workflow_id": None,
                "platform": "tiktok",
                "post_url": "https://tiktok.com/viral2",
                "author_username": "creator2",
                "author_followers": 80000,
                "title": "Trending on TikTok #2",
                "description": "Also trending",
                "hashtags": ["viral"],
                "view_count": 400000,
                "like_count": 40000,
                "comment_count": 4000,
                "share_count": 1500,
                "save_count": 800,
                "organic_score": 200000.0,
                "content_age_days": 2,
                "thumbnail_url": "https://example.com/thumb2.jpg",
            },
        ]

        mock_results_instagram = [
            {
                "workflow_id": None,
                "platform": "instagram",
                "post_url": "https://instagram.com/p/abc123",
                "author_username": "instacreator1",
                "author_followers": 200000,
                "title": "Instagram trending post",
                "description": "Amazing reels content",
                "hashtags": ["trending", "reels"],
                "view_count": 300000,
                "like_count": 30000,
                "comment_count": 2000,
                "share_count": 1000,
                "save_count": 5000,
                "organic_score": 180000.0,
                "content_age_days": 1,
                "thumbnail_url": "https://example.com/thumb3.jpg",
            },
            {
                "workflow_id": None,
                "platform": "instagram",
                "post_url": "https://instagram.com/p/def456",
                "author_username": "instacreator2",
                "author_followers": 150000,
                "title": "Instagram trending post #2",
                "description": "More reels",
                "hashtags": ["viral"],
                "view_count": 250000,
                "like_count": 25000,
                "comment_count": 1500,
                "share_count": 800,
                "save_count": 4000,
                "organic_score": 150000.0,
                "content_age_days": 2,
                "thumbnail_url": "https://example.com/thumb4.jpg",
            },
        ]

        mock_results_youtube = [
            {
                "workflow_id": None,
                "platform": "youtube",
                "post_url": "https://youtube.com/watch?v=abc123",
                "author_username": "YouTubeCreator1",
                "author_followers": 500000,
                "title": "Trending on YouTube",
                "description": "Check out this trending video",
                "hashtags": ["trending"],
                "view_count": 1000000,
                "like_count": 50000,
                "comment_count": 10000,
                "share_count": 5000,
                "save_count": 0,
                "organic_score": 450000.0,
                "content_age_days": 1,
                "thumbnail_url": "https://img.youtube.com/vi/abc123/hq.jpg",
            },
            {
                "workflow_id": None,
                "platform": "youtube",
                "post_url": "https://youtube.com/watch?v=def456",
                "author_username": "YouTubeCreator2",
                "author_followers": 300000,
                "title": "YouTube trending #2",
                "description": "Another trending video",
                "hashtags": ["viral"],
                "view_count": 800000,
                "like_count": 40000,
                "comment_count": 8000,
                "share_count": 4000,
                "save_count": 0,
                "organic_score": 350000.0,
                "content_age_days": 2,
                "thumbnail_url": "https://img.youtube.com/vi/def456/hq.jpg",
            },
        ]

        # Map platforms to their mock results
        mock_return_map = {
            "tiktok": mock_results_tiktok,
            "instagram": mock_results_instagram,
            "youtube": mock_results_youtube,
        }

        # Patch scrape_general_trending at the module where it's imported (jobs.py)
        with patch(
            "backend.scheduler.jobs.scrape_general_trending",
            new_callable=AsyncMock,
        ) as mock_scrape:
            # Configure mock to return appropriate data per platform
            mock_scrape.side_effect = lambda platform: mock_return_map[platform]

            # Track insert calls on the mock Supabase client
            original_insert = mock_supabase.table("trending_content").insert
            insert_calls = []

            def track_insert(data):
                insert_calls.append(data)
                # Return a mock query builder that has execute()
                builder = original_insert.__self__.__class__(
                    "trending_content"
                )
                builder._op = "insert"
                builder._insert_data = data
                return builder

            # Monkeypatch the table method to track insert calls
            original_table = mock_supabase.table

            def patched_table(name):
                result = original_table(name)
                if name == "trending_content":
                    result.insert = lambda data: track_insert(data)
                return result

            mock_supabase.table = patched_table

            # Execute the job
            await job_general_trending()

            # Verify scrape_general_trending was called 3 times
            assert mock_scrape.call_count == 3
            assert mock_scrape.call_args_list[0][0][0] == "tiktok"
            assert mock_scrape.call_args_list[1][0][0] == "instagram"
            assert mock_scrape.call_args_list[2][0][0] == "youtube"

            # Verify insert was called 3 times (once per platform)
            assert len(insert_calls) == 3
            # Verify each insert received the correct data
            assert insert_calls[0] == mock_results_tiktok
            assert insert_calls[1] == mock_results_instagram
            assert insert_calls[2] == mock_results_youtube

    @pytest.mark.asyncio
    async def test_happy_path_no_results_from_platform(self, mock_supabase):
        """
        Scrape returns empty list for one platform (no error).
        Job should skip insert for that platform, continue to others.
        """
        mock_return_map = {
            "tiktok": [],  # Empty — no insert call
            "instagram": [
                {
                    "workflow_id": None,
                    "platform": "instagram",
                    "post_url": "https://instagram.com/p/xyz",
                    "author_username": "creator",
                    "author_followers": 10000,
                    "title": "Test",
                    "description": "Test",
                    "hashtags": [],
                    "view_count": 1000,
                    "like_count": 100,
                    "comment_count": 10,
                    "share_count": 5,
                    "save_count": 2,
                    "organic_score": 500.0,
                    "content_age_days": 1,
                    "thumbnail_url": "",
                }
            ],
            "youtube": [],  # Empty — no insert call
        }

        with patch(
            "backend.scheduler.jobs.scrape_general_trending",
            new_callable=AsyncMock,
        ) as mock_scrape:
            mock_scrape.side_effect = lambda platform: mock_return_map[platform]

            insert_calls = []

            original_table = mock_supabase.table

            def patched_table(name):
                result = original_table(name)
                if name == "trending_content":
                    original_insert = result.insert

                    def track_insert(data):
                        insert_calls.append(data)
                        builder = original_insert.__self__.__class__(
                            "trending_content"
                        )
                        builder._op = "insert"
                        builder._insert_data = data
                        return builder

                    result.insert = track_insert
                return result

            mock_supabase.table = patched_table

            await job_general_trending()

            # 3 scrape calls, but only 1 insert (for instagram)
            assert mock_scrape.call_count == 3
            assert len(insert_calls) == 1
            assert insert_calls[0][0]["platform"] == "instagram"

    @pytest.mark.asyncio
    async def test_resilience_one_platform_fails(self, mock_supabase, caplog):
        """
        One platform raises an exception during scrape.
        Job logs error and continues with remaining platforms.
        Remaining platforms still insert their data.
        """
        error_msg = "Apify service temporarily unavailable"

        mock_return_map = {
            "tiktok": [
                {
                    "workflow_id": None,
                    "platform": "tiktok",
                    "post_url": "https://tiktok.com/ok",
                    "author_username": "creator_ok",
                    "author_followers": 5000,
                    "title": "TikTok OK",
                    "description": "This worked",
                    "hashtags": [],
                    "view_count": 10000,
                    "like_count": 500,
                    "comment_count": 50,
                    "share_count": 20,
                    "save_count": 10,
                    "organic_score": 5000.0,
                    "content_age_days": 1,
                    "thumbnail_url": "",
                }
            ],
            "instagram": Exception(error_msg),  # Will raise
            "youtube": [
                {
                    "workflow_id": None,
                    "platform": "youtube",
                    "post_url": "https://youtube.com/ok",
                    "author_username": "youtube_ok",
                    "author_followers": 50000,
                    "title": "YouTube OK",
                    "description": "This also worked",
                    "hashtags": [],
                    "view_count": 100000,
                    "like_count": 5000,
                    "comment_count": 500,
                    "share_count": 200,
                    "save_count": 0,
                    "organic_score": 45000.0,
                    "content_age_days": 1,
                    "thumbnail_url": "",
                }
            ],
        }

        def side_effect_fn(platform):
            result = mock_return_map[platform]
            if isinstance(result, Exception):
                raise result
            return result

        with patch(
            "backend.scheduler.jobs.scrape_general_trending",
            new_callable=AsyncMock,
        ) as mock_scrape:
            mock_scrape.side_effect = side_effect_fn

            insert_calls = []

            original_table = mock_supabase.table

            def patched_table(name):
                result = original_table(name)
                if name == "trending_content":
                    original_insert = result.insert

                    def track_insert(data):
                        insert_calls.append(data)
                        builder = original_insert.__self__.__class__(
                            "trending_content"
                        )
                        builder._op = "insert"
                        builder._insert_data = data
                        return builder

                    result.insert = track_insert
                return result

            mock_supabase.table = patched_table

            import logging

            caplog.set_level(logging.ERROR)

            await job_general_trending()

            # 3 scrape calls attempted
            assert mock_scrape.call_count == 3

            # Only 2 inserts (tiktok and youtube — instagram failed)
            assert len(insert_calls) == 2
            platforms_inserted = [call[0]["platform"] for call in insert_calls]
            assert "tiktok" in platforms_inserted
            assert "youtube" in platforms_inserted
            assert "instagram" not in platforms_inserted

            # Error should be logged
            assert "General trending scrape failed for instagram" in caplog.text
            assert error_msg in caplog.text

    @pytest.mark.asyncio
    async def test_multiple_platforms_fail_job_continues(
        self, mock_supabase, caplog
    ):
        """
        Multiple platforms fail; job continues and inserts from successful ones.
        Verifies job doesn't crash on cascading errors.
        """

        def side_effect_fn(platform):
            if platform == "instagram":
                raise RuntimeError("Instagram API down")
            elif platform == "youtube":
                raise RuntimeError("YouTube quota exceeded")
            else:
                return [
                    {
                        "workflow_id": None,
                        "platform": "tiktok",
                        "post_url": "https://tiktok.com/ok",
                        "author_username": "creator",
                        "author_followers": 5000,
                        "title": "TikTok",
                        "description": "Works",
                        "hashtags": [],
                        "view_count": 10000,
                        "like_count": 500,
                        "comment_count": 50,
                        "share_count": 20,
                        "save_count": 10,
                        "organic_score": 5000.0,
                        "content_age_days": 1,
                        "thumbnail_url": "",
                    }
                ]

        with patch(
            "backend.scheduler.jobs.scrape_general_trending",
            new_callable=AsyncMock,
        ) as mock_scrape:
            mock_scrape.side_effect = side_effect_fn

            insert_calls = []

            original_table = mock_supabase.table

            def patched_table(name):
                result = original_table(name)
                if name == "trending_content":
                    original_insert = result.insert

                    def track_insert(data):
                        insert_calls.append(data)
                        builder = original_insert.__self__.__class__(
                            "trending_content"
                        )
                        builder._op = "insert"
                        builder._insert_data = data
                        return builder

                    result.insert = track_insert
                return result

            mock_supabase.table = patched_table

            import logging

            caplog.set_level(logging.ERROR)

            # Should not raise
            await job_general_trending()

            # Only tiktok inserted
            assert len(insert_calls) == 1
            assert insert_calls[0][0]["platform"] == "tiktok"

            # Both errors logged
            assert "Instagram" in caplog.text or "instagram" in caplog.text
            assert "YouTube" in caplog.text or "youtube" in caplog.text
