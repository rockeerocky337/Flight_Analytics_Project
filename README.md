# Air Tracker - Flight Analytics

Recovered from:
- `rockeerocky337/Flight_Analytics_Project` — Streamlit application
- `rockeerocky337/assignment_1` — CSV dataset and Excel project file

## Data recovered
- `flights.csv` — 300 flight records
- `aircraft.csv`
- `airport_delays.csv`
- `India_Airports_10_Domestic_5_International.csv` (use as `airport.csv`)

## Important fixes
The original `app.py` used `mysql.connector` without importing it and called `.dispose()` on a MySQL connector. These issues are corrected in the new `app.py`.

## Run order
1. Download the four CSV files from the `assignment_1` repository.
2. Save them under `data/`, renaming the airport file to `airport.csv`.
3. Run `sql/01_create_database.sql` in MySQL Workbench.
4. Run `sql/02_load_data.sql` after correcting the CSV folder path.
5. Run `sql/03_analysis_queries.sql` to validate the database.
6. Create `.streamlit/secrets.toml` using `secrets.toml.example`.
7. Install packages: `pip install -r requirements.txt`
8. Start dashboard: `streamlit run app.py`

## Security
A MySQL password was present in the old `test_mysql.py`. Do not reuse or commit that password. Change/rotate it in MySQL and keep credentials only in `.streamlit/secrets.toml`.
