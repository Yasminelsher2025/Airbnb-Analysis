# Airbnb Open Data — Project README

## Overview
This folder contains an exploratory data analysis (EDA) and an interactive Streamlit app built from an Airbnb open dataset.

Key artifacts

- Notebook: `Airbnb_Analysis.ipynb` — full analysis with code and final charts
- Streamlit app: `app.py` — interactive app that reproduces the notebook's final charts
- Cleaned data: `Airbnb_Cleaned.csv` — cleaned dataset used by the notebook and app

## Data Summary
Files in this folder:

- `Airbnb_Open_Data.csv` — original raw download
- `Airbnb_Cleaned.csv` — cleaned, analysis-ready dataset

Common columns (may vary): `id`, `name`, `host_id`, `host_name`, `neighbourhood_group`, `neighbourhood`, `latitude`, `longitude`, `room_type`, `price`, `minimum_nights`, `number_of_reviews`, `last_review`, `reviews_per_month`, `calculated_host_listings_count`, `availability_365`, `review_rate_number`, `service_fee`, `host_identity_verified`, `cancellation_policy`, `instant_bookable`.

Cleaning highlights

- Converted price to numeric and reviewed / filtered obvious outliers
- Handled missing review fields appropriately (filled or excluded)
- Parsed date fields and extracted `year` for trend analysis
- Added derived features: price ranges, review bins, and categorical groupings

## Notebook — High-level Steps
1. Imports and data loading
2. Data profiling and cleaning
3. Feature engineering (price ranges, review bins, year extraction)
4. Exploratory visualizations (histograms, boxplots, scatterplots)
5. Correlation analysis and heatmaps
6. Analysis questions (Q1–Q12) with final charts

Each analysis question is followed by a short markdown explanation; the Streamlit app mirrors those charts on the "Analysis Questions" page.

## Project Structure
Top-level layout of this folder (key files and folders):

- `app.py` — Streamlit application script (main entry)
- `Airbnb_Analysis.ipynb` — Jupyter notebook with full EDA and chart code
- `Airbnb_Cleaned.csv` — cleaned dataset used by notebook and app
- `Airbnb_Open_Data.csv` — original raw dataset
- `requirements.txt` — pinned Python dependencies
- `README.md` — this document

## Run the Streamlit App (Quick Start)
Create and activate a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```

## Regenerating `app.py` from the Notebook
Execute the notebook cell containing `%%writefile app.py` to overwrite `app.py` with the notebook's current script.

## Files of Interest

- `Airbnb_Analysis.ipynb`
- `app.py`
- `Airbnb_Cleaned.csv`
- `requirements.txt`


---
Generated: 2026-02-13
