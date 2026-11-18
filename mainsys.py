"""
Operation SEMI / C2C training server.

Serves the dashboard (/), the CBT portal (/cbt) and the admin portal (/admin),
and stores every sign-up, sign-in and training result in Airtable.

Run locally:   uvicorn mainsys:app --reload
On Render:     uvicorn mainsys:app --host 0.0.0.0 --port $PORT   (see render.yaml)
Setup:         README.md
"""

import csv
import hmac
import io
import os
import re
import time
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, StreamingResponse
from pydantic import BaseModel

import airtable_store
from airtable_signup import SIGNUPS_TABLE, V_PATTERN, normalize_v, save_signup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SIGNINS_TABLE = os.environ.get("AIRTABLE_SIGNINS_TABLE", "Sign-Ins")
RESULTS_TABLE = os.environ.get("AIRTABLE_RESULTS_TABLE", "Training Results")

app = FastAPI(title="Operation SEMI Training System API", version="2.0")

# Sites on other addresses (GitHub Pages, the VR, 3D and AR apps) that may call this API.
# Comma-separated list in ALLOWED_ORIGINS; pages served by this server itself need no entry.
ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "https://arcchatbot.github.io").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Admin-Key"],
)


# ----------------------------------------------------------------------------- helpers

def clean(value, limit=200):
    return str(value or "").strip()[:limit]


def require_v(raw):
    v = normalize_v(raw)
    if not V_PATTERN.match(v):
        raise HTTPException(status_code=400, detail="Enter your Student ID as V00 followed by 6 numbers.")
    return v


def require_storage():
    if not airtable_store.configured():
        print("mainsys: AIRTABLE_TOKEN or AIRTABLE_BASE_ID is not set")
        raise HTTPException(status_code=503, detail="The training database is not connected yet. Please tell the C2C team.")


def require_admin(key):
    expected = os.environ.get("ADMIN_PASSWORD", "")
    if not expected:
        raise HTTPException(status_code=503, detail="ADMIN_PASSWORD is not set on the server.")
    if not key or not hmac.compare_digest(key.encode(), expected.encode()):
        raise HTTPException(status_code=401, detail="Wrong admin password.")


def store(action, *args):
    """Run an Airtable call; turn failures into a clean 502 for the browser."""
    try:
        return action(*args)
    except airtable_store.AirtableError as e:
        print(f"mainsys: {e}")  # full detail stays in the server log
        raise HTTPException(status_code=502, detail="The training database could not be reached. Please try again.")


def system_for(track, given=""):
    """Which training system a result came from, for the admin dashboard."""
    if given:
        return clean(given, 60)
    t = track.lower()
    if t.startswith("2d cbt") or "cbt" in t:
        return "CBT"
    if "vr" in t:
        return "VR Cleanroom"
    if "ar " in t or "augmented" in t:
        return "AR Data Visualization"
    if "3d" in t:
        return "3D Simulation"
    if any(k in t for k in ("equipment", "printer", "multimeter", "hololens", "jetson", "oculus")):
        return "Physical Equipment"
    return "Other"


def result_row(r):
    f = r.get("fields", {})
    return {
        "id": r.get("id"),
        "student_id": f.get("V Number", ""),
        "full_name": f.get("Full Name", ""),
        "system": f.get("System", ""),
        "track": f.get("Activity", ""),
        "score": f.get("Score"),
        "timestamp": r.get("createdTime", ""),
    }


# ----------------------------------------------------------------------------- pages

def page(name):
    return FileResponse(os.path.join(BASE_DIR, name))


@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
def read_index():
    return page("index.html")


@app.get("/cbt", include_in_schema=False)
@app.get("/cbt.html", include_in_schema=False)
def read_cbt():
    return page("cbt.html")


@app.get("/admin", include_in_schema=False)
@app.get("/admin.html", include_in_schema=False)
def read_admin():
    return page("admin.html")


