"""
run_calendar.py

Builds one Master Agricultural Calendar
from clean_entities.json
"""

import os
import json
import time

from calendar_builder import build_calendar
from export_calendar import export_all


# =====================================================
# INPUT
# =====================================================

INPUT_FILE = os.path.join(
    "output",
    "entities",
    "clean_entities.json"
)


# =====================================================
# OUTPUT
# =====================================================

OUTPUT_FOLDER = os.path.join(
    "output",
    "calendars"
)

REPORT_FOLDER = os.path.join(
    "output",
    "reports"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)
# =====================================================
# Remove Duplicate Calendar Records
# =====================================================

def remove_duplicates(records):

    unique = []

    seen = set()

    removed = 0

    for record in records:

        key = (

            record.get("crop", "").lower(),

            record.get("state", "").lower(),

            record.get("district", "").lower(),

            record.get("season", "").lower(),

            record.get("crop_stage", "").lower(),

            record.get("weather", "").lower(),

            record.get("recommendation", "").lower()

        )

        if key in seen:

            removed += 1

            continue

        seen.add(key)

        unique.append(record)

    return unique, removed
# =====================================================
# MAIN
# =====================================================

def main():

    start = time.time()

    # -------------------------------------------------
    # Load Clean Entity File
    # -------------------------------------------------

    if not os.path.exists(INPUT_FILE):

        print("\nclean_entities.json not found.")

        return

    with open(

        INPUT_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        entity_document = json.load(f)

    print("\nLoading Clean Entity File...")

    chunks = entity_document.get(

        "chunks",

        []

    )

    print(f"Chunks Loaded : {len(chunks)}")

    # -------------------------------------------------
    # Build Calendar
    # -------------------------------------------------

    print("\nBuilding Agricultural Calendar...")

    records = build_calendar(entity_document)

    before = len(records)

    # -------------------------------------------------
    # Remove Duplicates
    # -------------------------------------------------

    records, duplicates_removed = remove_duplicates(records)

    after = len(records)

    print(f"\nRecords Before Cleaning : {before}")

    print(f"Duplicates Removed      : {duplicates_removed}")

    print(f"Final Records           : {after}")

    # -------------------------------------------------
    # Output Files
    # -------------------------------------------------

    json_file = os.path.join(

        OUTPUT_FOLDER,

        "agricultural_calendar.json"

    )

    csv_file = os.path.join(

        OUTPUT_FOLDER,

        "agricultural_calendar.csv"

    )

    excel_file = os.path.join(

        OUTPUT_FOLDER,

        "agricultural_calendar.xlsx"

    )

    export_all(

        records,

        json_file,

        csv_file,

        excel_file

    )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    crops = set()

    states = set()

    districts = set()

    seasons = set()

    weather = set()

    stages = set()

    for record in records:

        if record["crop"]:
            crops.add(record["crop"])

        if record["state"]:
            states.add(record["state"])

        if record["district"]:
            districts.add(record["district"])

        if record["season"]:
            seasons.add(record["season"])

        if record["weather"]:
            weather.add(record["weather"])

        if record["crop_stage"]:
            stages.add(record["crop_stage"])

    runtime = round(

        time.time() - start,

        2

    )

    report = {

        "chunks_processed": len(chunks),

        "records_before_cleaning": before,

        "duplicates_removed": duplicates_removed,

        "final_records": after,

        "unique_crops": len(crops),

        "unique_states": len(states),

        "unique_districts": len(districts),

        "unique_weather_events": len(weather),

        "unique_crop_stages": len(stages),

        "unique_seasons": len(seasons),

        "processing_time_seconds": runtime

    }

    report_file = os.path.join(

        REPORT_FOLDER,

        "calendar_statistics.json"

    )

    with open(

        report_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            report,

            f,

            indent=4,

            ensure_ascii=False

        )

    # -------------------------------------------------
    # Console Report
    # -------------------------------------------------

    print("\n")

    print("=" * 70)

    print(" MASTER AGRICULTURAL CALENDAR REPORT ")

    print("=" * 70)

    print(f"Chunks Processed        : {len(chunks)}")

    print(f"Records Before Cleaning : {before}")

    print(f"Duplicates Removed      : {duplicates_removed}")

    print(f"Final Calendar Records  : {after}")

    print()

    print(f"Unique Crops            : {len(crops)}")

    print(f"Unique States           : {len(states)}")

    print(f"Unique Districts        : {len(districts)}")

    print(f"Weather Events          : {len(weather)}")

    print(f"Crop Stages             : {len(stages)}")

    print(f"Seasons                 : {len(seasons)}")

    print()

    print(f"Processing Time         : {runtime} sec")

    print("=" * 70)

    print("\nAgricultural Calendar Generated Successfully.")

    print("\nFiles Saved")

    print("-" * 30)

    print(json_file)

    print(csv_file)

    print(excel_file)

    print(report_file)
    
# =====================================================

if __name__ == "__main__":

    main()


# """
# run_calendar.py

# Master Agricultural Calendar Generator

# Pipeline
# --------
# 1. Read all entity JSONs
# 2. Build calendar records
# 3. Merge all records
# 4. Remove duplicates
# 5. Export master calendar
# 6. Generate statistics
# """

# import os
# import json
# import time

# from calendar_builder import build_calendar
# from duplicate_remover import clean_calendar
# from export_calendar import export_all
# from calendar_statistics import (
#     generate_statistics,
#     save_statistics
# )


# # =====================================================
# # INPUT / OUTPUT
# # =====================================================

# INPUT_FOLDER = os.path.join(
#     "output",
#     "entities"
# )

# OUTPUT_FOLDER = os.path.join(
#     "output",
#     "calendars"
# )

# REPORT_FOLDER = os.path.join(
#     "output",
#     "reports"
# )

# os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# os.makedirs(REPORT_FOLDER, exist_ok=True)


# # =====================================================
# # MAIN
# # =====================================================

# def main():

#     start = time.time()

#     files = sorted(

#         f

#         for f in os.listdir(INPUT_FOLDER)

#         if f.endswith(".json")

#     )

#     if not files:

#         print("No entity JSON files found.")

#         return

#     print()

#     print("=" * 70)
#     print("MASTER AGRICULTURAL CALENDAR GENERATION")
#     print("=" * 70)

#     all_records = []

#     reports_processed = 0

#     for file in files:

#         path = os.path.join(
#             INPUT_FOLDER,
#             file
#         )

#         print("\nProcessing:", file)

#         with open(
#             path,
#             "r",
#             encoding="utf-8"
#         ) as f:

#             entity_json = json.load(f)

#         records = build_calendar(entity_json)

#         print("Records:", len(records))

#         all_records.extend(records)

#         reports_processed += 1

#     print()

#     print("Total Records Before Cleaning:",
#           len(all_records))

#     # ----------------------------------------
#     # Remove duplicates
#     # ----------------------------------------

#     cleaned_records, stats = clean_calendar(
#         all_records
#     )

#     print(
#         "Duplicates Removed:",
#         stats["duplicates_removed"]
#     )

#     print(
#         "Final Records:",
#         stats["final_records"]
#     )

#     # ----------------------------------------
#     # Export
#     # ----------------------------------------

#     export_all(
#         cleaned_records,
#         OUTPUT_FOLDER
#     )

#     # ----------------------------------------
#     # Statistics
#     # ----------------------------------------

#     statistics = generate_statistics(
#         cleaned_records,
#         stats["duplicates_removed"]
#     )

#     statistics["reports_processed"] = reports_processed

#     statistics["processing_time_seconds"] = round(

#         time.time() - start,

#         2

#     )

#     save_statistics(

#         statistics,

#         os.path.join(

#             REPORT_FOLDER,

#             "calendar_statistics.json"

#         )

#     )

#     # ----------------------------------------
#     # Console Report
#     # ----------------------------------------

#     print()

#     print("=" * 70)

#     print("MASTER AGRICULTURAL CALENDAR REPORT")

#     print("=" * 70)

#     print(f"Reports Processed      : {reports_processed}")

#     print(f"Records Generated      : {len(all_records)}")

#     print(f"Duplicates Removed     : {stats['duplicates_removed']}")

#     print(f"Final Calendar Records : {stats['final_records']}")

#     print(f"Unique Crops           : {statistics['unique_crops']}")

#     print(f"Unique States          : {statistics['unique_states']}")

#     print(f"Unique Districts       : {statistics['unique_districts']}")

#     print(f"Weather Events         : {statistics['unique_weather_events']}")

#     print(f"Crop Stages            : {statistics['unique_crop_stages']}")

#     print(f"Seasons                : {statistics['unique_seasons']}")

#     print()

#     print(
#         f"Processing Time        : "
#         f"{statistics['processing_time_seconds']} sec"
#     )

#     print("=" * 70)

#     print()

#     print("Agricultural Calendar Generated Successfully.")

#     print()

#     print("Files Saved")

#     print("------------------------------")

#     print(

#         os.path.join(

#             OUTPUT_FOLDER,

#             "agricultural_calendar.json"

#         )

#     )

#     print(

#         os.path.join(

#             OUTPUT_FOLDER,

#             "agricultural_calendar.csv"

#         )

#     )

#     print(

#         os.path.join(

#             OUTPUT_FOLDER,

#             "agricultural_calendar.xlsx"

#         )

#     )

#     print(

#         os.path.join(

#             REPORT_FOLDER,

#             "calendar_statistics.json"

#         )

#     )


# # =====================================================

# if __name__ == "__main__":

#     main()
