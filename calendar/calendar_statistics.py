"""
calendar_statistics.py

Generates statistics for the
Master Agricultural Calendar.
"""

import json
from collections import Counter


# ---------------------------------------------------------
# Count Unique Values
# ---------------------------------------------------------

def unique_values(records, field):

    values = set()

    for record in records:

        value = record.get(field, "")

        if isinstance(value, list):

            for item in value:

                if str(item).strip():

                    values.add(str(item).strip())

        else:

            if str(value).strip():

                values.add(str(value).strip())

    return values


# ---------------------------------------------------------
# Top Frequent Values
# ---------------------------------------------------------

def top_values(records, field, top_n=20):

    counter = Counter()

    for record in records:

        value = record.get(field, "")

        if isinstance(value, list):

            counter.update(value)

        elif value:

            counter.update([value])

    return counter.most_common(top_n)


# ---------------------------------------------------------
# Generate Statistics
# ---------------------------------------------------------

def generate_statistics(records, duplicates_removed):

    stats = {

        "total_records": len(records),

        "duplicates_removed": duplicates_removed,

        "unique_crops": len(unique_values(records, "crop")),

        "unique_states": len(unique_values(records, "state")),

        "unique_districts": len(unique_values(records, "district")),

        "unique_weather_events": len(unique_values(records, "weather")),

        "unique_crop_stages": len(unique_values(records, "crop_stage")),

        "unique_seasons": len(unique_values(records, "season")),

        "recommendations": sum(
            1
            for r in records
            if r.get("recommendation")
            and r["recommendation"] != "No Advisory"
        ),

        "top_crops": top_values(records, "crop"),

        "top_states": top_values(records, "state"),

        "top_weather": top_values(records, "weather")

    }

    return stats


# ---------------------------------------------------------
# Save Statistics
# ---------------------------------------------------------

def save_statistics(stats, output_file):

    with open(

        output_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            stats,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("Statistics Saved :", output_file)