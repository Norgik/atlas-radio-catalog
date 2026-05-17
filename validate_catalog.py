#!/usr/bin/env python3
"""
Validates remote_catalog.json — every station must have a non-empty `language` field.
Run: python3 validate_catalog.py
Used in CI on every PR to atlas-radio-catalog.
"""
import json
import sys

CATALOG_PATH = "remote_catalog.json"
BULK_FILL_MIN_STATIONS = 5

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
    bulk_warnings = []

    for country in countries:
        cc = country.get("countryCode", "?")
        stations = country.get("stations", [])
        langs = set()
        for station in stations:
            total += 1
            lang = str(station.get("language", "")).strip()
            if not lang:
                missing.append({
                    "countryCode": cc,
                    "id": station.get("id", "?"),
                    "name": station.get("name", "?"),
                })
            else:
                langs.add(lang.lower())

        if len(stations) >= BULK_FILL_MIN_STATIONS and len(langs) == 1:
            only_lang = next(iter(langs))
            bulk_warnings.append((cc, len(stations), only_lang))

    if missing:
        print(f"ERROR: {len(missing)} station(s) missing non-empty `language` field:\n")
        for s in missing:
            print(f"  [{s['countryCode']}] {s['id']} — {s['name']}")
        print(f"\nTotal checked: {total}")
        sys.exit(1)

    print(f"OK: all {total} stations have a non-empty `language` field.")

    if bulk_warnings:
        print(f"\nWARNING: {len(bulk_warnings)} country/countries with a single language for all stations (likely bulk-filled):")
        for cc, n, lang in sorted(bulk_warnings, key=lambda x: x[0]):
            print(
                f"  WARNING: country {cc} has all {n} stations with language {lang!r}, likely bulk-filled"
            )

if __name__ == "__main__":
    main()
