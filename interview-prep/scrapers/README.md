# Apify Scrapers — LinkedIn & X interview-experience posts

Pulls recent public posts where people share their interview experiences and the questions
they were asked, then distills them into a markdown digest you can fold back into the
question bank.

## Setup & run

```bash
cd interview-prep/scrapers
pip install -r requirements.txt
export APIFY_TOKEN=apify_api_...        # console.apify.com → Settings → Integrations

python scrape_linkedin.py               # LinkedIn post search  → data/raw/linkedin_*.json
python scrape_x.py                      # X keyword search      → data/raw/x_*.json
python parse_results.py                 # → data/interview-experiences-<date>.md
```

Tune queries and volumes in `config.py` (`MAX_POSTS_PER_QUERY=50` keeps first runs cheap;
bump the `since:` dates in `X_QUERIES` each run).

## Actors used (verify before a paid run)

| Platform | Default actor | Notes |
|---|---|---|
| LinkedIn | `apimaestro/linkedin-posts-search-scraper` | keyword post search, no cookies needed. Alternative: `curious_coder/linkedin-post-search-scraper`. Override with `LINKEDIN_ACTOR` env var. |
| X | `apidojo/tweet-scraper` (Tweet Scraper V2) | richest search-operator support (`min_faves:`, `since:`, `lang:`), ~$0.40/1k tweets. Cheaper: kaitoeasyapi's pay-per-result scraper (~$0.25/1k). Override with `X_ACTOR`. |

Actor input schemas change — if a run fails immediately, open the actor's page on
apify.com, check its **Input** tab, and adjust `build_input()` in the scraper (it's one
small dict per script).

## Cost expectations
With defaults (6 LinkedIn queries + 4 X queries × 50 posts): a few hundred results per run,
typically **well under $5** on pay-per-result actors. Set a spending limit in the Apify
console before the first run anyway.

## Ethics / terms note
These scrapers collect **public posts only**, at low volume, for personal interview prep.
Automated collection can still violate a platform's Terms of Service (LinkedIn is
notoriously strict and X restricts automated access) — Apify runs the actors on its own
infrastructure, but the responsibility for how you use them is yours. Keep volumes small,
don't republish scraped content verbatim, and credit authors if you quote their posts.

## Folding results back into the bank
Open `data/interview-experiences-<date>.md`, pick the posts with concrete questions, and
add them to `india/04-company-experiences.md` or `us-global/04-company-loops.md` with the
post link as source. (Or hand the digest to Claude and ask it to merge + answer the new
questions.)
