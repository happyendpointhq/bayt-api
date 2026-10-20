"""Minimal client for the Bayt.com Jobs API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "bayt-com.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        # Post-filtered searches scan up to 10 pages upstream, so allow time.
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def salary_text(job):
    """Search cards carry a `salary` object; detail records a `salaryRange` string."""
    salary = job.get("salary")
    if isinstance(salary, dict):
        return salary.get("formatted") or "Unspecified"
    return job.get("salaryRange") or "Unspecified"


def employer(job):
    """Employer name, or "Confidential" when the employer hides it."""
    company = job.get("company") or {}
    if company.get("isConfidential"):
        return "Confidential"
    return company.get("name") or "Unknown"
