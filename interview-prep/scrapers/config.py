"""Configuration for the Apify interview-experience scrapers.

Actor IDs are overridable via env vars because Apify Store actors evolve;
verify the actor page + its input schema before a paid run:
  - LinkedIn: https://apify.com/apimaestro/linkedin-posts-search-scraper
    (alternative: curious_coder/linkedin-post-search-scraper)
  - X/Twitter: https://apify.com/apidojo/tweet-scraper  (Tweet Scraper V2)
    (cheaper alternative: kaitoeasyapi's pay-per-result tweet scraper, ~$0.25/1k)
"""

import os
from pathlib import Path

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")

LINKEDIN_ACTOR = os.environ.get("LINKEDIN_ACTOR", "apimaestro/linkedin-posts-search-scraper")
X_ACTOR = os.environ.get("X_ACTOR", "apidojo/tweet-scraper")

# Keep per-query volumes low on the first run to sanity-check cost + relevance.
MAX_POSTS_PER_QUERY = int(os.environ.get("MAX_POSTS_PER_QUERY", "50"))

DATA_DIR = Path(__file__).parent / "data"
RAW_DIR = DATA_DIR / "raw"

# ---------------------------------------------------------------------------
# Search queries — tuned for people sharing their own interview experiences.
# ---------------------------------------------------------------------------

LINKEDIN_QUERIES = [
    '"interview experience" AI engineer',
    '"interview experience" GenAI',
    '"interview questions" LLM engineer',
    '"interview experience" machine learning engineer fresher',
    '"cracked" interview "AI engineer"',
    '"interview experience" SDE 1',
]

# apidojo/tweet-scraper supports full X search operators.
# min_faves filters low-signal posts; adjust the since: date on each run.
X_QUERIES = [
    '"interview experience" (AI engineer OR "GenAI" OR "LLM engineer") lang:en min_faves:20 since:2025-06-01',
    '"interview questions" (RAG OR langchain OR "AI engineer") lang:en min_faves:20 since:2025-06-01',
    '"got asked" interview (LLM OR RAG OR "AI engineer") lang:en min_faves:10 since:2025-06-01',
    '"interview experience" (SDE OR "software engineer") india lang:en min_faves:20 since:2025-06-01',
]

# parse_results.py keeps a post only if it matches at least one term from EACH group.
RELEVANCE_FILTER = {
    "must_any_interview": ["interview", "hiring process", "recruitment"],
    "must_any_role": [
        "ai engineer", "genai", "gen ai", "llm", "machine learning", "ml engineer",
        "rag", "langchain", "data scientist", "sde", "software engineer",
    ],
}
