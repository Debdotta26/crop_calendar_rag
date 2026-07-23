# 🌾 India Crop Calendar AI Portal

An AI-powered agricultural information extraction and crop calendar generation system built from **Crop Weather Watch Group (CWWG)** reports published by the Department of Agriculture & Farmers Welfare, Government of India.

The project automatically extracts agricultural information from PDF reports, cleans and normalizes entities, builds a structured agricultural calendar, and provides a searchable Streamlit interface with analytics and evidence tracking.

---

## Features

- Automated PDF text extraction
- Agricultural entity extraction using GLiNER
- Entity cleaning and normalization
- Duplicate removal
- Agricultural calendar generation
- Calendar validation and quality statistics
- Interactive Streamlit dashboard
- Crop-wise and state-wise filtering
- Evidence logs linked to source reports
- Agricultural analytics and visualizations

---

## Project Pipeline

```
website scrapping
        │
        ▼
CWWG PDF Reports
        │
        ▼
PDF Text Extraction
        │
        ▼
Chunk Generation
        │
        ▼
GLiNER Entity Extraction
        │
        ▼
Entity Cleaning & Normalization
        │
        ▼
Master Agricultural Calendar
        │
        ▼
Validation & Statistics
        │
        ▼
Streamlit AI Portal
```

---

## Project Structure

```
project/

├── extraction/
│   ├── pdf_extractor.py
│   ├── chunk_builder.py
│   └── image_extractor.py
│   │
│   │
│   ├── extractor.py              # Main extraction pipeline
│   ├── run_extraction.py         #pymupdf
│   │
│   ├── cleaner.py
│   │
│   ├── metadata.py               # PyMuPDF
│   ├── text_extractor.py         # PyMuPDF
│   ├── table_extractor.py        # PyMuPDF/pdfplumber
│   ├── image_extractor.py        # PyMuPDF
│   │
│   ├── docling_extractor.py      #docling   
│   ├── merger.py                 #merging pymupdf and docling
│   ├── run_docling.py            #docling 
│   
│
├── chunking/
│   ├── adaptive_splitter.py
│   ├── semantic_merger.py
│   ├── chunk_builder.py
│   ├── chunk_validator.py
│   ├── heading_detector.py
│   ├── section_detector.py
│   ├── subsection_detector.py
│   ├── keyword_generator.py
│   ├── multimodal_linker.py
│   ├── run_chunking.py
│   ├── table_chunker.py
│   ├── page_normalizer.py
│   ├── image_chunker.py
│   
│ 
├── entity_extraction/
│   ├── gliner_extractor.py
│   ├── merge_entities.py
│   └── clean_entity.py
│   ├── entity_statistics.py
│   ├── entity_validator.py
│   └── entity_postprocessor.py
│
├── calendar/
│   ├── calendar_builder.py
│   ├── export_calendar.py
│   ├── duplicate_remover.py
│   ├── calendar_statistics.py
│   ├── run_calendar.py
│   └── stage_mapper.py
│
├── streamlit_app/
│   └──app_1.py
│
├── output/
│
├── requirements.txt
└── README.md
```

---

## Technologies Used

- Python
- GLiNER
- PyMuPDF
- Pandas
- Streamlit
- Plotly
- JSON
- Regular Expressions

---

## Installation

Clone the repository

```bash
git clone https://github.com/your_username/India-Crop-Calendar-AI.git

cd India-Crop-Calendar-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

### Entity Cleaning

```bash
python entity_extraction/clean_entity.py
```

### Build Calendar

```bash
python calendar/run_calendar.py
```

### Launch Dashboard

```bash
streamlit run app.py
```

---

## Outputs

The pipeline generates

```
output/

├── entities/
│      clean_entities.json
│
├── calendars/
│      agricultural_calendar.csv
│      agricultural_calendar.json
│
├── reports/
│      calendar_statistics.json
│      validation_report.json
│
└── evidence/
```

---

## Current Capabilities

- Crop extraction
- State extraction
- Weather event extraction
- Season detection
- Recommendation extraction
- Calendar generation
- Entity normalization
- Duplicate removal
- Dashboard analytics

---

## Future Work

- LLM-assisted missing field completion
- Semantic search
- Retrieval-Augmented Generation (RAG)
- District-level crop mapping
- Timeline visualization
- Interactive PDF evidence highlighting
- AI agricultural assistant

---

## Data Source

Crop Weather Watch Group (CWWG)

Department of Agriculture & Farmers Welfare

Government of India

https://agriwelfare.gov.in/

---

## License

This project is intended for academic and research purposes.