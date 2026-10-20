"""Find a city's id, search recent mid-career jobs there, then open the first one.

    python quickstart.py            # Dubai
    python quickstart.py sa riyadh  # country code and city slug
"""

import sys

from client import employer, get, salary_text

country = sys.argv[1] if len(sys.argv) > 1 else "ae"
city_slug = sys.argv[2] if len(sys.argv) > 2 else "dubai"

# 1. City ids are composite ("ae,4,0"); copy them from /cities, names are rejected.
cities = get("/cities", country=country)
city = next((c for c in cities["cities"] if c["slug"] == city_slug), None)
if city is None:
    raise SystemExit(f"No city {city_slug!r} in {country}. Try: {[c['slug'] for c in cities['cities'][:10]]}")
print(f"{city['name']} (id {city['id']}): {city['jobsCount']:,} jobs")

# 2. Mid-career jobs posted in the past 7 days, newest first, 30 per page.
results = get("/job-search", city=city["id"], career_level="2", date_posted="2")
print(f"{results['count']:,} matching jobs, page {results['page']} of {results['maxPage']}\n")
for job in results["jobs"][:10]:
    print(f"{job['postedAt'][:10]}  {job['title'][:48]:<48}  {employer(job)[:28]:<28}  {salary_text(job)}")

# 3. The job record: description, skills, employment type, experience and salary band.
#    (/job-details adds expiry, the AI summary and the employer profile.)
if results["jobs"]:
    job = get("/job", job_id=results["jobs"][0]["jobId"])
    print(f"\n{job['title']}, {job['locationFormatted']}")
    print(f"{job.get('employmentType')}, {job.get('careerLevel')}, vacancies: {job.get('vacancies')}")
    years = (job.get("experienceMinYears"), job.get("experienceMaxYears"))
    print(f"Experience: {years[0]} to {years[1]} years")
    if job.get("salaryBandUsdMin") is not None:
        inferred = " (inferred)" if job.get("salaryBandUsdInferred") else ""
        print(f"Salary band: USD {job['salaryBandUsdMin']:,} to {job['salaryBandUsdMax']:,} a month{inferred}")
    for skill in (job.get("skills") or [])[:5]:
        print(f"  - {skill[:100]}")
