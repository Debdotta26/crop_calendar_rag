"""
duplicate_remover.py

Removes duplicate calendar records.
"""

from copy import deepcopy


# ---------------------------------------------------------
# Normalize Value
# ---------------------------------------------------------

def normalize(value):

    if value is None:
        return ""

    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)

    return str(value).strip().lower()


# ---------------------------------------------------------
# Create Duplicate Key
# ---------------------------------------------------------

def create_key(record):

    """
    Two records are considered duplicates if they
    describe the same advisory for the same crop,
    state and date.
    """

    return (

        normalize(record.get("report_date")),

        normalize(record.get("crop")),

        normalize(record.get("state")),

        normalize(record.get("district")),

        normalize(record.get("weather")),

        normalize(record.get("crop_stage")),

        normalize(record.get("recommendation"))

    )


# ---------------------------------------------------------
# Remove Duplicates
# ---------------------------------------------------------

def remove_duplicates(records):

    """
    Remove duplicate calendar records.
    """

    unique = []

    seen = set()

    removed = 0

    for record in records:

        key = create_key(record)

        if key in seen:

            removed += 1

            continue

        seen.add(key)

        unique.append(deepcopy(record))

    return unique, removed


# ---------------------------------------------------------
# Sort Calendar
# ---------------------------------------------------------

def sort_calendar(records):

    """
    Sort by

    Date

    Crop

    State
    """

    records.sort(

        key=lambda r: (

            normalize(r.get("report_date")),

            normalize(r.get("crop")),

            normalize(r.get("state"))

        )

    )

    return records


# ---------------------------------------------------------
# Final Processing
# ---------------------------------------------------------

def clean_calendar(records):

    """
    Remove duplicates and sort records.
    """

    unique_records, duplicates_removed = remove_duplicates(records)

    unique_records = sort_calendar(unique_records)

    return unique_records, {

        "duplicates_removed": duplicates_removed,

        "final_records": len(unique_records)

    }