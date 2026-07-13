"""Turn raw scraped JSON (data/raw/*.json) into a readable markdown digest.

- Field names differ between actors, so extraction tries a list of common keys.
- Posts are kept only if they pass the RELEVANCE_FILTER in config.py.
- Deduplicated by normalized text, sorted by engagement, grouped by source.

Usage:
    python parse_results.py
Output:
    data/interview-experiences-<date>.md
"""

import hashlib
import json
import re
from datetime import date

import config

TEXT_KEYS = ["text", "full_text", "content", "commentary", "post_text", "description"]
URL_KEYS = ["url", "postUrl", "post_url", "twitterUrl", "link", "shareUrl"]
AUTHOR_KEYS = ["author", "authorName", "author_name", "user", "username", "name"]
LIKE_KEYS = ["likeCount", "likes", "favorite_count", "favouriteCount", "numLikes", "reactions"]


def first(item: dict, keys: list[str]):
    for k in keys:
        v = item.get(k)
        if isinstance(v, dict):  # e.g. author: {"name": ...}
            v = v.get("name") or v.get("username") or v.get("screen_name")
        if v not in (None, "", [], {}):
            return v
    return None


def relevant(text: str) -> bool:
    t = text.lower()
    f = config.RELEVANCE_FILTER
    return any(w in t for w in f["must_any_interview"]) and any(w in t for w in f["must_any_role"])


def main() -> None:
    posts, seen = [], set()
    for path in sorted(config.RAW_DIR.glob("*.json")):
        blob = json.loads(path.read_text())
        source = "LinkedIn" if path.name.startswith("linkedin") else "X"
        for item in blob.get("items", []):
            if not isinstance(item, dict):
                continue
            text = str(first(item, TEXT_KEYS) or "")
            if len(text) < 80 or not relevant(text):
                continue
            key = hashlib.md5(re.sub(r"\s+", " ", text.lower())[:400].encode()).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            likes = first(item, LIKE_KEYS)
            posts.append({
                "source": source,
                "query": blob.get("query", ""),
                "text": text.strip(),
                "url": first(item, URL_KEYS),
                "author": first(item, AUTHOR_KEYS),
                "likes": int(likes) if str(likes).isdigit() else 0,
            })

    posts.sort(key=lambda p: p["likes"], reverse=True)

    out = config.DATA_DIR / f"interview-experiences-{date.today()}.md"
    lines = [f"# Scraped interview experiences — {date.today()}", ""]
    for src in ("LinkedIn", "X"):
        group = [p for p in posts if p["source"] == src]
        lines += [f"## {src} ({len(group)} posts)", ""]
        for p in group:
            head = f"**{p['author'] or 'unknown'}** · {p['likes']} likes"
            if p["url"]:
                head += f" · [link]({p['url']})"
            body = "\n".join(f"> {ln}" for ln in p["text"].splitlines() if ln.strip())
            lines += [head, "", body, "", "---", ""]
    out.write_text("\n".join(lines))
    print(f"kept {len(posts)} relevant posts -> {out}")


if __name__ == "__main__":
    main()
