"""
calendar_builder.py

Builds agricultural calendar records from one
entity JSON file.
"""

import re

from stage_mapper import (
    normalize_stage,
    normalize_state,
    normalize_weather,
    normalize_recommendation,
    normalize_keywords
)


# --------------------------------------------------
# Helper
# --------------------------------------------------

def first_entity(entities, label):
    """
    Returns first entity of requested label.
    """
    for entity in entities:
        if entity.get("label") == label:
            return entity.get("text", "")
    return ""


def all_entities(entities, label):
    """
    Returns all entities of requested label.
    """

    values = []
    seen = set()

    for entity in entities:

        if entity.get("label") != label:
            continue

        value = entity.get("text", "").strip()

        if not value:
            continue

        key = value.lower()

        if key in seen:
            continue

        seen.add(key)

        values.append(value)

    return values


# --------------------------------------------------
# Recommendation Extraction
# --------------------------------------------------

ADVISORY_PATTERNS = [

    r"recommended.*?\.",
    r"advised.*?\.",
    r"should.*?\.",
    r"apply.*?\.",
    r"avoid.*?\.",
    r"maintain.*?\.",
    r"irrigat.*?\.",
    r"spray.*?\.",
    r"monitor.*?\.",
    r"store.*?\."

]


def extract_advisory(text):

    if not text:
        return "No Advisory"

    for pattern in ADVISORY_PATTERNS:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return normalize_recommendation(
                match.group(0)
            )

    return "No Advisory"


# --------------------------------------------------
# Report Date Extraction
# --------------------------------------------------

def extract_report_date(text):

    if not text:
        return ""

    patterns = [

        r"as\s+on\s+(\d{2}[./-]\d{2}[./-]\d{4})",

        r"\(as\s+on\s+(\d{2}[./-]\d{2}[./-]\d{4})\)",

        r"(\d{2}[./-]\d{2}[./-]\d{4})"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return ""

# --------------------------------------------------
# Build Calendar Records
# --------------------------------------------------

def build_calendar(entity_document):

    """
    Convert one entity JSON into calendar records.
    """


    chunks = entity_document.get(
        "chunks",
        []
    )

    records = []

    record_id = 1

    for chunk in chunks:

        entities = chunk.get(
            "entities",
            []
        )

        text = chunk.get(
            "text",
            ""
        )

        document_name = chunk.get(
            "source_document",
            "Unknown"
        )
        crops = all_entities(
            entities,
            "Crop"
        )

        states = all_entities(
            entities,
            "State"
        )

        districts = all_entities(
            entities,
            "District"
        )

        weather = all_entities(
            entities,
            "Weather Event"
        )

        rainfall = all_entities(
            entities,
            "Rainfall"
        )

        temperature = all_entities(
            entities,
            "Temperature"
        )

        stages = all_entities(
            entities,
            "Stage"
        )

        dates = all_entities(
            entities,
            "Date"
        )

        if not dates:

            report_date = extract_report_date(text)

            if report_date:

                dates = [report_date]

        # ------------------------------------------
        # If Date entity is missing,
        # extract from chunk text
        # ------------------------------------------

        if not dates:

            report_date = extract_report_date(text)

            if report_date:
                dates = [report_date]

        seasons = all_entities(
            entities,
            "Season"
        )

        recommendation = extract_advisory(text)

        keywords = normalize_keywords(
            chunk.get(
                "keywords",
                []
            )
        )

        # ------------------------------------------
        # Missing Values
        # ------------------------------------------

        if not crops:
            continue

        if not states:
            states = [""]

        if not weather:
            weather = [""]

        if not stages:
            stages = [""]

        if not rainfall:
            rainfall = [""]

        if not temperature:
            temperature = [""]

        if not districts:
            districts = [""]

        if not seasons:
            seasons = [""]

        if not dates:
            dates = [""]

        page = chunk.get(
            "page_start",
            ""
        )

        chunk_id = chunk.get(
            "chunk_id",
            ""
        )

        # ------------------------------------------
        # Build Records
        # ------------------------------------------

        for crop in crops:

            for state in states:

                record = {

                    "record_id": record_id,

                    "report_date": dates[0],

                    "season": seasons[0],

                    "crop": crop,

                    "state": normalize_state(state),

                    "district": districts[0],

                    "weather": normalize_weather(weather[0]),

                    "temperature": temperature[0],

                    "rainfall": rainfall[0],

                    "crop_stage": normalize_stage(stages[0]),

                    "recommendation": recommendation,

                    "keywords": keywords,

                    "source_document": document_name,

                    "chunk_id": chunk_id,

                    "page": page

                }

                records.append(record)

                record_id += 1

    return records