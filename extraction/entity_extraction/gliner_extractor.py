"""
gliner_extractor.py

Hybrid GLiNER Entity Extractor

Features
--------
✓ Loads GLiNER only once
✓ Uses custom agricultural labels
✓ Confidence threshold
✓ Returns structured entities
"""

from gliner import GLiNER

# -------------------------------------------------
# Load Model (only once)
# -------------------------------------------------

MODEL_NAME = "urchade/gliner_medium-v2.1"

print("Loading GLiNER model...")

model = GLiNER.from_pretrained(MODEL_NAME)

print("GLiNER loaded successfully.\n")

# -------------------------------------------------
# Domain Labels
# -------------------------------------------------

LABELS = [

    "Crop",

    "State",

    "District",

    "Weather Event",

    "Temperature",

    "Rainfall",

    "Season",

    "Reservoir",

    "River",

    "Pest",

    "Disease",

    "Organization",

    "Government Scheme",

    "Month",

    "Date",

    "Year"

]

# -------------------------------------------------
# Confidence Threshold
# -------------------------------------------------

THRESHOLD = 0.50

# -------------------------------------------------
# Entity Extraction
# -------------------------------------------------

def extract_entities(text):

    """
    Extract entities from a text chunk.
    """

    if not text.strip():
        return []

    predictions = model.predict_entities(

        text,

        LABELS,

        threshold=THRESHOLD

    )

    entities = []

    seen = set()

    for entity in predictions:

        entity_text = entity["text"].strip()

        label = entity["label"]

        score = round(entity["score"], 4)

        key = (

            entity_text.lower(),

            label

        )

        if key in seen:
            continue

        seen.add(key)

        entities.append({

            "text": entity_text,

            "label": label,

            "score": score

        })

    return entities