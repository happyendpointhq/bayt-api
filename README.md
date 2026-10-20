# Bayt API and Scraper

The Bayt API returns job listings from Bayt.com, the largest job site in the Middle East, as
JSON: vacancies in the UAE, Saudi Arabia, Qatar, Egypt, Kuwait and beyond, with salary
bands in local currency and normalised USD, career level, employment type, remote type,
employer, skills and live hiring counts by industry, city and employer. Bayt.com does not
publish a public developer API for its listings, so this REST API is the way to scrape
Bayt jobs into your own code without maintaining a Bayt scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/bayt-api?utm_source=github&utm_medium=readme&utm_campaign=bayt-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/bayt-com
- Product page: https://happyendpoint.com/library/bayt-api?utm_source=github&utm_medium=readme&utm_campaign=bayt-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://bayt-com.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 15, all `GET` |
| Coverage | 17 MENA markets plus international listings (`/countries`) |
| Languages | English and Arabic (`language=en` or `ar`) |
| Page size | 30 jobs per page, newest first |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Search**
- Jobs by country, province, city, career level, employment type, industry, company, company type, posting age, remote type and listing source
- Salary filters in normalised monthly USD or in one currency, "salary published only", easy apply, maximum required experience, excluding confidential employers
- Search by pasting a Bayt.com search URL, and all jobs from one employer
- Optional facet counts with every search

**Jobs**
- Title, posting date and age, location, career level, remote type, easy apply flag
- Salary band: code, USD minimum and maximum, local currency and the formatted range
- Employer name, logo and profile link, or a confidential flag
- Full record: description, skills, employment type, vacancies, experience range, education, and the employer profile

**Reference and market data**
- Countries with live job counts, cities and provinces with their IDs, job title autocomplete
- The filter taxonomy (career levels, industries, salary bands, currencies) in one call
- Live job counts by industry, career level, city, province and employer
- Popular jobs and similar jobs

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/bayt-com). Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

City filters take a composite ID such as `ae,4,0`, not a name. Look it up first:

```bash
curl "https://bayt-com.p.rapidapi.com/cities?country=ae" \
  -H "x-rapidapi-host: bayt-com.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://bayt-com.p.rapidapi.com/job-search?city=ae,4,0&career_level=2&date_posted=2" \
  -H "x-rapidapi-host: bayt-com.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py ae dubai
```

```python
from client import get

dubai = next(c for c in get("/cities", country="ae")["cities"] if c["slug"] == "dubai")
results = get("/job-search", city=dubai["id"], date_posted="2")
for job in results["jobs"]:
    print(job["postedAt"][:10], job["title"], job["salary"]["formatted"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs ae dubai
```

---

## Example response

