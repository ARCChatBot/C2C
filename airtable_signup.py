"""
Validates C2C student sign-ups from index.html and saves them to Airtable.

mainsys.py calls save_signup() from the /api/register-interest route.
Airtable setup (table and field names) is described in README.md.
"""

import os
import re

import airtable_store

SIGNUPS_TABLE = os.environ.get("AIRTABLE_SIGNUPS_TABLE", "C2C Sign-Ups")

V_PATTERN = re.compile(r"^V00\d{6}$")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
CLASSIFICATIONS = {"Freshman", "Sophomore", "Junior", "Senior", "Graduate"}
INTERESTS = {
    "Computer-Based Training", "3D Simulation", "VR Cleanroom",
    "AR Data Visualization", "3D Printer & Equipment",
}


def _clean(value, limit=100):
    return str(value or "").strip()[:limit]


def normalize_v(raw):
    """Uppercase, drop spaces and dashes, and fix a letter O typed for zero in 'V00'."""
    v = re.sub(r"[\s-]", "", _clean(raw, 20).upper())
    if re.match(r"^V[O0]{2}", v):
        v = "V00" + v[3:]
    return v


def save_signup(data):
    """Validate one sign-up and create an Airtable record.

    Returns (ok, http_status, message). The message is safe to show students.
    """
    v_number = normalize_v(data.get("v_number"))
    first = _clean(data.get("first_name"))
    last = _clean(data.get("last_name"))
    email = _clean(data.get("email"), 254)
    classification = _clean(data.get("classification"), 20)
    interests = data.get("interests") or []
    interests = [i for i in interests if isinstance(i, str) and i in INTERESTS] if isinstance(interests, list) else []

    if not V_PATTERN.match(v_number):
        return False, 400, "Enter your V# as V00 followed by 6 numbers."
    if not first or not last:
        return False, 400, "Enter both your first and last name."
    if not EMAIL_PATTERN.match(email):
        return False, 400, "Enter a valid email address."
    if classification not in CLASSIFICATIONS:
        return False, 400, "Choose your classification."

    if not airtable_store.configured():
        print("airtable_signup: AIRTABLE_TOKEN or AIRTABLE_BASE_ID is not set")
        return False, 503, "Sign-up is temporarily unavailable. Please tell the C2C team."
    try:
        airtable_store.create_record(SIGNUPS_TABLE, {
            "V Number": v_number,
            "First Name": first,
            "Last Name": last,
            "Email": email,
            "Classification": classification,
            "Interests": interests,
        })
        return True, 200, "Saved"
    except airtable_store.AirtableError as e:
        print(f"airtable_signup: {e}")  # server log only
        return False, 502, "Your sign-up could not be saved right now. Please try again later."
