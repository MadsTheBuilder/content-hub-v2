SPONSORED_HASHTAGS = {"ad", "sponsored", "partner", "gifted", "collab", "paid", "promo", "advertisement"}


def is_organic(post: dict) -> bool:
    hashtags = {h.lower().lstrip("#") for h in post.get("hashtags", [])}
    if hashtags & SPONSORED_HASHTAGS:
        return False
    if post.get("author_followers", 0) < 1000:
        return False
    if post.get("content_age_days", 0) < 3:
        return False
    description = (post.get("description", "") or "").lower()
    if any(tag in description for tag in ["#ad", "#sponsored", "#partner", "paid partnership"]):
        return False
    return True


def compute_organic_score(post: dict, platform: str) -> float:
    views = post.get("view_count", 0) or post.get("plays", 0) or 1
    likes = post.get("like_count", 0) or 0
    comments = post.get("comment_count", 0) or 0
    shares = post.get("share_count", 0) or 0
    saves = post.get("save_count", 0) or 0
    followers = max(post.get("author_followers", 1), 1)

    if platform == "tiktok":
        return views * (likes + shares + comments) / followers
    elif platform == "youtube":
        return views * (likes + comments) / followers
    elif platform == "instagram":
        engagement = saves + shares
        interaction = max(likes + comments, 1)
        return views * engagement / interaction
    else:
        return views * (likes + shares + comments) / followers