One job card from `GET /job-search?country=ae&career_level=2`, trimmed. Values are the
example in the API's public documentation. Full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "count": 10068,
    "page": 1,
    "pageSize": 30,
    "maxPage": 334,
    "resultWindowExhausted": true,
    "jobs": [
      {
        "jobId": "5473846",
        "title": "Senior Estimator",
        "postedAt": "2026-08-15T06:12:41.000Z",
        "daysOld": 1,
        "locationFormatted": "Dubai, United Arab Emirates",
        "careerLevel": "Mid career",
        "remoteType": "onsite",
        "isEasyApply": true,
        "salary": {
          "bandCode": "7",
          "bandUsdMin": 4000,
          "bandUsdMax": 5000,
          "currencyCode": "AED",
          "formatted": "AED 14,690 - AED 18,363",
          "isSpecified": true
        },
        "company": { "name": "Accenture", "companyId": "4023641", "isConfidential": false }
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://bayt-com.p.rapidapi.com`

### Reference

| Endpoint | Returns |
|---|---|
| `GET /countries` | Supported countries with live job counts |
| `GET /cities` | Cities and provinces in one country, with the IDs the `city` filter takes |
| `GET /taxonomy` | Career levels, industries, employment types, salary bands, currencies and other vocabularies |
| `GET /autocomplete` | Job title suggestions for a partial keyword |

### Search

| Endpoint | Returns |
|---|---|
| `GET /job-search` | Jobs matching every filter, newest first, 30 a page, with optional facets |
| `GET /job-search-by-url` | The results of a pasted Bayt.com search URL |
| `GET /company-jobs` | All open jobs from one employer |
| `GET /popular-jobs` | Currently popular jobs |
| `GET /similar-jobs` | Jobs similar to one job |

### Jobs

| Endpoint | Returns |
|---|---|
| `GET /job-details` | Full posting: description, skills, expiry, AI summary, employer profile |
| `GET /job-details-by-url` | The same, from a Bayt.com job URL |
| `GET /job` | Lightweight record: description, skills, employment type, experience, salary band |
| `GET /job-listing` | The search card for one job |

### Market

| Endpoint | Returns |
|---|---|
| `GET /market-facets` | Live job counts by industry, career level, location, employer and more |
| `GET /status` | Service health |

---

## Things to know about the data

Most of these come from running the examples against the live API in October 2026.

- **The salary is a band, not the employer's figure.** `formatted` is the USD band
  converted into the job's currency: "AED 3,673 - AED 5,509" is the USD 1,000 to 1,500 band
  at 3.6725 dirhams to the dollar. Compare jobs on `bandUsdMin` and `bandUsdMax`, and read
  `bandUsdInferred`, which marks a band Bayt inferred rather than one the employer published.
- **Many jobs publish no salary.** In a live Dubai search, 11 of the 30 jobs on the first page
  read `"Unspecified"` with null USD bands. Use `salary_specified_only=true` when salary is the
  point of the analysis.
- **Keyword and salary filters only scan a few pages.** They are post-filters: the API reads
  `scan_pages` pages (default 3, maximum 10, 30 jobs each) and keeps the matches. In our
  live test, `country=ae&keyword=accountant&salary_specified_only=true` reported a `count` of
  14,175 (the total before post-filtering) but scanned 90 jobs and matched 1. Read
  `postFilter.jobsScanned` and `jobsMatched`, raise `scan_pages`, and narrow with `city`,
  `industry` or `date_posted` first, since those filter the whole index.
- **The result window stops at 10,000 jobs.** `count` can be larger, but rows end at page
  334. `resultWindowExhausted` tells you when; split by city or posting date.
- **City IDs are composite.** `city` takes `ae,4,0` from `/cities`; a name or a truncated ID
  is a 400. Several cities are joined with a pipe: `ae,4,0|eg,2,10`.
- **Facets do not all add up to the total.** In a live Saudi Arabia search (6,966 jobs) the
  career level facet summed to a few hundred, because only postings that declare a level are
  counted, and one catch-all industry ("Other Business Support Services") held 5,456. The
  `countries` facet ignores the `country` filter and shows every market.
- **Confidential employers.** Some jobs show `"Confidential Company"` with a null
  `companyId`. `company.isConfidential` flags them, and `exclude_confidential=true` drops them.
- **Card and record shapes differ.** Search cards carry a `salary` object; `/job` carries flat
  `salaryBandUsdMin` and `salaryBandUsdMax`; `/job-details` has a formatted `salaryRange`
  string. `client.salary_text()` handles them.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | City ID lookup, a filtered search for the past 7 days, one job record with skills and salary band |
| [`examples/python/salary_bands.py`](examples/python/salary_bands.py) | Published salaries for a role in one country, by career level, in normalised USD, to CSV |
| [`examples/python/hiring_snapshot.py`](examples/python/hiring_snapshot.py) | Who is hiring where: job counts by industry, city, career level and employer, in one call |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Example responses for seven endpoints |

---

## API or your own Bayt scraper

A Bayt scraper has to keep up with page changes, Arabic and English variants, salary bands
and pagination limits. This API returns the same jobs as documented JSON with a stable
contract, so the work you keep is the analysis. If you need a recurring export of a market
rather than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=bayt-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can search Bayt jobs
without code:

```json
{
  "mcpServers": {
    "bayt": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: bayt-com.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Bayt API?

Bayt.com does not publish a public developer API for its job listings. This API, built and
maintained by Happy Endpoint and independent of Bayt.com, provides that access as REST and
JSON.

### Is there a free Bayt API?

Yes. The [RapidAPI listing](https://rapidapi.com/happyendpoint/api/bayt-com) has a free plan, and every endpoint can be tried on it.

### Can I get Bayt job salaries through the API?

Yes, where the posting has one. Every job card carries a salary band in local currency and
in normalised monthly USD. [`salary_bands.py`](examples/python/salary_bands.py) summarises
them by career level.

### How do I scrape Bayt jobs in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call `/job-search` with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) is a small client, and the
other scripts in that folder are ready to run.

### Can I get all jobs from one company on Bayt?

Yes. `/company-jobs` takes the employer slug (for example `accenture`), which you can find in
the `companies` facet of `/market-facets` or of a search with `include_facets=true`.

### Does the API return Arabic job listings?

Yes. Every endpoint takes `language=en` or `language=ar`, and job cards carry both an
English and an Arabic summary.

### Do you cover other Gulf and Saudi sites?

Yes, including Aqar and Wasalt for Saudi property and Bayut and PropertyFinder for the UAE.
See the [API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=bayt-api).

---

## Related repos

- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment and labour-market research
- [aqar-api](https://github.com/happyendpointhq/aqar-api) - Saudi Arabia property listings and district prices
- [wasalt-api](https://github.com/happyendpointhq/wasalt-api) - Saudi listings, REGA licences and Infath auctions
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - Bayut and PropertyFinder in one API

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
