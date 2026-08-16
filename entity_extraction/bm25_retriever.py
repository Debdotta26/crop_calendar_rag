"""
bm25_retriever.py

BM25-assisted retrieval for agricultural entity extraction.

BM25 is used to identify the relevance of each chunk
to different agricultural entity categories before GLiNER
performs the actual entity extraction.
"""

import re

from rank_bm25 import BM25Okapi


# =====================================================
# DOMAIN QUERY TERMS
# =====================================================

ENTITY_QUERIES = {

    "Crop": """
        crop rice paddy wheat maize corn cotton soybean
        groundnut mustard gram pulse sugarcane bajra jowar
        millet sesame sunflower potato onion tomato chilli
        turmeric ginger tea coffee coconut banana mango
    """,

    "State": """
        state district region province
        Andhra Pradesh Assam Bihar Gujarat Haryana
        Karnataka Kerala Maharashtra Odisha Punjab Rajasthan
        Tamil Nadu Telangana Uttar Pradesh Uttarakhand
        West Bengal Madhya Pradesh
    """,

    "District": """
        district block subdivision region tehsil mandal
    """,

    "Weather Event": """
        rainfall heavy rain heavy rainfall flood drought
        cyclone storm thunderstorm hailstorm heat wave
        cold wave dry spell strong wind weather
    """,

    "Temperature": """
        temperature maximum minimum hot cold degree Celsius
        heat thermal
    """,

    "Rainfall": """
        rainfall rain precipitation showers heavy rainfall
        millimeter mm deficit excess normal
    """,

    "Season": """
        kharif rabi zaid summer monsoon winter season
    """,

    "Reservoir": """
        reservoir dam water storage storage level
        water availability
    """,

    "River": """
        river basin water level river flow
    """,

    "Pest": """
        pest insect infestation aphid bollworm caterpillar
        stem borer leaf folder whitefly thrips
    """,

    "Disease": """
        disease infection blast rust wilt blight mildew
        rot viral bacterial fungal
    """,

    "Organization": """
        ministry department government organization
        university institute ICAR IMD agriculture
    """,

    "Government Scheme": """
        scheme mission programme program subsidy
        government scheme agriculture support
    """,

    "Month": """
        January February March April May June July August
        September October November December
    """,

    "Date": """
        date day dated as on reported meeting
    """,

    "Year": """
        2020 2021 2022 2023 2024 2025 2026
    """
}


# =====================================================
# TOKENIZER
# =====================================================

def tokenize(text):

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


# =====================================================
# BUILD BM25 INDEX
# =====================================================

def build_bm25_index(chunks):

    corpus = [

        tokenize(
            chunk.get("text", "")
        )

        for chunk in chunks

    ]

    bm25 = BM25Okapi(corpus)

    return bm25


# =====================================================
# GET CATEGORY SCORES
# =====================================================

def get_category_scores(chunks):

    if not chunks:
        return []

    bm25 = build_bm25_index(chunks)

    results = []

    for index, chunk in enumerate(chunks):

        scores = {}

        for label, query in ENTITY_QUERIES.items():

            query_tokens = tokenize(query)

            all_scores = bm25.get_scores(
                query_tokens
            )

            scores[label] = round(
                float(all_scores[index]),
                4
            )

        results.append({

            "chunk_index": index,

            "bm25_scores": scores

        })

    return results


# =====================================================
# GET TOP CATEGORIES FOR A CHUNK
# =====================================================

def get_top_categories(
    bm25_scores,
    top_k=5
):

    sorted_categories = sorted(

        bm25_scores.items(),

        key=lambda x: x[1],

        reverse=True

    )

    return [

        category

        for category, score
        in sorted_categories[:top_k]

        if score > 0

    ]