@app.get("/c2c-connect.js", include_in_schema=False)
def read_connector():
    return FileResponse(os.path.join(BASE_DIR, "c2c-connect.js"), media_type="application/javascript")


@app.get("/healthz")
def health():
    return {"ok": True, "database_connected": airtable_store.configured()}


# ----------------------------------------------------------------------------- student routes

class SignIn(BaseModel):
    student_id: str
    full_name: str
    system: str = "CBT"


class TrainingCompletion(BaseModel):
    student_id: str
    score: float
    track: str
    full_name: str = ""
    system: str = ""


@app.post("/api/register-interest")
def register_interest(payload: dict):
    """Dashboard sign-up form -> 'C2C Sign-Ups' table."""
    ok, status, message = save_signup(payload)
    return JSONResponse({"ok": True} if ok else {"error": message}, status_code=status)


@app.post("/api/register")
def register(data: SignIn):
    """CBT (and other systems') sign-in -> 'Sign-Ins' table."""
    v = require_v(data.student_id)
    name = clean(data.full_name, 120)
    if not name:
        raise HTTPException(status_code=400, detail="Enter your full name.")
    require_storage()
    store(airtable_store.create_record, SIGNINS_TABLE, {
        "V Number": v, "Full Name": name, "System": clean(data.system, 60) or "CBT",
    })
    return {"ok": True, "student_id": v}


@app.post("/api/complete-training")
def complete_training(data: TrainingCompletion):
    """A finished simulation, game or session from any system -> 'Training Results' table."""
    v = require_v(data.student_id)
    track = clean(data.track)
    if not track:
        raise HTTPException(status_code=400, detail="Missing training activity name.")
    if not 0 <= data.score <= 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100.")
    require_storage()
    store(airtable_store.create_record, RESULTS_TABLE, {
        "V Number": v,
        "Full Name": clean(data.full_name, 120),
        "System": system_for(track, data.system),
        "Activity": track,
        "Score": round(data.score, 1),
    })
    return {"ok": True}


@app.get("/api/training-logs")
def training_logs(student_id: str = Query(default=""), x_admin_key: str = Header(default="")):
    """With ?student_id=V00…: that student's own results (used by CBT to restore progress).
    Without it: every result, for the admin portal only."""
    require_storage()
    if student_id:
        v = require_v(student_id)
        rows = store(airtable_store.list_records, RESULTS_TABLE, f"{{V Number}}='{v}'")
        return [{k: row[k] for k in ("student_id", "track", "score", "timestamp")} for row in map(result_row, rows)]
    require_admin(x_admin_key)
    return [result_row(r) for r in store(airtable_store.list_records, RESULTS_TABLE)]


# ----------------------------------------------------------------------------- AR reports
# Summary data for the AR data visualization site, in its CSV format. No names or V#s.

_report_cache = {"at": 0.0, "results": []}


def recent_results():
    """All training results, cached for a minute so a busy AR page doesn't hit Airtable limits."""
    if time.time() - _report_cache["at"] > 60:
        _report_cache["results"] = [result_row(r) for r in store(airtable_store.list_records, RESULTS_TABLE)]
        _report_cache["at"] = time.time()
    return _report_cache["results"]


SYSTEMS = ["CBT", "3D Simulation", "VR Cleanroom", "AR Data Visualization", "Physical Equipment"]


def activity_csv(results):
    today = datetime.now(timezone.utc).date()
    counts = {s: [0] * 30 for s in SYSTEMS}
    for r in results:
        try:
            day = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")).date()
        except ValueError:
            continue
        ago = (today - day).days
        if 0 <= ago < 30 and r["system"] in counts:
            counts[r["system"]][29 - ago] += 1
    used = [s for s in SYSTEMS if any(counts[s])] or ["CBT"]
    lines = [
        "# type: series   # title: C2C Training Completions (last 30 days)   # category: quality",
        "# x: Day (0 = today)   # y: Completions",
        "# description: Training sessions completed per day in each C2C system. Live from the C2C Airtable base.",
        "# source: C2C training server",
        "Day," + ",".join(used),
    ]
    for i in range(30):
        lines.append(f"{i - 29}," + ",".join(str(counts[s][i]) for s in used))
    return "\n".join(lines) + "\n"


