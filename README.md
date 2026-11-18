# C2C

Classroom to Cleanroom (C2C) training system by Operation SEMI (VSU), NSF Award #2606117.

| Page | Address on the server | File |
|---|---|---|
| Dashboard | `/` | `index.html` |
| CBT portal (simulations + matching game) | `/cbt` | `cbt.html` |
| Admin portal (password protected) | `/admin` | `admin.html` |

`mainsys.py` is the server. It stores every sign-up, sign-in and training result in **Airtable**.
GitHub Pages (`arcchatbot.github.io/C2C`) can show the pages but cannot run the server, so nothing is
saved there. Use the Render address for live training.

## 1. Airtable

Create one base with these three tables. Field names must match exactly.

**C2C Sign-Ups** (dashboard sign-up form)

| Field | Type |
|---|---|
| V Number | Single line text |
| First Name | Single line text |
| Last Name | Single line text |
| Email | Email |
| Classification | Single select |
| Interests | Multiple select |

**Sign-Ins** (every CBT sign-in)

| Field | Type |
|---|---|
| V Number | Single line text |
| Full Name | Single line text |
| System | Single select |

**Training Results** (every finished simulation, game or session, from any system)

| Field | Type |
|---|---|
| V Number | Single line text |
| Full Name | Single line text |
| System | Single select |
| Activity | Single line text |
| Score | Number (1 decimal) |

Select options are created automatically. Optionally add a **Created time** field to each table to see
when rows arrived in Airtable itself; the admin portal already shows the time.

Then create a personal access token at https://airtable.com/create/tokens with the scopes
`data.records:read` and `data.records:write`, limited to this base only.

## 2. Render

Render dashboard → **New → Blueprint** → choose this repo. `render.yaml` sets everything up and asks for:

| Setting | Value |
|---|---|
| `AIRTABLE_TOKEN` | the token from step 1 |
| `AIRTABLE_BASE_ID` | from the base's URL; starts with `app` |
| `ADMIN_PASSWORD` | a password for the admin portal; share it only with instructors |

Never put these values in a page or commit them to GitHub.

Optional: `AIRTABLE_SIGNUPS_TABLE`, `AIRTABLE_SIGNINS_TABLE`, `AIRTABLE_RESULTS_TABLE` if your tables have
different names, and `ALLOWED_ORIGINS` (comma-separated) to let apps on other addresses send results.

Check it works: open `https://<your-service>.onrender.com/healthz`. It should say
`"database_connected": true`.

## 3. Sending results from other systems (VR, 3D, AR)

Any system can save a result with one request to the Render server:

```
POST https://<your-service>.onrender.com/api/complete-training
Content-Type: application/json

{ "student_id": "V00123456", "full_name": "First Last", "system": "VR Cleanroom",
  "track": "VR Gowning Protocol", "score": 100 }
```

Use `system` values `CBT`, `3D Simulation`, `VR Cleanroom`, `AR Data Visualization` or
`Physical Equipment` so the admin portal counts them correctly. Apps hosted on another address must be
listed in `ALLOWED_ORIGINS`.

## API

| Route | Who | Purpose |
|---|---|---|
| `POST /api/register-interest` | Dashboard | Save a sign-up |
| `POST /api/register` | CBT | Record a sign-in |
| `POST /api/complete-training` | Any system | Save a training result |
| `GET /api/training-logs?student_id=V00…` | CBT | One student's own results |
| `GET /api/training-logs` | Admin (password) | All results |
| `GET /api/students` | Admin (password) | All students |
| `GET /api/export-csv` | Admin (password) | Download everything as CSV |
| `GET /healthz` | Anyone | Server and database status |

Student IDs must be `V00` followed by 6 numbers.

## Run locally

```
pip install -r requirements.txt
AIRTABLE_TOKEN=... AIRTABLE_BASE_ID=... ADMIN_PASSWORD=... uvicorn mainsys:app --reload
```
