# app.py - Complete Enhanced India Crop Calendar Interface with Proper Chunk Loading
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
from pathlib import Path
import os
import re

# Page Configuration
st.set_page_config(
    page_title="India Crop Calendar AI Portal",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e7e34, #28a745);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #28a745;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e7e34;
    }
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }
    .detail-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin: 1rem 0;
    }
    .chunk-box {
        background: #f5f5f5;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 0.95rem;
        line-height: 1.8;
        max-height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
        border: 1px solid #e0e0e0;
    }
    .chunk-box code {
        background: #e8f5e9;
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-size: 0.85rem;
    }
    .report-link {
        background: #e3f2fd;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        margin: 0.5rem 0;
        border-left: 4px solid #1976d2;
        transition: all 0.3s;
    }
    .report-link:hover {
        background: #bbdefb;
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .chunk-ref {
        background: #fff8e1;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 3px solid #ffa000;
        margin: 0.3rem 0;
        font-size: 0.85rem;
    }
    .entity-tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1565c0;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid #90caf9;
    }
    .entity-label {
        font-weight: bold;
        color: #0d47a1;
    }
    .success-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .month-timeline {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.5rem 0;
    }
    .month-box {
        background: #e8f5e9;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        border: 1px solid #a5d6a7;
    }
    .month-box.active {
        background: #28a745;
        color: white;
        border-color: #28a745;
    }
    .stage-badge {
        display: inline-block;
        background: #e3f2fd;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 0.2rem;
        border: 1px solid #90caf9;
    }
    .report-name-box {
        background: #e8f5e9;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    .chunk-heading {
        background: #e3f2fd;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        display: inline-block;
        font-weight: bold;
        color: #0d47a1;
        margin-bottom: 0.5rem;
    }
    .date-filled {
        background: #d4edda;
        color: #155724;
        padding: 0.1rem 0.4rem;
        border-radius: 3px;
        font-size: 0.75rem;
        margin-left: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">🌱 India Crop Calendar AI Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Driven Agricultural Information Extraction from CWWG Reports</div>', unsafe_allow_html=True)

# ============================================
# LOAD DATA FROM CSV OR JSON
# ============================================

@st.cache_data
def load_data():
    """Load agricultural calendar data from CSV or JSON file"""
    
    script_dir = Path(__file__).parent if "__file__" in globals() else Path.cwd()
    
    possible_paths = [
        script_dir / "output" / "calendar" / "agricultural_calendar.csv",
        script_dir / "output" / "calendars" / "agricultural_calendar.csv",
        script_dir / "output" / "calendar" / "agricultural_calendar.json",
        script_dir / "output" / "calendars" / "agricultural_calendar.json",
        script_dir / "agricultural_calendar.csv",
        script_dir / "agricultural_calendar.json",
        script_dir / "output" / "agricultural_calendar.csv",
        script_dir / "output" / "agricultural_calendar.json",
    ]
    
    df = pd.DataFrame()
    source_file = None
    loaded_path = None
    found_files = []
    
    for path in possible_paths:
        if path.exists():
            found_files.append(str(path))
            try:
                if path.suffix.lower() == '.csv':
                    df = pd.read_csv(path)
                    source_file = "CSV"
                    loaded_path = path
                    break
                elif path.suffix.lower() == '.json':
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    df = pd.DataFrame(data)
                    source_file = "JSON"
                    loaded_path = path
                    break
            except Exception as e:
                st.warning(f"Error loading {path.name}: {str(e)}")
                continue
    
    if not df.empty:
        df = df.replace('', pd.NA)
        df = df.replace('nan', pd.NA)
        
        if source_file == "JSON" and 'record_id' in df.columns:
            column_mapping = {
                'record_id': 'Record ID',
                'report_date': 'Report Date',
                'season': 'Season',
                'crop': 'Crop',
                'state': 'State',
                'district': 'District',
                'weather': 'Weather',
                'temperature': 'Temperature',
                'rainfall': 'Rainfall',
                'crop_stage': 'Crop Stage',
                'recommendation': 'Recommendation',
                'chunk_id': 'Chunk ID',
                'source_document': 'Source',
                'page': 'Page'
            }
            rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df.rename(columns=rename_dict)
        
        elif source_file == "CSV":
            if 'crop' in df.columns:
                column_mapping = {
                    'record_id': 'Record ID',
                    'report_date': 'Report Date',
                    'season': 'Season',
                    'crop': 'Crop',
                    'state': 'State',
                    'district': 'District',
                    'weather': 'Weather',
                    'temperature': 'Temperature',
                    'rainfall': 'Rainfall',
                    'crop_stage': 'Crop Stage',
                    'recommendation': 'Recommendation',
                    'chunk_id': 'Chunk ID',
                    'source_document': 'Source',
                    'page': 'Page'
                }
                rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
                df = df.rename(columns=rename_dict)
        
        return df, source_file, loaded_path, found_files
    
    return df, None, None, found_files

# ============================================
# LOAD CHUNK DATA FROM ALL JSON FILES IN output/chunks/
# ============================================

@st.cache_data
def load_all_chunks():
    """Load all chunk data from output/chunks/ folder"""
    script_dir = Path(__file__).parent if "__file__" in globals() else Path.cwd()
    chunks_dir = script_dir / "output" / "chunks"
    
    chunk_data = {}
    source_names_list = []
    
    if chunks_dir.exists():
        json_files = list(chunks_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    source_name = json_file.stem.replace('_chunks', '')
                    source_name = source_name.replace('_', ' ')
                    source_name = source_name.replace('.pdf', '')
                    source_names_list.append(source_name)
                    
                    chunk_data[source_name] = {}
                    
                    if isinstance(data, dict):
                        if 'chunks' in data and isinstance(data['chunks'], list):
                            for chunk in data['chunks']:
                                if isinstance(chunk, dict):
                                    chunk_id = chunk.get('chunk_id')
                                    text = chunk.get('text', '')
                                    heading = chunk.get('heading', '')
                                    page_start = chunk.get('page_start', '')
                                    page_end = chunk.get('page_end', '')
                                    
                                    if chunk_id and text:
                                        chunk_data[source_name][chunk_id] = {
                                            'text': text,
                                            'heading': heading,
                                            'page': f"{page_start}-{page_end}" if page_end else str(page_start)
                                        }
                        else:
                            for key, value in data.items():
                                if isinstance(value, dict):
                                    chunk_id = value.get('chunk_id', key)
                                    text = value.get('text') or value.get('content') or value.get('chunk_text') or str(value)
                                    heading = value.get('heading', '')
                                    if chunk_id and text:
                                        chunk_data[source_name][chunk_id] = {
                                            'text': text,
                                            'heading': heading,
                                            'page': ''
                                        }
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                chunk_id = item.get('chunk_id')
                                text = item.get('text') or item.get('content') or item.get('chunk_text')
                                heading = item.get('heading', '')
                                if chunk_id and text:
                                    chunk_data[source_name][chunk_id] = {
                                        'text': text,
                                        'heading': heading,
                                        'page': ''
                                    }
                        
            except Exception as e:
                st.warning(f"Error loading chunk file {json_file.name}: {str(e)}")
    
    return chunk_data, source_names_list

# Load the data
df, source_file, loaded_path, found_files = load_data()
chunk_data, source_names_list = load_all_chunks()

# ============================================
# HELPER FUNCTION TO GET CHUNK TEXT
# ============================================

def get_chunk_text(source, chunk_id):
    """Get chunk text by source and chunk_id with improved matching"""
    if pd.isna(source) or source == '' or source is None:
        return None, None, None
    
    if pd.isna(chunk_id) or chunk_id == '' or chunk_id is None:
        return None, None, None
    
    source_clean = source.replace('.pdf', '').strip()
    chunk_id_str = str(chunk_id).strip().upper()
    
    if source_clean in chunk_data:
        if chunk_id_str in chunk_data[source_clean]:
            info = chunk_data[source_clean][chunk_id_str]
            return info.get('text'), info.get('heading'), info.get('page')
    
    for stored_source in chunk_data:
        if source_clean in stored_source or stored_source in source_clean:
            if chunk_id_str in chunk_data[stored_source]:
                info = chunk_data[stored_source][chunk_id_str]
                return info.get('text'), info.get('heading'), info.get('page')
    
    date_match = re.search(r'(\d{2}-\d{2}-\d{4})', source_clean)
    if date_match:
        date_str = date_match.group(1)
        for stored_source in chunk_data:
            if date_str in stored_source:
                if chunk_id_str in chunk_data[stored_source]:
                    info = chunk_data[stored_source][chunk_id_str]
                    return info.get('text'), info.get('heading'), info.get('page')
    
    for stored_source in chunk_data:
        if chunk_id_str in chunk_data[stored_source]:
            info = chunk_data[stored_source][chunk_id_str]
            return info.get('text'), info.get('heading'), info.get('page')
    
    return None, None, None

def normalize_source_name(source):
    if pd.isna(source) or source == '':
        return source
    return source.replace('.pdf', '').strip()

if 'Source' in df.columns:
    df['Source'] = df['Source'].apply(normalize_source_name)

# ============================================
# FILL REPORT DATE FROM CHUNK DATA
# ============================================

def fill_report_dates(df, chunk_data):
    if 'Report Date' in df.columns and 'Chunk ID' in df.columns:
        filled_count = 0
        for idx, row in df.iterrows():
            chunk_id = row.get('Chunk ID')
            source = row.get('Source', '')
            if pd.notna(chunk_id) and chunk_id != '' and source != '':
                chunk_text, _, _ = get_chunk_text(source, chunk_id)
                if chunk_text and (pd.isna(row['Report Date']) or row['Report Date'] == ''):
                    date_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', source)
                    if date_match:
                        day, month, year = date_match.groups()
                        month_names = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                                      '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
                        df.at[idx, 'Report Date'] = f"{int(day)} {month_names.get(month, month)} {year}"
                        filled_count += 1
        return df, filled_count
    return df, 0

df, filled_dates = fill_report_dates(df, chunk_data)

# Initialize session state
if 'selected_crops' not in st.session_state:
    st.session_state.selected_crops = []
if 'selected_states' not in st.session_state:
    st.session_state.selected_states = []
if 'selected_seasons' not in st.session_state:
    st.session_state.selected_seasons = []
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = []
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# ============================================
# EXTRACT ENTITIES FROM TEXT
# ============================================

def extract_entities_from_text(text):
    entities = {}
    
    if not text:
        return entities
    
    crop_patterns = ['rice', 'wheat', 'cotton', 'maize', 'sugarcane', 'soybean', 'groundnut', 'mustard', 
                      'pulses', 'moong', 'gram', 'bajra', 'jowar', 'ragi', 'sunflower']
    state_patterns = ['punjab', 'haryana', 'uttar pradesh', 'madhya pradesh', 'maharashtra', 'rajasthan', 
                      'gujarat', 'karnataka', 'andhra pradesh', 'tamil nadu', 'kerala', 'west bengal',
                      'bihar', 'odisha', 'assam', 'jharkhand', 'chhattisgarh', 'himachal pradesh']
    pest_patterns = ['borer', 'worm', 'mite', 'aphid', 'whitefly', 'jassid', 'hopper', 'caterpillar',
                     'thrips', 'weevil', 'beetle', 'maggot']
    disease_patterns = ['blight', 'rust', 'mildew', 'wilt', 'mosaic', 'virus', 'bacterial', 'fungal',
                        'leaf spot', 'powdery mildew', 'downy mildew']
    
    text_lower = text.lower()
    
    crops = []
    for crop in crop_patterns:
        if crop in text_lower:
            crops.append(crop.title())
    if crops:
        entities['CROP'] = crops
    
    states = []
    for state in state_patterns:
        if state in text_lower:
            states.append(state.title())
    if states:
        entities['STATE'] = states
    
    pests = []
    for pest in pest_patterns:
        if pest in text_lower:
            pests.append(pest.title())
    if pests:
        entities['PEST'] = pests
    
    diseases = []
    for disease in disease_patterns:
        if disease in text_lower:
            diseases.append(disease.title())
    if diseases:
        entities['DISEASE'] = diseases
    
    stage_patterns = ['sowing', 'germination', 'vegetative', 'flowering', 'pod formation', 'maturity', 'harvesting']
    stages = []
    for stage in stage_patterns:
        if stage in text_lower:
            stages.append(stage.title())
    if stages:
        entities['GROWTH_STAGE'] = stages
    
    return entities

# ============================================
# CHART FUNCTIONS
# ============================================

def create_bar_chart(data, x, y, title, xlabel, ylabel, color='green'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, y, color=color, alpha=0.7)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig

def create_pie_chart(data, labels, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

# ============================================
# DISPLAY CHUNK CONTENT
# ============================================

def display_chunk_content(chunk_text, report_name, heading, pages, chunk_id, report_date):
    st.markdown("### 📄 Original Chunk Content")
    
    st.markdown(f"""
    <div style="background: #e3f2fd; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <div>
                <b>📁 Source:</b> {report_name}
            </div>
            <div>
                <b>📄 Pages:</b> {pages if pages else 'N/A'}
            </div>
            <div>
                <b>🧩 Chunk ID:</b> <code>{chunk_id}</code>
            </div>
            <div>
                <b>📅 Date:</b> {report_date if report_date else 'N/A'}
            </div>
        </div>
        {f'<div style="margin-top: 0.3rem;"><b>📌 Heading:</b> {heading}</div>' if heading else ''}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="chunk-box">
        {chunk_text}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DISPLAY CHUNK WITH ENTITIES
# ============================================

def display_chunk_with_entities(row):
    chunk_id = row.get('Chunk ID', None)
    source = row.get('Source', None)
    
    chunk_text, heading, pages = get_chunk_text(source, chunk_id)
    
    if not chunk_text:
        chunk_text = row.get('Recommendation', 'No chunk text available')
        heading = ''
        pages = row.get('Page', '')
    
    display_chunk_content(
        chunk_text, 
        source, 
        heading, 
        pages, 
        chunk_id, 
        row.get('Report Date', None)
    )
    
    entities = extract_entities_from_text(chunk_text)
    
    if entities:
        st.markdown("### 🏷️ Extracted Entities")
        
        entity_colors = {
            'CROP': '#28a745',
            'STATE': '#007bff',
            'DISTRICT': '#17a2b8',
            'PEST': '#dc3545',
            'DISEASE': '#ffc107',
            'GROWTH_STAGE': '#6f42c1',
            'WEATHER': '#20c997'
        }
        
        entities_html = ""
        for entity_type, entity_values in entities.items():
            if isinstance(entity_values, list):
                for val in entity_values:
                    color = entity_colors.get(entity_type.upper(), '#6c757d')
                    entities_html += f'<span class="entity-tag" style="border-color: {color};"><span class="entity-label">{entity_type}:</span> {val}</span> '
            else:
                color = entity_colors.get(entity_type.upper(), '#6c757d')
                entities_html += f'<span class="entity-tag" style="border-color: {color};"><span class="entity-label">{entity_type}:</span> {entity_values}</span> '
        
        st.markdown(entities_html, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    page = st.radio(
        "Go to",
        ["📊 Dashboard", "🔍 Smart Search", "📋 Evidence Logs", "📈 Analytics", 
         "📅 Crop Calendar", "🌾 Crop Timeline", "⚠️ Events"],
        index=2
    )
    
    st.divider()
    
    if not df.empty:
        st.markdown("### 🔍 Quick Filters")
        
        if 'Crop' in df.columns:
            crops = df['Crop'].dropna().unique().tolist()
            if crops:
                selected_crops = st.multiselect(
                    "🌾 Filter by Crop",
                    options=sorted(crops),
                    default=st.session_state.selected_crops
                )
                st.session_state.selected_crops = selected_crops
        
        if 'State' in df.columns:
            states = df['State'].dropna().unique().tolist()
            if states:
                selected_states = st.multiselect(
                    "📍 Filter by State",
                    options=sorted(states),
                    default=st.session_state.selected_states
                )
                st.session_state.selected_states = selected_states
        
        if 'District' in df.columns:
            districts = df['District'].dropna().unique().tolist()
            if districts:
                selected_district = st.multiselect(
                    "🏙️ Filter by District/Region",
                    options=sorted(districts),
                    default=st.session_state.selected_district
                )
                st.session_state.selected_district = selected_district
        
        if 'Season' in df.columns:
            seasons = df['Season'].dropna().unique().tolist()
            if seasons:
                selected_seasons = st.multiselect(
                    "📅 Filter by Season",
                    options=sorted(seasons),
                    default=st.session_state.selected_seasons
                )
                st.session_state.selected_seasons = selected_seasons
        
        if st.button("🔄 Clear All Filters"):
            st.session_state.selected_crops = []
            st.session_state.selected_states = []
            st.session_state.selected_seasons = []
            st.session_state.selected_district = []
            st.rerun()
    
    st.divider()
    
    if not df.empty:
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Records", len(df))
        st.metric("Unique Crops", df['Crop'].nunique() if 'Crop' in df.columns else 0)
        st.metric("States Covered", df['State'].nunique() if 'State' in df.columns else 0)
        st.metric("Chunks Loaded", len(chunk_data))
        if filled_dates > 0:
            st.metric("📅 Dates Filled", f"{filled_dates} records")
        if source_file:
            st.metric("Data Source", source_file)
    
    st.divider()
    st.caption("Last Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

# Apply filters
filtered_df = df.copy() if not df.empty else pd.DataFrame()

if not filtered_df.empty:
    if st.session_state.selected_crops:
        filtered_df = filtered_df[filtered_df['Crop'].isin(st.session_state.selected_crops)]
    if st.session_state.selected_states:
        filtered_df = filtered_df[filtered_df['State'].isin(st.session_state.selected_states)]
    if st.session_state.selected_seasons:
        filtered_df = filtered_df[filtered_df['Season'].isin(st.session_state.selected_seasons)]
    if st.session_state.selected_district:
        filtered_df = filtered_df[filtered_df['District'].isin(st.session_state.selected_district)]

# ============================================
# PAGE: DASHBOARD
# ============================================

if page == "📊 Dashboard":
    st.markdown("### 📊 Dashboard Overview")
    
    if df.empty:
        st.warning("⚠️ No data loaded!")
    else:
        st.markdown(f"""
        <div class="success-box">
            ✅ <b>Data loaded successfully!</b><br>
            📁 Source: <code>{loaded_path}</code><br>
            📊 Format: {source_file} | Records: {len(df)} | Chunks: {len(chunk_data)}
            {f' | 📅 Dates filled: {filled_dates}' if filled_dates > 0 else ''}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(df)}</div>
                <div class="stat-label">📄 Total Records</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            crop_count = df['Crop'].nunique() if 'Crop' in df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{crop_count}</div>
                <div class="stat-label">🌾 Unique Crops</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            state_count = df['State'].nunique() if 'State' in df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{state_count}</div>
                <div class="stat-label">📍 States Covered</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            district_count = df['District'].nunique() if 'District' in df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{district_count}</div>
                <div class="stat-label">🏙️ Districts/Regions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            season_count = df['Season'].nunique() if 'Season' in df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{season_count}</div>
                <div class="stat-label">📅 Seasons</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        display_df = filtered_df if not filtered_df.empty else df
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 🌾 Top Crops")
            if 'Crop' in display_df.columns:
                crop_counts = display_df['Crop'].value_counts().head(15)
                if not crop_counts.empty:
                    fig = create_bar_chart(
                        crop_counts, 
                        crop_counts.index, 
                        crop_counts.values,
                        "Crop Distribution",
                        "Crop",
                        "Frequency",
                        '#28a745'
                    )
                    st.pyplot(fig)
        
        with col_chart2:
            st.markdown("#### 📍 State Distribution")
            if 'State' in display_df.columns:
                state_counts = display_df['State'].value_counts().head(15)
                if not state_counts.empty:
                    fig = create_bar_chart(
                        state_counts,
                        state_counts.index,
                        state_counts.values,
                        "State Distribution",
                        "State",
                        "Frequency",
                        '#007bff'
                    )
                    st.pyplot(fig)

# ============================================
# PAGE: EVIDENCE LOGS
# ============================================

elif page == "📋 Evidence Logs":
    st.markdown("### 📋 Evidence Logs")
    st.markdown("*Trace individual agricultural observations back to their source reports*")
    
    if df.empty:
        st.warning("No data available. Please check your data file.")
    else:
        if st.session_state.selected_crops or st.session_state.selected_states or st.session_state.selected_seasons or st.session_state.selected_district:
            st.info(f"🔍 Showing filtered results: {len(filtered_df)} records")
        
        search = st.text_input("🔍 Search Evidence", placeholder="Search by crop, state, recommendation, chunk text...")
        
        if search and not filtered_df.empty:
            mask = filtered_df.astype(str).apply(
                lambda row: row.str.contains(search, case=False).any(), axis=1
            )
            display_df = filtered_df[mask]
        elif not filtered_df.empty:
            display_df = filtered_df
        else:
            display_df = df
        
        st.info(f"Showing {len(display_df)} evidence logs out of {len(df)} total records.")
        
        display_cols = ['Record ID', 'Crop', 'State', 'District', 'Season', 'Report Date', 'Chunk ID']
        available_cols = [col for col in display_cols if col in display_df.columns]
        
        if not available_cols:
            available_cols = display_df.columns.tolist()[:7]
        
        st.dataframe(
            display_df[available_cols],
            width=1200,
            height=400
        )
        
        st.markdown("### 📋 Detail Insights with Chunk View")
        st.caption("Select a record from the table above to view the original chunk and extracted entities")
        
        if not display_df.empty:
            selected_idx = st.selectbox(
                "Select Record",
                options=display_df.index,
                format_func=lambda x: f"{display_df.loc[x, 'Crop'] if 'Crop' in display_df.columns else 'N/A'} - {display_df.loc[x, 'State'] if 'State' in display_df.columns else 'N/A'} (ID: {display_df.loc[x, 'Record ID'] if 'Record ID' in display_df.columns else 'N/A'})"
            )
            
            if selected_idx is not None:
                record = display_df.loc[selected_idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="detail-card">
                        <h4>📋 Record Details</h4>
                    """, unsafe_allow_html=True)
                    
                    for col in ['Record ID', 'Crop', 'State', 'District', 'Season', 'Report Date', 'Chunk ID', 'Source', 'Page']:
                        if col in record and pd.notna(record[col]):
                            st.markdown(f"**{col}:** {record[col]}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="detail-card">
                        <h4>🌤️ Weather & Recommendations</h4>
                    """, unsafe_allow_html=True)
                    
                    if 'Weather' in record and pd.notna(record['Weather']):
                        st.markdown(f"**🌤️ Weather:** {record['Weather']}")
                    
                    if 'Temperature' in record and pd.notna(record['Temperature']):
                        st.markdown(f"**🌡️ Temperature:** {record['Temperature']}")
                    
                    if 'Rainfall' in record and pd.notna(record['Rainfall']):
                        st.markdown(f"**🌧️ Rainfall:** {record['Rainfall']}")
                    
                    if 'Crop Stage' in record and pd.notna(record['Crop Stage']):
                        st.markdown(f"**🌱 Crop Stage:** {record['Crop Stage']}")
                    
                    if 'Recommendation' in record and pd.notna(record['Recommendation']):
                        st.markdown(f"**📋 Recommendation:** {record['Recommendation']}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.divider()
                display_chunk_with_entities(record)

# ============================================
# PAGE: SMART SEARCH
# ============================================

elif page == "🔍 Smart Search":
    st.markdown("### 🔍 Smart Search")
    st.markdown("*Search across all reports including chunk text and get intelligent answers*")
    
    if df.empty:
        st.warning("No data available")
    else:
        search_query = st.text_input(
            "🔍 What would you like to know?",
            placeholder="e.g., 'wheat crop in Punjab', 'pest attack in Maharashtra', 'flood damage in rice'",
            value=st.session_state.search_query
        )
        st.session_state.search_query = search_query
        
        if search_query:
            results = []
            query_lower = search_query.lower()
            
            for idx, row in df.iterrows():
                score = 0
                matches = []
                
                for col in df.columns:
                    val = str(row[col]) if pd.notna(row[col]) else ''
                    val_lower = val.lower()
                    
                    if query_lower in val_lower:
                        if col == 'Chunk ID':
                            source = row.get('Source')
                            chunk_text, _, _ = get_chunk_text(source, val)
                            if chunk_text and query_lower in chunk_text.lower():
                                score += 5
                                matches.append(f"Chunk Text: {chunk_text[:150]}...")
                        else:
                            score += 3
                            matches.append(f"{col}: {val[:150]}...")
                    elif any(word in val_lower for word in query_lower.split()):
                        score += 1
                        matches.append(f"{col}: {val[:150]}...")
                
                if score > 0:
                    results.append({
                        'row': row,
                        'score': score,
                        'matches': matches[:3]
                    })
            
            results.sort(key=lambda x: x['score'], reverse=True)
            
            if results:
                st.success(f"✅ Found {len(results)} relevant results")
                
                for idx, result in enumerate(results[:20]):
                    row = result['row']
                    with st.expander(f"📄 Result {idx+1}: {row.get('Crop', 'N/A')} - {row.get('State', 'N/A')} (Score: {result['score']})", expanded=idx<3):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="search-result">
                                <p><b>🌾 Crop:</b> {row.get('Crop', 'N/A')}</p>
                                <p><b>📍 Location:</b> {row.get('State', 'N/A')} {f"- {row.get('District', '')}" if pd.notna(row.get('District', '')) else ''}</p>
                                <p><b>📅 Season:</b> {row.get('Season', 'N/A')}</p>
                                <p><b>📅 Report Date:</b> {row.get('Report Date', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            chunk_id = row.get('Chunk ID', None)
                            source = row.get('Source')
                            chunk_text, heading, pages = get_chunk_text(source, chunk_id)
                            st.markdown(f"""
                            <div style="background: #f5f5f5; padding: 0.8rem; border-radius: 8px;">
                                <p><b>📁 Source:</b> {source or 'Unknown'}</p>
                                <p><b>📄 Pages:</b> {pages or row.get('Page', 'N/A')}</p>
                                <p><b>🧩 Chunk ID:</b> {chunk_id}</p>
                                {f'<p><b>📌 Heading:</b> {heading}</p>' if heading else ''}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("#### 📌 Relevant Sections")
                        for match in result['matches'][:3]:
                            st.markdown(f"""
                            <div class="chunk-box">
                                {match}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        chunk_id = row.get('Chunk ID', None)
                        source = row.get('Source')
                        if chunk_id:
                            chunk_text, heading, pages = get_chunk_text(source, chunk_id)
                            if chunk_text:
                                st.markdown(f"### 📄 Full Chunk Content")
                                display_chunk_content(
                                    chunk_text,
                                    source,
                                    heading,
                                    pages,
                                    chunk_id,
                                    row.get('Report Date', None)
                                )
            else:
                st.info("No results found. Try different keywords.")
        else:
            st.info("💡 Enter a search query above to find relevant information")

# ============================================
# PAGE: CROP TIMELINE - UPDATED WITH GROWTH STAGE CHART
# ============================================

elif page == "🌾 Crop Timeline":
    st.markdown("### 🌾 Crop Timeline")
    st.markdown("*Track crop start and end dates, stages, and regional activity*")
    
    if df.empty:
        st.warning("No data available")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            timeline_crop = st.selectbox(
                "🌾 Select Crop",
                options=sorted(df['Crop'].dropna().unique()),
                index=0
            )
        
        with col2:
            timeline_state = st.selectbox(
                "📍 Select State",
                options=sorted(df['State'].dropna().unique()),
                index=0
            )
        
        with col3:
            seasons_list = sorted(df['Season'].dropna().unique()) if 'Season' in df.columns else ['All']
            timeline_season = st.selectbox(
                "📅 Select Season",
                options=seasons_list,
                index=0
            )
        
        timeline_filtered = df[
            (df['Crop'] == timeline_crop) &
            (df['State'] == timeline_state)
        ]
        
        if timeline_season != 'All':
            timeline_filtered = timeline_filtered[timeline_filtered['Season'] == timeline_season]
        
        if not timeline_filtered.empty:
            st.success(f"📊 Found {len(timeline_filtered)} timeline entries for {timeline_crop} in {timeline_state}")
            
            # ============================================
            # GROWTH STAGE ANALYSIS CHART
            # ============================================
            
            st.markdown("### 📈 Growth Stage Analysis")
            st.markdown("*Occurrence of growth stages in the selected data*")
            
            # Define growth stage keywords
            growth_keywords = {
                'Active Growth': ['active growth', 'growth', 'vegetative', 'tiller', 'leaf', 'stem', 'branching', 'growing'],
                'Harvesting': ['harvesting', 'harvest', 'harvested', 'cutting', 'yield', 'threshing'],
                'Sowing': ['sowing', 'sown', 'planting', 'transplant', 'seed', 'germination']
            }
            
            # Count occurrences in the filtered data
            growth_counts = {key: 0 for key in growth_keywords.keys()}
            
            for _, row in timeline_filtered.iterrows():
                chunk_id = row.get('Chunk ID', None)
                source = row.get('Source')
                if chunk_id:
                    chunk_text, _, _ = get_chunk_text(source, chunk_id)
                    if chunk_text:
                        chunk_lower = chunk_text.lower()
                        for stage, keywords in growth_keywords.items():
                            for keyword in keywords:
                                if keyword in chunk_lower:
                                    growth_counts[stage] += 1
                                    break
            
            # Create bar chart
            if any(growth_counts.values()):
                fig, ax = plt.subplots(figsize=(10, 6))
                stages = list(growth_counts.keys())
                counts = list(growth_counts.values())
                colors = ['#28a745', '#ffc107', '#007bff']
                
                bars = ax.bar(stages, counts, color=colors, alpha=0.7)
                ax.set_title(f'Growth Stage Occurrences for {timeline_crop} in {timeline_state}', fontsize=14, fontweight='bold')
                ax.set_xlabel('Growth Stage')
                ax.set_ylabel('Number of Occurrences')
                
                # Add value labels on bars
                for bar, count in zip(bars, counts):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                            str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No growth stage keywords found in the chunks for this selection")
            
            st.divider()
            
            st.markdown("### 📋 Related Chunks")
            
            for _, row in timeline_filtered.iterrows():
                chunk_id = row.get('Chunk ID', None)
                source = row.get('Source')
                if chunk_id:
                    chunk_text, heading, pages = get_chunk_text(source, chunk_id)
                    report_date = row.get('Report Date', 'N/A')
                    
                    with st.expander(f"📄 {source} - {chunk_id}", expanded=True):
                        display_chunk_content(
                            chunk_text,
                            source,
                            heading,
                            pages,
                            chunk_id,
                            report_date
                        )
            
            st.divider()
            st.markdown("#### 📋 Detailed Timeline Data")
            st.dataframe(
                timeline_filtered[['Crop', 'State', 'District', 'Crop Stage', 'Report Date', 'Source', 'Page', 'Chunk ID']], 
                width=1200
            )
            
        else:
            st.info(f"No timeline data found for {timeline_crop} in {timeline_state}")

# ============================================
# PAGE: EVENTS - UPDATED WITH DISTINCT DISEASE AND PEST COUNTS
# ============================================

elif page == "⚠️ Events":
    st.markdown("### ⚠️ Event Tracking & Crop Damage Reports")
    st.markdown("*Track pest and disease occurrences based on actual data from CWWG reports*")
    
    if df.empty:
        st.warning("No data available")
    else:
        # Define DISTINCT disease and pest keywords (NO OVERLAP)
        disease_keywords = ['disease', 'blight', 'rust', 'mildew', 'wilt', 'mosaic', 'virus', 'bacterial', 'fungal', 'leaf spot', 'powdery mildew', 'downy mildew']
        pest_keywords = ['pest', 'infestation', 'borer', 'worm', 'mite', 'aphid', 'whitefly', 'bollworm', 'caterpillar', 'thrips', 'weevil', 'beetle', 'maggot', 'jassid', 'hopper']
        
        # Collect events from chunks with counts per source
        events_data = []
        
        # Get unique sources
        sources = df['Source'].dropna().unique()
        
        for source in sources:
            # Get all rows for this source
            source_rows = df[df['Source'] == source]
            
            disease_count = 0
            pest_count = 0
            
            for _, row in source_rows.iterrows():
                chunk_id = row.get('Chunk ID', None)
                if chunk_id:
                    chunk_text, heading, pages = get_chunk_text(source, chunk_id)
                    if chunk_text:
                        chunk_lower = chunk_text.lower()
                        
                        # Count diseases (using distinct disease keywords)
                        for keyword in disease_keywords:
                            if keyword in chunk_lower:
                                disease_count += 1
                                break
                        
                        # Count pests (using distinct pest keywords)
                        for keyword in pest_keywords:
                            if keyword in chunk_lower:
                                pest_count += 1
                                break
            
            if disease_count > 0 or pest_count > 0:
                # Extract date from source
                date_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', source)
                display_date = source
                if date_match:
                    day, month, year = date_match.groups()
                    month_names = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                                  '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
                    display_date = f"{int(day)} {month_names.get(month, month)} {year}"
                
                events_data.append({
                    'Source Report': display_date,
                    'Disease': disease_count,
                    'Pest': pest_count,
                    'Total Events': disease_count + pest_count,
                    'Full Source': source
                })
        
        events_df = pd.DataFrame(events_data)
        
        if not events_df.empty:
            # Sort by Total Events descending
            events_df = events_df.sort_values('Total Events', ascending=False)
            
            # Show statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 Reports with Events", len(events_df))
            with col2:
                st.metric("🦠 Total Disease Events", events_df['Disease'].sum())
            with col3:
                st.metric("🐛 Total Pest Events", events_df['Pest'].sum())
            with col4:
                st.metric("⚠️ Total Events", events_df['Total Events'].sum())
            
            st.divider()
            
            # Display table
            st.markdown("### 📊 Event Summary by Report")
            st.markdown("*Disease and Pest occurrences per report*")
            
            st.dataframe(
                events_df[['Source Report', 'Disease', 'Pest', 'Total Events']],
                width=1200,
                height=400,
                column_config={
                    "Source Report": "📅 Source Report",
                    "Disease": "🦠 Disease",
                    "Pest": "🐛 Pest",
                    "Total Events": "⚠️ Total"
                }
            )
            
            # Highlight top reports
            st.divider()
            st.markdown("### 🔥 Top Reports with Most Events")
            
            col1, col2 = st.columns(2)
            
            with col1:
                top_disease = events_df.nlargest(5, 'Disease')
                st.markdown("#### 🦠 Top 5 Disease Reports")
                st.dataframe(
                    top_disease[['Source Report', 'Disease']],
                    width=500,
                    height=200
                )
            
            with col2:
                top_pest = events_df.nlargest(5, 'Pest')
                st.markdown("#### 🐛 Top 5 Pest Reports")
                st.dataframe(
                    top_pest[['Source Report', 'Pest']],
                    width=500,
                    height=200
                )
            
            # Charts
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Disease vs Pest Distribution")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                x = range(len(events_df))
                bar_width = 0.35
                
                ax.bar(x, events_df['Disease'], bar_width, label='Disease', color='#ff6b6b', alpha=0.8)
                ax.bar([i + bar_width for i in x], events_df['Pest'], bar_width, label='Pest', color='#ffd93d', alpha=0.8)
                
                ax.set_xlabel('Source Report')
                ax.set_ylabel('Count')
                ax.set_title('Disease vs Pest Count by Report', fontsize=14, fontweight='bold')
                ax.set_xticks([i + bar_width/2 for i in x])
                ax.set_xticklabels(events_df['Source Report'], rotation=45, ha='right', fontsize=8)
                ax.legend()
                
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                st.markdown("#### 📈 Event Trend Over Time")
                
                events_df_sorted = events_df.sort_values('Source Report')
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(events_df_sorted['Source Report'], events_df_sorted['Disease'], 
                       marker='o', label='Disease', color='#ff6b6b', linewidth=2)
                ax.plot(events_df_sorted['Source Report'], events_df_sorted['Pest'], 
                       marker='s', label='Pest', color='#ffd93d', linewidth=2)
                ax.plot(events_df_sorted['Source Report'], events_df_sorted['Total Events'], 
                       marker='^', label='Total', color='#74b9ff', linewidth=2, linestyle='--')
                
                ax.set_xlabel('Report Date')
                ax.set_ylabel('Event Count')
                ax.set_title('Event Trends Over Time', fontsize=14, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
                ax.legend()
                
                plt.tight_layout()
                st.pyplot(fig)
            
            # Additional chart: Total events per report
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Total Events per Report")
                top_events = events_df.nlargest(10, 'Total Events')
                fig = create_bar_chart(
                    top_events['Total Events'],
                    top_events['Source Report'],
                    top_events['Total Events'].values,
                    "Top 10 Reports with Most Events",
                    "Source Report",
                    "Event Count",
                    '#74b9ff'
                )
                st.pyplot(fig)
            
            with col2:
                st.markdown("#### 🍩 Event Type Distribution")
                total_disease = events_df['Disease'].sum()
                total_pest = events_df['Pest'].sum()
                
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie([total_disease, total_pest], 
                       labels=[f'Disease ({total_disease})', f'Pest ({total_pest})'],
                       autopct='%1.1f%%', 
                       startangle=90,
                       colors=['#ff6b6b', '#ffd93d'])
                ax.set_title('Overall Disease vs Pest Distribution', fontsize=14, fontweight='bold')
                plt.tight_layout()
                st.pyplot(fig)
            
            # Export button for events data
            st.divider()
            st.markdown("#### 📥 Export Events Data")
            
            csv_events = events_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Events CSV",
                data=csv_events,
                file_name="events_summary.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Show detailed view for selected report
            st.divider()
            st.markdown("### 📋 Detailed Report View")
            st.markdown("*Select a report to view its detailed events*")
            
            selected_report = st.selectbox(
                "Select Source Report",
                options=events_df['Full Source'].tolist(),
                format_func=lambda x: x[:40] + '...' if len(x) > 40 else x
            )
            
            if selected_report:
                source_rows = df[df['Source'] == selected_report]
                
                st.markdown(f"#### 📁 {selected_report}")
                st.markdown(f"**Total Records:** {len(source_rows)}")
                
                st.dataframe(
                    source_rows[['Crop', 'State', 'Season', 'Report Date', 'Chunk ID', 'Recommendation']],
                    width=1200,
                    height=300
                )
                
                if not source_rows.empty:
                    first_row = source_rows.iloc[0]
                    chunk_id = first_row.get('Chunk ID')
                    if chunk_id:
                        chunk_text, heading, pages = get_chunk_text(selected_report, chunk_id)
                        if chunk_text:
                            with st.expander("📄 View Sample Chunk Content", expanded=True):
                                display_chunk_content(
                                    chunk_text,
                                    selected_report,
                                    heading,
                                    pages,
                                    chunk_id,
                                    first_row.get('Report Date', 'N/A')
                                )
        else:
            st.info("No events found in the current dataset.")

# ============================================
# PAGE: ANALYTICS
# ============================================

elif page == "📈 Analytics":
    st.markdown("### 📈 Agricultural Analytics Dashboard")
    st.markdown("*Statistical summaries and distribution metrics of extracted observations*")
    
    if df.empty:
        st.warning("No data available. Please check your data file.")
    else:
        display_df = filtered_df if not filtered_df.empty else df
        
        if display_df.empty:
            st.warning("No data matches the selected filters. Try clearing the filters.")
            if st.button("Clear Filters"):
                st.session_state.selected_crops = []
                st.session_state.selected_states = []
                st.session_state.selected_seasons = []
                st.session_state.selected_district = []
                st.rerun()
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🌾 Crop Distribution")
                if 'Crop' in display_df.columns:
                    crop_counts = display_df['Crop'].value_counts()
                    if not crop_counts.empty:
                        fig = create_bar_chart(
                            crop_counts,
                            crop_counts.index,
                            crop_counts.values,
                            "Crop Distribution in Observations",
                            "Crop",
                            "Frequency",
                            '#28a745'
                        )
                        st.pyplot(fig)
            
            with col2:
                st.markdown("#### 📍 State Distribution")
                if 'State' in display_df.columns:
                    state_counts = display_df['State'].value_counts()
                    if not state_counts.empty:
                        fig = create_bar_chart(
                            state_counts,
                            state_counts.index,
                            state_counts.values,
                            "State Distribution in Observations",
                            "State",
                            "Frequency",
                            '#007bff'
                        )
                        st.pyplot(fig)
            
            st.divider()
            col3, col4, col5 = st.columns(3)
            
            with col3:
                st.markdown("#### 📅 Season Distribution")
                if 'Season' in display_df.columns:
                    season_counts = display_df['Season'].value_counts()
                    if not season_counts.empty:
                        fig = create_pie_chart(
                            season_counts.values,
                            season_counts.index,
                            "Season Distribution"
                        )
                        st.pyplot(fig)
            
            with col4:
                st.markdown("#### 📊 Top Crops")
                if 'Crop' in display_df.columns:
                    top_crops = display_df['Crop'].value_counts().head(10)
                    if not top_crops.empty:
                        fig = create_pie_chart(
                            top_crops.values,
                            top_crops.index,
                            "Top 10 Crops"
                        )
                        st.pyplot(fig)
            
            with col5:
                st.markdown("#### 📈 Summary Stats")
                st.metric("Total Records", len(display_df))
                st.metric("Unique Crops", display_df['Crop'].nunique() if 'Crop' in display_df.columns else 0)
                st.metric("States Covered", display_df['State'].nunique() if 'State' in display_df.columns else 0)
                st.metric("Districts/Regions", display_df['District'].nunique() if 'District' in display_df.columns else 0)
            
            st.divider()
            st.markdown("#### 📊 Crop-State Matrix")
            
            if 'Crop' in display_df.columns and 'State' in display_df.columns:
                pivot_table = pd.crosstab(
                    display_df['Crop'], 
                    display_df['State']
                )
                if not pivot_table.empty:
                    st.dataframe(pivot_table, width=1200, height=400)

# ============================================
# PAGE: CROP CALENDAR
# ============================================

elif page == "📅 Crop Calendar":
    st.markdown("### 📅 Crop Calendar")
    st.markdown("*Consolidated crop calendar showing sowing, growing, and harvesting periods*")
    
    if df.empty:
        st.warning("No calendar data available. Please check your data file.")
    else:
        display_df = filtered_df if not filtered_df.empty else df
        
        if filled_dates > 0:
            st.info(f"📅 Auto-filled {filled_dates} Report Date values from chunk filenames")
        
        display_cols = ['Crop', 'State', 'District', 'Season', 'Report Date', 'Chunk ID', 'Source', 'Page']
        available_cols = [col for col in display_cols if col in display_df.columns]
        
        if not available_cols:
            available_cols = df.columns.tolist()[:8]
        
        st.dataframe(
            display_df[available_cols],
            width=1200,
            height=400
        )
        
        st.divider()
        st.markdown("#### 📥 Export Calendar Data")
        
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name="agricultural_calendar.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_export2:
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Calendar')
                st.download_button(
                    label="📱 Download Excel",
                    data=output.getvalue(),
                    file_name="agricultural_calendar.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.warning("⚠️ openpyxl not installed. Excel export disabled.")
        
        with col_export3:
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="🔗 Download JSON",
                data=json_data,
                file_name="agricultural_calendar.json",
                mime="application/json",
                use_container_width=True
            )

# Footer
st.divider()
if not df.empty:
    st.caption(f"🌱 India Crop Calendar AI Portal | Data Source: {source_file} | Records: {len(df)} | Chunks: {len(chunk_data)} | Dates Filled: {filled_dates} | © 2026")
else:
    st.caption("🌱 India Crop Calendar AI Portal | No data loaded | © 2026")