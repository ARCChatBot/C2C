"""
Saves C2C student sign-ups from index.html into Airtable.

The sign-up form in index.html POSTs JSON to /api/register-interest on your
Render server. This file does the Airtable part on the server, so the Airtable
token is never visible in the web page.

------------------------------------------------------------------------------
1. Airtable setup
------------------------------------------------------------------------------
Create a table (for example "C2C Sign-Ups") with these fields, spelled exactly:

    V Number        Single line text
    First Name      Single line text
    Last Name       Single line text
    Email           Email
    Classification  Single select   (options are created automatically)
    Interests       Multiple select (options are created automatically)
    Signed Up At    Created time    (optional; Airtable fills it in by itself)

Create a personal access token at https://airtable.com/create/tokens with the
scope "data.records:write" and access to only this base.

------------------------------------------------------------------------------
2. Render setup  (Dashboard -> your Web Service -> Environment)
------------------------------------------------------------------------------
    AIRTABLE_TOKEN   the token from step 1
    AIRTABLE_BASE_ID the base ID; it starts with "app" (from the base's URL)
    AIRTABLE_TABLE   the table name, e.g. C2C Sign-Ups

Never put these values in index.html or commit them to GitHub.

------------------------------------------------------------------------------
3. Add the route to your server
------------------------------------------------------------------------------
Put this file next to your server's main file, then add ONE of these.

Flask:
    from flask import request, jsonify
    from airtable_signup import save_signup

    @app.post("/api/register-interest")
    def register_interest():
        ok, status, message = save_signup(request.get_json(silent=True) or {})
        return jsonify({"ok": ok} if ok else {"error": message}), status

FastAPI:
    from fastapi import Request
    from fastapi.responses import JSONResponse
    from airtable_signup import save_signup

    @app.post("/api/register-interest")
    async def register_interest(request: Request):
        ok, status, message = save_signup(await request.json())
        return JSONResponse({"ok": ok} if ok else {"error": message}, status_code=status)

Uses only the Python standard library; nothing to install.
"""

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

V_PATTERN = re.compile(r"^V\d{8}$")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
CLASSIFICATIONS = {"Freshman", "Sophomore", "Junior", "Senior", "Graduate"}
INTERESTS = {
    "Computer-Based Training", "3D Simulation", "VR Cleanroom",
    "AR Data Visualization", "3D Printer & Equipment",
}


def _clean(value, limit=100):
    return str(value or "").strip()[:limit]


def save_signup(data):
    """Validate one sign-up and create an Airtable record.

    Returns (ok, http_status, message). The message is safe to show students.
    """
    v_number = _clean(data.get("v_number"), 9).upper()
    first = _clean(data.get("first_name"))
    last = _clean(data.get("last_name"))
    email = _clean(data.get("email"), 254)
    classification = _clean(data.get("classification"), 20)
    interests = data.get("interests") or []
    interests = [i for i in interests if isinstance(i, str) and i in INTERESTS] if isinstance(interests, list) else []

    if not V_PATTERN.match(v_number):
        return False, 400, "Enter your V# as the letter V followed by 8 digits."
    if not first or not last:
        return False, 400, "Enter both your first and last name."
    if not EMAIL_PATTERN.match(email):
        return False, 400, "Enter a valid email address."
    if classification not in CLASSIFICATIONS:
        return False, 400, "Choose your classification."

    token = os.environ.get("AIRTABLE_TOKEN")
    base_id = os.environ.get("AIRTABLE_BASE_ID")
    table = os.environ.get("AIRTABLE_TABLE")
    if not (token and base_id and table):
        print("airtable_signup: AIRTABLE_TOKEN, AIRTABLE_BASE_ID or AIRTABLE_TABLE is not set")
        return False, 500, "Sign-up is temporarily unavailable. Please tell the C2C team."

    url = f"https://api.airtable.com/v0/{base_id}/{urllib.parse.quote(table, safe='')}"
    payload = {
        "records": [{"fields": {
            "V Number": v_number,
            "First Name": first,
            "Last Name": last,
            "Email": email,
            "Classification": classification,
            "Interests": interests,
        }}],
        "typecast": True,  # lets Airtable create new select options automatically
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True, 200, "Saved"
    except urllib.error.HTTPError as e:
        # Logged on the server only; students get a generic message.
        print(f"airtable_signup: Airtable returned {e.code}: {e.read().decode(errors='replace')[:500]}")
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"airtable_signup: could not reach Airtable: {e}")
    return False, 502, "Your sign-up could not be saved right now. Please try again later."
