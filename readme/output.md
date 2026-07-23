# 🌾 India Crop Calendar Dataset

This repository contains the structured outputs generated from the AI-powered agricultural information extraction pipeline.

The dataset is created from Crop Weather Watch Group (CWWG) reports published by the Department of Agriculture & Farmers Welfare, Government of India.

---

# Dataset Contents

```
output/

├── entities/
│      52 json files...
│      merged_entities.json
│      clean_entities.json
│
├──chunks/
│      52 json files...
│ 
├── calendars/
│      agricultural_calendar.json
│      agricultural_calendar.csv
│
├── reports/
│      entity_cleaning_report.json
│      calendar_statistics.json
│      chunking_report.json
```

---

# Dataset Pipeline

```
PDF Reports
      │
      ▼
Text Extraction
      │
      ▼
Entity Extraction
      │
      ▼
Entity Cleaning
      │
      ▼
Calendar Generation
      │
      ▼
Statistics & Validation
```

---

# Files Description

## merged_entities.json

Contains raw entities extracted from every document chunk before cleaning.

Includes

- Crop
- State
- District
- Weather Event
- Season
- Recommendation
- Pest
- Disease
- Organization
- Date
- Confidence Score

---

## clean_entities.json

Contains normalized entities after

- duplicate removal
- confidence filtering
- normalization
- validation

---

## agricultural_calendar.json

Contains structured agricultural calendar records.

Example

```json
{
    "record_id": 25,
    "crop": "Rice",
    "state": "Punjab",
    "season": "Kharif",
    "weather": "Heavy Rain",
    "crop_stage": "Flowering",
    "recommendation": "Maintain proper drainage.",
    "page": 14,
    "chunk_id": 235
}
```

---

## agricultural_calendar.csv

CSV version of the agricultural calendar for analytics and visualization.

---

## entity_cleaning_report.json

Contains statistics such as

- total entities
- duplicates removed
- invalid entities removed
- normalized entities

---

## calendar_statistics.json

Contains

- crop distribution
- state distribution
- weather distribution
- recommendation distribution
- season distribution

---

## validation_report.json

Contains

- total records
- missing values
- duplicate records
- unique crops
- unique states
- quality score

---

# Applications

The dataset can be used for

- Agricultural analytics
- Crop calendar generation
- RAG applications
- Question Answering
- AI assistants
- Dashboard development
- Agricultural recommendation systems
- Information retrieval

---

# Source

Crop Weather Watch Group (CWWG)

Department of Agriculture & Farmers Welfare

Government of India

https://agriwelfare.gov.in/

---

# Notes

- The dataset is automatically generated using an AI-based extraction pipeline.
- Some fields may remain empty when information is not explicitly mentioned in the source reports.
- The extracted information preserves traceability to the original reports through page numbers and chunk identifiers.

---

# Citation

If you use this dataset in research or academic work, please cite the original CWWG reports published by the Department of Agriculture & Farmers Welfare, Government of India.