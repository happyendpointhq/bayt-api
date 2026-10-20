"""Who is hiring where: live job counts by industry, city, career level and employer.

    python hiring_snapshot.py sa
    python hiring_snapshot.py ae --top 15

One /job-search call with include_facets=true returns the counts alongside the first page of
jobs. /market-facets returns the same kind of aggregates without the job rows.
"""

import argparse

from client import get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("country", nargs="?", default="ae", help="ISO code from /countries")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    data = get("/job-search", country=args.country, include_facets="true")
    print(f"{data['count']:,} open jobs in {args.country.upper()}\n")
    for name, values in (data.get("facets") or {}).items():
        if not values:
            continue
        print(name)
        for item in values[: args.top]:
            print(f"  {item['count']:>7,}  {item['label']}")
        print()


if __name__ == "__main__":
    main()
