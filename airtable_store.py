"""
Small Airtable client shared by the C2C server (mainsys.py) and airtable_signup.py.

Reads its settings from environment variables (set them in Render -> Environment):

    AIRTABLE_TOKEN     personal access token (scopes: data.records:read, data.records:write)
    AIRTABLE_BASE_ID   base ID, starts with "app"

Uses only the Python standard library.
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

# Overridable for local testing against a fake Airtable.
API_URL = os.environ.get("AIRTABLE_API_URL", "https://api.airtable.com/v0").rstrip("/")


class AirtableError(Exception):
    """Raised when Airtable cannot be reached or rejects a request."""


def configured():
    return bool(os.environ.get("AIRTABLE_TOKEN") and os.environ.get("AIRTABLE_BASE_ID"))


def _request(method, table, params=None, body=None):
    token = os.environ.get("AIRTABLE_TOKEN")
    base_id = os.environ.get("AIRTABLE_BASE_ID")
    if not (token and base_id):
        raise AirtableError("AIRTABLE_TOKEN or AIRTABLE_BASE_ID is not set")

    url = f"{API_URL}/{base_id}/{urllib.parse.quote(table, safe='')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    # Airtable allows about 5 requests per second per base; back off briefly when it says so.
    for attempt in range(4):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read() or b"{}")
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(1 + attempt)
                continue
            raise AirtableError(f"Airtable returned {e.code} for table '{table}': {detail}") from None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 3:
                time.sleep(1 + attempt)
                continue
            raise AirtableError(f"Could not reach Airtable: {e}") from None


def create_record(table, fields):
    """Create one record. Unknown select options are created automatically."""
    result = _request("POST", table, body={"records": [{"fields": fields}], "typecast": True})
    return result["records"][0]


def list_records(table, formula=None, max_records=5000):
    """Return every record in a table (optionally filtered), newest first."""
    records, offset = [], None
    while True:
        params = {"pageSize": 100}
        if formula:
            params["filterByFormula"] = formula
        if offset:
            params["offset"] = offset
        page = _request("GET", table, params=params)
        records.extend(page.get("records", []))
        offset = page.get("offset")
        if not offset or len(records) >= max_records:
            break
    records.sort(key=lambda r: r.get("createdTime", ""), reverse=True)
    return records
