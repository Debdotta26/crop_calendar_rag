"""
stage_mapper.py

Normalizes:
1. Crop Stages
2. Weather Events
3. State Names
4. Recommendations
5. Keywords
"""

import re


# =====================================================
# Crop Stage Mapping
# =====================================================

STAGE_MAPPING = {

    "sowing": "Sowing",
    "seeding": "Sowing",
    "transplanting": "Transplanting",
    "nursery": "Nursery",

    "vegetative": "Vegetative",
    "germination": "Germination",

    "flowering": "Flowering",
    "heading": "Flowering",
    "fruiting": "Fruiting",

    "grain filling": "Grain Filling",
    "pod filling": "Pod Filling",

    "harvesting": "Harvesting",
    "harvest": "Harvesting",

    "storage": "Storage",

    "post harvest": "Post Harvest",

    "maturity": "Maturity",

    "ripening": "Ripening"
}


# =====================================================
# Weather Mapping
# =====================================================

WEATHER_MAPPING = {

    "heat wave": "Heat Wave",

    "cold wave": "Cold Wave",

    "heavy rainfall": "Heavy Rainfall",

    "rainfall": "Rainfall",

    "light rainfall": "Light Rainfall",

    "dry weather": "Dry Weather",

    "western disturbance": "Western Disturbance",

    "cyclone": "Cyclone",

    "cyclonic circulation": "Cyclonic Circulation",

    "thunderstorm": "Thunderstorm",

    "hailstorm": "Hailstorm",

    "fog": "Fog",

    "monsoon": "Monsoon"
}


# =====================================================
# State Mapping
# =====================================================

STATE_MAPPING = {

    "up": "Uttar Pradesh",
    "uttar pradesh": "Uttar Pradesh",

    "mp": "Madhya Pradesh",
    "madhya pradesh": "Madhya Pradesh",

    "tn": "Tamil Nadu",
    "tamil nadu": "Tamil Nadu",

    "wb": "West Bengal",
    "west bengal": "West Bengal",

    "odisha": "Odisha",
    "orissa": "Odisha",

    "jk": "Jammu and Kashmir",
    "j&k": "Jammu and Kashmir"
}


# =====================================================
# Normalize Text
# =====================================================

def normalize_text(text):

    if text is None:
        return ""

    text = str(text).strip()

    text = re.sub(r"\s+", " ", text)

    return text


# =====================================================
# Crop Stage
# =====================================================

def normalize_stage(stage):

    stage = normalize_text(stage).lower()

    if not stage:
        return ""

    stage = stage.replace(" stage", "")

    stage = stage.replace("-", " ")

    stage = stage.strip()

    if stage in STAGE_MAPPING:
        return STAGE_MAPPING[stage]

    return stage.title()


# =====================================================
# Weather
# =====================================================

def normalize_weather(weather):

    weather = normalize_text(weather).lower()

    if not weather:
        return ""

    weather = weather.replace("-", " ")

    weather = weather.strip()

    if weather in WEATHER_MAPPING:
        return WEATHER_MAPPING[weather]

    return weather.title()


# =====================================================
# State
# =====================================================

def normalize_state(state):

    state = normalize_text(state).lower()

    if not state:
        return ""

    if state in STATE_MAPPING:
        return STATE_MAPPING[state]

    return state.title()


# =====================================================
# Recommendation Cleaner
# =====================================================

def normalize_recommendation(text):

    text = normalize_text(text)

    if not text:
        return ""

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# Keyword Cleaner
# =====================================================

def normalize_keywords(keywords):

    if not keywords:
        return []

    if isinstance(keywords, str):
        keywords = [keywords]

    cleaned = []

    seen = set()

    for word in keywords:

        word = normalize_text(word)

        if len(word) < 3:
            continue

        key = word.lower()

        if key in seen:
            continue

        seen.add(key)

        cleaned.append(word)

    return cleaned