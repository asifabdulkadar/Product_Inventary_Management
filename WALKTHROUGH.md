# Project walkthrough — Flask Inventory Management

This file is a short guide you can use to walk an interviewer through the codebase, run the app locally, seed data, and point out where changes would be made.

1) Quick elevator pitch
- Small Flask application for managing products, locations and inventory movements.
- SQLite by default, SQLAlchemy ORM, Jinja2 templates, and a simple balance-report SQL for inventory per product/location.

2) Key files and responsibilities
- `app.py` — Flask application routes, CRUD views for products, locations, movements, and report endpoint.
- `models.py` — SQLAlchemy models: `Product`, `Location`, `ProductMovement`, and `db` initialization.
- `config.py` — Application configuration and `DATABASE_URL` handling.
- `seed.py` — Script to drop/create schema and populate sample data (use to demo behavior quickly).
- `templates/` — Jinja2 templates grouped by feature (products, locations, movements, reports).
- `tests/test_balances.py` — Minimal pytest that asserts the balance SQL calculation.
- `requirements.txt` / `requirements-dev.txt` — pinned runtime/development dependencies.

3) How to run locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional for running tests
python seed.py  # creates app.db and sample data
python app.py

# Visit http://127.0.0.1:5000
```

4) How to run tests

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

5) Demo plan (5–10 minutes)
- Open `app.py`, show route structure for products, locations, movements.
- Open `models.py` and explain why `from_location`/`to_location` are nullable and how movement types (in/out/transfer) are represented.
- Run `seed.py` and then open the app in browser; show adding a product and recording a movement.
- Navigate to `/reports/balances` to show the grid of balances; open the SQL in `app.py` and explain logic.

6) Common follow-up change requests (be ready to discuss)
- Add authentication and per-user auditing (where to add models and middleware).
- Add CSRF protection (use Flask-WTF's CSRFProtect and add tokens to templates).
- Replace text primary keys with integer autoincrement keys (or add surrogate keys while preserving user-friendly IDs).
- Add pagination and API endpoints (where to add and how to version).

7) Code locations for likely edits
- Validation and forms: update templates and `app.py` routes; consider adding `forms.py` with WTForms.
- Transactions for movement operations: wrap `db.session` changes in `session.begin()` in `app.py`.
- Add unit tests: create new tests under `tests/` mocking small datasets and asserting expected behavior.

8) Troubleshooting
- If the app fails to start because of dependency mismatch, ensure pinned versions are installed from `requirements.txt` (notably Flask 2.2.x is used here).
- Use `DATABASE_URL` env var for non-default DBs.

9) Closing notes
- The project is intentionally minimal to keep it interview friendly. Focus on explaining tradeoffs and where you'd make production hardening changes.
