---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/storage/client.py"
category: "Content Hub Source Code"
---

# client.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
from backend.database import get_supabase
import logging
import uuid

logger = logging.getLogger(__name__)

_BUCKET = "content-hub"
_PUBLIC_URL_PREFIX = "/storage/v1/object/public/content-hub/"


async def upload_file(user_id: str, workflow_id: str, file_bytes: bytes, filename: str, content_type: str = "image/png") -> str:
    sb = get_supabase()
    path = f"{user_id}/{workflow_id}/{uuid.uuid4().hex}/{filename}"
    sb.storage.from_(_BUCKET).upload(path, file_bytes, {"content-type": content_type})
    return sb.storage.from_(_BUCKET).get_public_url(path)


def delete_files(urls: list[str]) -> None:
    """Delete a list of Supabase Storage files by their public URLs.

    Extracts the storage path from each URL and removes the object from the
    bucket. Logs warnings on failure but never raises — callers should not
    fail because storage cleanup failed.
    """
    if not urls:
        return

    sb = get_supabase()
    paths = []
    for url in urls:
        idx = url.find(_PUBLIC_URL_PREFIX)
        if idx == -1:
            logger.warning("delete_files: unrecognised URL format, skipping: %s", url)
            continue
        paths.append(url[idx + len(_PUBLIC_URL_PREFIX):])

    if not paths:
        return

    try:
        sb.storage.from_(_BUCKET).remove(paths)
        logger.debug("Deleted %d storage object(s): %s", len(paths), paths)
    except Exception:
        logger.warning("Storage deletion failed for paths: %s", paths, exc_info=True)

```
