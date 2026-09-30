"""
AeroDataBox API - Flight Data Extraction

This script demonstrates how to extract flight information
from AeroDataBox without storing the API key in source code.

API key must be supplied through the AERODATABOX_API_KEY
environment variable.
"""

import json
import os
from pathlib import Path

import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = (
    "https://aerodatabox.p.rapidapi.com/"
    "flights/airports/iata/DEL/2026-09-30T00:00/"
    "2026-09-30T23:59"
)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "aerodatabox_flights.json"


# ============================================================
# API EXTRACTION FUNCTION
# ============================================================

def fetch_flight_data():
    """Fetch flight data from AeroDataBox."""

    api_key = os.getenv("AERODATABOX_API_KEY")

    if not api_key:
        raise RuntimeError(
            "AERODATABOX_API_KEY is not set. "
            "Please configure your API key before running this script."
        )

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# SAVE JSON DATA
# ============================================================

def save_json(data):
    """Save extracted API data as a JSON file."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("Flight data saved successfully.")
    print(f"Output file: {OUTPUT_FILE}")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """Run the AeroDataBox extraction process."""

    print("=" * 60)
    print("AERODATABOX FLIGHT DATA EXTRACTION")
    print("=" * 60)

    try:
        data = fetch_flight_data()
        save_json(data)

        print()
        print("API extraction completed successfully.")

    except requests.exceptions.RequestException as error:
        print()
        print("API request failed.")
        print(f"Error: {error}")

    except RuntimeError as error:
        print()
        print("Configuration error.")
        print(f"Error: {error}")

    except Exception as error:
        print()
        print("Unexpected error.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()