"""Scrape X (Twitter) posts about interview experiences via an Apify actor.

Usage:
    export APIFY_TOKEN=apify_api_...
    python scrape_x.py

Default actor apidojo/tweet-scraper (Tweet Scraper V2) supports native X search
operators (min_faves:, since:, lang:), which config.X_QUERIES already use.
Writes one raw JSON file per query into data/raw/. Then run parse_results.py.
"""

import json
import sys
from datetime import date

from apify_client import ApifyClient

import config


def build_input(query: str) -> dict:
    # Input for apidojo/tweet-scraper (verify on the actor page).
    return {
        "searchTerms": [query],
        "maxItems": config.MAX_POSTS_PER_QUERY,
        "sort": "Top",
    }


def main() -> None:
    if not config.APIFY_TOKEN:
        sys.exit("APIFY_TOKEN env var is not set. Get one at https://console.apify.com/account/integrations")

    client = ApifyClient(config.APIFY_TOKEN)
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    for i, query in enumerate(config.X_QUERIES):
        print(f"[x {i + 1}/{len(config.X_QUERIES)}] {query!r}")
        try:
            run = client.actor(config.X_ACTOR).call(run_input=build_input(query))
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        except Exception as e:
            print(f"  FAILED: {e}", file=sys.stderr)
            continue

        out = config.RAW_DIR / f"x_{date.today()}_{i}.json"
        out.write_text(json.dumps({"query": query, "items": items}, indent=2, default=str))
        print(f"  saved {len(items)} posts -> {out}")


if __name__ == "__main__":
    main()
