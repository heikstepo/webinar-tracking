# Raw research data

Complete video catalogs pulled 2026-08-26 from YouTube channel pages
(`ytInitialData` + InnerTube `browse` continuation — full pagination, not first page only).

| File | Channel | Videos |
|---|---|---|
| `itsjjsimon-videos.json` | @itsjjsimon (JJ Simon) — 25.3K subs | 37 |
| `daytradingrauf-videos.json` | @DayTradingRauf — 25.1K subs | 59 |
| `hanckfxbusiness-videos.json` | @HanckFXBusiness (Create And Collect) — 2.87K subs | 57 |

Each record: `{title, views, age, id}`. View counts are YouTube's rounded display
values ("22K"), so aggregates are approximate. `age` is relative to the pull date.
