"""Summarise published salaries for a role in one country, by career level, and save a CSV.

    python salary_bands.py accountant --country ae --out uae-accountant.csv

Salary filters and the keyword are post-filters: the API scans `scan_pages` pages of 30 jobs
(maximum 10, so 300 jobs) and keeps the matches. `postFilter` reports how many were scanned
and matched; `count` stays the total before post-filtering. Salaries are compared in the
normalised monthly USD band (`bandUsdMin`/`bandUsdMax`), so AED, SAR and QAR posts line up.
"""

import argparse
import csv
from collections import defaultdict
from statistics import median

from client import employer, get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword")
    parser.add_argument("--country", default="ae", help="ISO code from /countries, e.g. ae, sa, qa")
    parser.add_argument("--scan-pages", type=int, default=10, help="1 to 10, 30 jobs a page (one call either way)")
    parser.add_argument("--out", default="salary-bands.csv")
    args = parser.parse_args()

    data = get(
        "/job-search",
        country=args.country,
        keyword=args.keyword,
        salary_specified_only="true",
        scan_pages=args.scan_pages,
    )
    scan = data.get("postFilter") or {}
    print(f"Scanned {scan.get('jobsScanned')} jobs, {scan.get('jobsMatched')} publish a salary "
          f"(truncated: {scan.get('scanTruncated')})")

    rows, by_level = [], defaultdict(list)
    for job in data["jobs"]:
        band = job.get("salary") or {}
        low, high = band.get("bandUsdMin"), band.get("bandUsdMax")
        if low is None or high is None:
            continue
        mid = (low + high) / 2
        level = job.get("careerLevel") or "Not stated"
        by_level[level].append(mid)
        rows.append({
            "job_id": job["jobId"],
            "title": job["title"],
            "employer": employer(job),
            "location": job.get("locationFormatted"),
            "career_level": level,
            "posted_at": job.get("postedAt"),
            "salary_as_posted": band.get("formatted"),
            "currency": band.get("currencyCode"),
            "band_usd_min": low,
            "band_usd_max": high,
            "url": job.get("url"),
        })

    print(f"\n{'career level':<22} jobs  median band midpoint (USD a month)")
    for level, mids in sorted(by_level.items(), key=lambda kv: median(kv[1])):
        print(f"{level:<22} {len(mids):>4}  {median(mids):>10,.0f}")

    if rows:
        with open(args.out, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nWrote {len(rows)} jobs to {args.out}")


if __name__ == "__main__":
    main()
