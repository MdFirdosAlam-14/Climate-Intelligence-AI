# Secure Climate Intelligence & Smart Agriculture Research Platform

An upgraded Streamlit application based on the original Weather & Climate Analyzer. The existing weather, climate trend, ML, anomaly, blockchain-ledger and security modules are retained, with a redesigned left-sidebar workspace and agriculture/research sections.

## Main workspace

- **Overview** — climate snapshot, live indicators, forecast and threshold flags.
- **Live Weather** — current conditions, 7-day meteorological forecast and AQI.
- **Smart Agriculture** — transparent weather/season-based crop screening for field crops, vegetables and fruits.
- **Crop Calendar** — indicative monthly crop windows.
- **Climate Research** — annual temperature/rainfall summaries, hot-day counts, Mann–Kendall test and Sen slope.
- **AI / ML Lab** — time-ordered holdout comparison, persistence baseline, regression models, recursive experimental forecast and rainfall classification.
- **Anomaly Detection** — Isolation Forest screening.
- **Blockchain Ledger** — local SHA-256 hash-linked snapshot ledger and tamper demonstration.
- **Security & Audit** — SQLite authentication, password hashing, failed-login lockout and admin-only audit history.
- **Research Export** — download daily data, annual summary and a methods/limitations research note.

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

First-run demo admin: `admin / Admin@123`. Change this before using the app beyond a local demonstration. New accounts can be registered from the login screen.

## Data sources

The application retrieves geocoding, historical daily weather, forecast and air-quality data from Open-Meteo services. An internet connection is required. API availability, coverage and revisions can affect outputs.

## Important research and agriculture limitations

- Crop suitability scores are heuristic screening scores based on current temperature, humidity, seven-day forecast rainfall and month. They are **not** probabilities, yield forecasts or agronomic prescriptions.
- The crop calendar contains broad illustrative month windows, not district- and variety-specific sowing advisories.
- Soil pH, NPK, organic carbon, soil moisture, irrigation infrastructure, variety, local pest pressure and validated ICAR/SAU advisories are not yet integrated.
- The recursive ML temperature forecast is an experiment based on historical temperatures; it is not the meteorological forecast and is not suitable for warnings or operational decisions.
- Trend tests are exploratory. Serial dependence, missing observations, station/grid representation and period selection affect inference. A detected trend is not causal attribution.
- Isolation Forest flags unusual observations; it does not prove that a value is erroneous or a climate extreme.
- The ledger is a local tamper-evident demonstration, not a distributed public blockchain.
- The local SQLite authentication layer is suitable for a prototype, not production deployment without a security review, secrets management, HTTPS and operational controls.

## Project files

- `app.py` — Streamlit UI and page navigation
- `data.py` — Open-Meteo API and location helpers
- `crops.py` — crop catalogue and screening score
- `ml.py` — trend, regression, classification and anomaly methods
- `security.py` — local authentication and audit logging
- `chain.py` — local hash-linked data snapshot ledger
- `requirements.txt` — Python dependencies

The app creates `app.db` and `chain.json` locally at runtime. Keep these files backed up if you need to retain local users, audit history or ledger entries.