def scores_csv(results):
    scores = [r["score"] for r in reversed(results) if isinstance(r["score"], (int, float))][-200:]
    lines = [
        "# type: spc   # title: C2C Training Scores   # category: quality",
        "# quantity: Score   # unit: %   # target: 100   # lsl: 70   # usl: 100",
        "# description: Scores of the most recent training sessions across all C2C systems, oldest to newest. 70% is the passing line.",
        "# source: C2C training server",
        "score",
    ] + [str(round(s, 1)) for s in scores]
    return "\n".join(lines) + "\n"


@app.get("/api/reports/index.json")
def reports_index():
    require_storage()
    results = recent_results()
    names = ["c2c_training_activity.csv"]
    if sum(isinstance(r["score"], (int, float)) for r in results) >= 8:
        names.append("c2c_training_scores.csv")  # the control chart needs at least 8 scores
    return names


@app.get("/api/reports/{name}")
def report(name: str):
    require_storage()
    results = recent_results()
    if name == "c2c_training_activity.csv":
        return PlainTextResponse(activity_csv(results), media_type="text/csv")
    if name == "c2c_training_scores.csv":
        return PlainTextResponse(scores_csv(results), media_type="text/csv")
    raise HTTPException(status_code=404, detail="No such report.")


# ----------------------------------------------------------------------------- admin routes

def all_students():
    """One row per student, combining sign-ups and sign-ins (newest activity first)."""
    people = {}
    for r in store(airtable_store.list_records, SIGNUPS_TABLE):
        f = r.get("fields", {})
        v = f.get("V Number")
        if v and v not in people:
            people[v] = {
                "student_id": v,
                "full_name": f"{f.get('First Name', '')} {f.get('Last Name', '')}".strip(),
                "email": f.get("Email", ""),
                "classification": f.get("Classification", ""),
                "interests": ", ".join(f.get("Interests", []) or []),
                "signed_up": r.get("createdTime", ""),
                "last_sign_in": "",
            }
    for r in store(airtable_store.list_records, SIGNINS_TABLE):
        f = r.get("fields", {})
        v = f.get("V Number")
        if not v:
            continue
        p = people.setdefault(v, {
            "student_id": v, "full_name": f.get("Full Name", ""), "email": "", "classification": "",
            "interests": "", "signed_up": "", "last_sign_in": "",
        })
        if not p["last_sign_in"]:
            p["last_sign_in"] = r.get("createdTime", "")  # records arrive newest first
    return sorted(people.values(), key=lambda p: max(p["signed_up"], p["last_sign_in"]), reverse=True)


@app.get("/api/students")
def get_students(x_admin_key: str = Header(default="")):
    require_admin(x_admin_key)
    require_storage()
    return all_students()


@app.get("/api/export-csv")
def export_csv(x_admin_key: str = Header(default="")):
    require_admin(x_admin_key)
    require_storage()
    students = all_students()
    results = [result_row(r) for r in store(airtable_store.list_records, RESULTS_TABLE)]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Students"])
    writer.writerow(["V Number", "Full Name", "Email", "Classification", "Interests", "Signed Up", "Last Sign-In"])
    for p in students:
        writer.writerow([p["student_id"], p["full_name"], p["email"], p["classification"], p["interests"], p["signed_up"], p["last_sign_in"]])
    writer.writerow([])
    writer.writerow(["Training Results"])
    writer.writerow(["V Number", "Full Name", "System", "Activity", "Score", "Completed"])
    for r in results:
        writer.writerow([r["student_id"], r["full_name"], r["system"], r["track"], r["score"], r["timestamp"]])

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=c2c_training_records.csv"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mainsys:app", host="127.0.0.1", port=8000, reload=True)
