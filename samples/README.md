# Sample responses

Example `200` responses for seven Bayt.com Jobs API endpoints. Long arrays are cut to their
first few items and long text fields are shortened. Field names and values are otherwise
unchanged.

| File | Request | Source |
|---|---|---|
| `countries.json` | `GET /countries` | public documentation |
| `cities.json` | `GET /cities?country=ae` | public documentation |
| `job-search.json` | `GET /job-search?country=ae&career_level=2` | public documentation |
| `job-search-facets.json` | `GET /job-search?country=sa&include_facets=true` | live response, 20 Oct 2026 |
| `job.json` | `GET /job?job_id=5497355` | live response, 20 Oct 2026 |
| `job-details.json` | `GET /job-details?job_id=5473846` | public documentation |
| `market-facets.json` | `GET /market-facets?country=ae` | public documentation |

The two live responses were added because live search cards carry many more fields than
the documented example (`summaryEn`, `applicantCount`, `bandUsdInferred`, confidential
employers), and `/job` has no full example in the documentation.

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
