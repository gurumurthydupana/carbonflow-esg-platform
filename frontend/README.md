# CarbonFlow Frontend

React + Vite frontend for the CarbonFlow ESG emissions platform.

## Demo Flow (Recruiter-Friendly)

### 1) Quick Setup (3-5 minutes)

1. Start backend:
   - `cd backend`
   - `./venv/Scripts/python.exe manage.py migrate`
   - `./venv/Scripts/python.exe manage.py seed_demo_data --reset`
   - `./venv/Scripts/python.exe manage.py runserver`
2. Start frontend in a new terminal:
   - `cd frontend`
   - `npm install`
   - `npm run dev`
3. Open `http://localhost:5173`.

### 2) Live Demo Workflow

1. Select `Acme Manufacturing` in the organization dropdown.
2. Open **Dashboard** and explain:
   - total CO2e,
   - emissions by scope/source,
   - suspicious count.
3. Open **Upload CSV** and upload a sample SAP/Utility/Travel CSV.
4. Open **Suspicious Records** to show flagged anomalies.
5. Open **Review Workflow** and approve/reject/lock a suspicious record.
6. Open **Audit Logs** to show immutable action history.

### 3) Interview Presentation Order (Suggested Script)

1. **Problem framing (20-30 sec):** ESG data is fragmented and needs traceable ingestion + review.
2. **Architecture (30-45 sec):** DRF backend + React frontend, monolithic and practical for fast delivery.
3. **Ingestion pipeline (45-60 sec):** CSV parser -> validation -> normalization -> suspicious detection -> emissions estimation.
4. **Governance controls (45-60 sec):** analyst review workflow, approval/rejection, audit locking, full audit trail.
5. **Business value (20-30 sec):** cleaner reporting readiness, explainable records, and interview-ready enterprise patterns.
