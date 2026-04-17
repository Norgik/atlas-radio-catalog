#!/usr/bin/env python3
"""
Validates remote_catalog.json — every station must have a non-empty `language` field.
Run: python3 validate_catalog.py
Used in CI on every PR to atlas-radio-catalog.
"""
import json
import sys

CATALOG_PATH = "remote_catalog.json"

def main():
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {CATALOG_PATH} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: {CATALOG_PATH} is not valid JSON: {e}")
        sys.exit(1)

    countries = data.get("countries", [])
    total = 0
    missing = []

    for country in countries:
        cc = country.get("countryCode", "?")
        for station in country.get("stations", []):
            total += 1
            lang = str(station.get("language", "")).strip()
            if not lang:
                missing.append({
                    "countryCode": cc,
                    "id": station.get("id", "?"),
                    "name": station.get("name", "?"),
                })

    if missing:
        print(f"ERROR: {len(missing)} station(s) missing non-empty `language` field:\n")
        for s in missing:
            print(f"  [{s['countryCode']}] {s['id']} — {s['name']}")
        print(f"\nTotal checked: {total}")
        sys.exit(1)

    print(f"OK: all {total} stations have a non-empty `language` field.")

if __name__ == "__main__":
    main()
