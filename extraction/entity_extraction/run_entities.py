"""
run_entities.py

Runs Hybrid GLiNER Entity Extraction
for all chunked documents.

Pipeline
--------
Chunks
   ↓
GLiNER
   ↓
Post Processing
   ↓
Validation
   ↓
Save Updated Chunks
   ↓
Statistics Report
"""

import os
import json
import time

from gliner_extractor import extract_entities
from entity_postprocessor import postprocess_entities
from entity_validator import validate_entities
from entity_statistics import (
    generate_statistics,
    print_statistics,
    save_statistics
)


# -------------------------------------------------
# INPUT / OUTPUT
# -------------------------------------------------

INPUT_FOLDER = os.path.join(
    "output",
    "chunks"
)

OUTPUT_FOLDER = os.path.join(
    "output",
    "entities"
)

REPORT_FOLDER = os.path.join(
    "output",
    "reports"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# -------------------------------------------------
# Process One Document
# -------------------------------------------------

def process_document(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        document = json.load(f)

    print("\n----------------------------------")
    print("Processing:", document["metadata"]["document_name"])
    print("----------------------------------")

    total_entities = 0

    for chunk in document["chunks"]:

        text = chunk.get("text", "")

        entities = extract_entities(text)

        entities = postprocess_entities(
            entities
        )

        entities, stats = validate_entities(
            entities
        )

        chunk["entities"] = entities

        total_entities += len(entities)

    print("Chunks:", len(document["chunks"]))

    print("Entities:", total_entities)

    outfile = os.path.join(

        OUTPUT_FOLDER,

        os.path.basename(filepath)

    )

    with open(

        outfile,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            document,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("Saved:", outfile)

    return document


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    start = time.time()

    files = [

        f

        for f in os.listdir(INPUT_FOLDER)

        if f.endswith(".json")

    ]

    if not files:

        print("No chunk files found.")

        return

    all_documents = []

    for file in files:

        document = process_document(

            os.path.join(

                INPUT_FOLDER,

                file

            )

        )

        all_documents.append(document)

    stats = generate_statistics(

        all_documents

    )

    runtime = round(

        time.time() - start,

        2

    )

    stats["processing_time_seconds"] = runtime

    print_statistics(stats)

    report_path = save_statistics(

        stats,

        REPORT_FOLDER

    )

    print()

    print("Statistics Saved Successfully.")

    print(report_path)

    print()

    print("Hybrid Entity Extraction Completed Successfully.")


# -------------------------------------------------

if __name__ == "__main__":

    main()