"""Scrape LinkedIn posts about interview experiences via an Apify actor.

Usage:
    export APIFY_TOKEN=apify_api_...
    pip install -r requirements.txt
    python scrape_linkedin.py

Writes one raw JSON file per query into data/raw/. Then run parse_results.py.

NOTE: check the actor's input schema on its Apify page — different LinkedIn
actors name the keyword field differently (e.g. "keyword" vs "searchQuery").
Adjust build_input() if you switch actors.
"""

import json
import sys
from datetime import date

from apify_client import ApifyClient

import config


def build_input(query: str) -> dict:
    # Input for apimaestro/linkedin-posts-search-scraper (verify on the actor page).
    return {
        "keyword": query,
        "sort_type": "relevance",
        "limit": config.MAX_POSTS_PER_QUERY,
    }


def main() -> None:
    if not config.APIFY_TOKEN:
        sys.exit("APIFY_TOKEN env var is not set. Get one at https://console.apify.com/account/integrations")

    client = ApifyClient(config.APIFY_TOKEN)
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    for i, query in enumerate(config.LINKEDIN_QUERIES):
        print(f"[linkedin {i + 1}/{len(config.LINKEDIN_QUERIES)}] {query!r}")
        try:
            run = client.actor(config.LINKEDIN_ACTOR).call(run_input=build_input(query))
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        except Exception as e:  # actor missing, quota, bad input schema…
            print(f"  FAILED: {e}", file=sys.stderr)
            continue

        out = config.RAW_DIR / f"linkedin_{date.today()}_{i}.json"
        out.write_text(json.dumps({"query": query, "items": items}, indent=2, default=str))
        print(f"  saved {len(items)} posts -> {out}")


if __name__ == "__main__":
    main()
