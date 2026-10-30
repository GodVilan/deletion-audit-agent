# Usage report

**Pricing source:** Anthropic list prices for Claude Opus 5.5 (`claude-opus-5-5`), $4.00 per 1M input tokens and $20.00 per 1M output tokens. Source: the model price table in Anthropic's Claude API reference as bundled with Claude Code (cached 2026-10-06). No prompt caching or batch discount is applied. Rejected requests (HTTP 400) are not billed.

## Final full-dataset run that produced output.csv

Run on 2026-10-24 at 19:13Z in the repository with the key: `INTENT_CACHE_PATH=<empty temp file> python3 code/main.py --refresh-media` (empty intent cache, live media extraction), `MAX_WORKERS=8`. Its output is **byte-identical** to the submitted `output.csv` (sha256 `c140419a317d70ecd5d0daf1106154180c0cc5f6a7eaa703d726e3af5c476490`, 0 changed cases). The shipped media cache `code/cache/media/` is this run's extraction. All counters below are exact: the client counts per role.

| | value |
|---|---|
| provider / model | Anthropic / `claude-opus-5-5` (both roles) |
| intent paths | 518/518 agent: 380 live tool loops + 138 reuses of this run's own agent answers for duplicate request texts (375 distinct texts; parallel threads raced on 5). **0 fallback** |
| successful API calls | **775** (intent 760, media 15) |
| input tokens | **834,578** |
| output tokens | **92,821** |
| total tokens | **927,399** |
| average tokens per request (518) | **1,790** (1,611 input + 179 output) |
| estimated total cost | **$5.19** (input $3.34 + output $1.86) |
| estimated cost per request | **$0.0100** |
| retries | 0 |
| rejected (HTTP 400, not billed) | 8, all media: the forced-`tool_choice` attempt that the model rejects, after which the extractor uses `auto` + strict + nudge |
| errors (retries exhausted) | 0 |
| wall time | **273.7 s** (intent 245.6 s, media 27.3 s) |

| role | calls | input tokens | output tokens | total tokens | est. cost | retries | rejected | errors | wall time |
|---|---|---|---|---|---|---|---|---|---|
| intent (R1) | 760 | 772,732 | 74,389 | 847,121 | $4.58 | 0 | 0 | 0 | 245.6 s |
| media extraction (11 PNG + 4 PDF) | 15 | 61,846 | 18,432 | 80,278 | $0.62 | 0 | 8 | 0 | 27.3 s |
| **overall** | **775** | **834,578** | **92,821** | **927,399** | **$5.19** | **0** | **8** | **0** | **273.7 s** |

## Development runs

| run | calls | input tokens | output tokens | retries | rejected | wall time | est. cost |
|---|---|---|---|---|---|---|---|
| clean-unzip live run (empty intent cache, `--refresh-media`); output byte-identical. The API credit ran out at case_497, so its last 38 intent calls were rejected with HTTP 400 "credit balance is too low" and used the deterministic fallback (0 disagreements) | 707 | 763,830 | 86,499 | 0 | 46 (38 credit, 8 forced tool_choice) | 262.9 s | $4.79 |
| intent, first full 518 run (sequential, before parallelization) | 732 | 744,256 | 71,761 | n/a (SDK built-in) | 0 | 2,036 s | $4.41 |
| media extraction media-v1 (15 files) | 15 | 61,801 | 18,322 | 0 | 8 | 30.9 s | $0.61 |
| parallel intent check, 32 samples, temp cache | 64 | 64,791 | 6,771 | 0 | 0 | 28.4 s | $0.40 |
| media re-extraction media-v2 (example id `user_123` removed) | 15 | 61,846 | 19,294 | 0 | 8 | 30.7 s | $0.63 |
| golden trace (case_07, case_538) | 4 | 4,157 | 383 | 0 | 0 | – | $0.02 |
| golden trace regeneration (live, case_07 + case_538; final GOLDEN_TRACE.md) | 4 | 4,157 | 391 | 0 | 0 | – | $0.02 |
| one earlier scorer run on the samples (usage not persisted; estimated from full-run averages) | ≈64 | ≈65,000 | ≈6,000 | – | – | – | ≈$0.38 |

**All runs, including the final run:** ≈2,376 successful calls, ≈2,600,300 input / ≈301,900 output tokens, about **$16.4**. Not included: the custom-case and golden-trace checks on 2026-10-24 (a few small calls).

## Reproducing without a key

Without `ANTHROPIC_API_KEY`, intents use the deterministic fallback, which agrees with the agent on 518/518 requests. Media comes from the shipped cache `code/cache/media/`. The keyless output is byte-identical (same sha256). A media file with neither a key nor a cache hit is flagged `media_unread`.
