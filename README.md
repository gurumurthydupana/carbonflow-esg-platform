# CarbonFlow

CarbonFlow is an internship-level, enterprise-inspired ESG emissions platform that ingests operational CSV data, normalizes activity records, estimates CO2e, flags suspicious entries, and supports analyst review with audit trails.

The project is intentionally practical: simple architecture, clean APIs, and realistic governance controls that are easy to explain in interviews.

## Project Overview

- Ingests `SAP`, `Utility`, and `Travel` CSV datasets.
- Preserves both raw and normalized values for traceability.
- Detects suspicious records for analyst review.
- Supports approval/rejection workflows with audit locking.
- Provides dashboard and audit visibility for reporting readiness.

## Architecture Summary

- **Backend:** Django REST Framework monolith with app-based separation:
  - `core`: org + health endpoints
  - `ingestion`: upload + parsing/validation/normalization pipeline
  - `emissions`: records, summaries, and audit log APIs
  - `review`: review queue + approve/reject/lock actions
- **Frontend:** React + Vite single-page app with operational pages for dashboard, ingestion, review, and audit.
- **Data Store:** SQLite by default (PostgreSQL-ready via Django configuration).

## Tech Stack

- Python, Django, Django REST Framework
- SQLite / PostgreSQL
- React, Vite, Tailwind CSS
- Axios, React Router

## Setup Instructions

### 1) Backend

```bash
cd backend
./venv/Scripts/python.exe manage.py migrate
./venv/Scripts/python.exe manage.py runserver
```

Backend runs at `http://127.0.0.1:8000`.

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Seed Data Instructions

Use the demo seed command to prepare recruiter-friendly sample data.

```bash
cd backend
./venv/Scripts/python.exe manage.py seed_demo_data --reset
```

This seeds:
- 1 demo organization
- Plant + airport lookups
- Sample uploads across SAP/Utility/Travel
- Emission records (including suspicious and approved/locked records)
- Audit logs

## Demo Workflow

1. Select the demo organization in the UI.
2. Open **Dashboard** to show total emissions and source/scope breakdowns.
3. Open **Upload CSV** and ingest a sample file.
4. Open **Suspicious Records** to show anomaly detection results.
5. Open **Review Workflow** to approve/reject/lock records.
6. Open **Audit Logs** to show action traceability and governance.

## Screenshots (Placeholders)

- `docs/screenshots/dashboard.png` - Dashboard KPIs and charts
- `docs/screenshots/upload.png` - CSV upload flow
- `docs/screenshots/suspicious-records.png` - Flagged records list
- `docs/screenshots/review-workflow.png` - Approve/reject/lock actions
- `docs/screenshots/audit-logs.png` - Audit history

## API Overview

Base URL: `http://127.0.0.1:8000/api`

- `GET /core/health/` - service health check
- `GET /core/organizations/` - list organizations
- `GET /ingestion/uploads/` - list uploads
- `POST /ingestion/uploads/csv/` - upload and process CSV
- `GET /emissions/records/` - list emission records (supports suspicious filter)
- `GET /emissions/summary/` - aggregated emissions metrics
- `GET /emissions/audit-logs/` - audit trail listing
- `GET /review/queue/` - pending suspicious review queue
- `POST /review/records/{id}/approve/` - approve record
- `POST /review/records/{id}/reject/` - reject record
- `POST /review/records/{id}/lock/` - lock record for audit integrity

## Key Enterprise Features

- Multi-source ingestion pipeline with source-specific parsing.
- Validation + normalization with preserved provenance.
- Suspicious record detection for risk-focused QA.
- Structured analyst review workflow.
- Audit logging and record locking for governance.
- Clear API boundaries and maintainable app-level separation.

## Interview Talking Points

- **Why this project matters:** ESG reporting requires traceable and reviewable data, not just dashboards.
- **Engineering trade-offs:** Built as a pragmatic monolith to reduce complexity while preserving enterprise patterns.
- **Data quality focus:** Raw vs normalized preservation enables debugging and defensible reporting.
- **Governance mindset:** Review states, lock controls, and audit logs mirror real compliance workflows.
- **Scalability path:** App boundaries and API design allow gradual hardening (Postgres, auth, async) without redesign.
