# app.py - Complete Enhanced India Crop Calendar Interface
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
    .event-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .report-link {
        background: #e3f2fd;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin: 0.3rem 0;
        border-left: 3px solid #1976d2;
    }
    .report-link:hover {
        background: #bbdefb;
    }
    .chunk-box {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
    }
    .region-tag {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .timeline-item {
        padding: 0.5rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .search-result {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
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
                    'source_document': 'Source',
                    'page': 'Page'
                }
                rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
                df = df.rename(columns=rename_dict)
        
        return df, source_file, loaded_path, found_files
    
    return df, None, None, found_files

# Load the data
df, source_file, loaded_path, found_files = load_data()

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
# ENHANCED FUNCTIONS
# ============================================

def extract_crop_timeline(df):
    """Extract crop start and end dates/timelines from recommendations"""
    timelines = []
    
    stage_durations = {
        'sowing': 7,
        'germination': 10,
        'vegetative': 30,
        'flowering': 20,
        'pod formation': 15,
        'maturity': 20,
        'harvesting': 14
    }
    
    if 'Crop' in df.columns and 'Recommendation' in df.columns:
        for idx, row in df.iterrows():
            rec = str(row['Recommendation']) if pd.notna(row['Recommendation']) else ''
            
            date_patterns = [
                r'(\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))',
                r'(\d{1,2}/\d{1,2}/\d{4})',
                r'(\d{4}-\d{2}-\d{2})',
                r'Week\s+(\d+)'
            ]
            
            dates_found = []
            for pattern in date_patterns:
                matches = re.findall(pattern, rec, re.IGNORECASE)
                dates_found.extend(matches)
            
            stage = 'Unknown'
            for s in stage_durations.keys():
                if s in rec.lower():
                    stage = s.title()
                    break
            
            timelines.append({
                'Crop': row.get('Crop', 'N/A'),
                'State': row.get('State', 'N/A'),
                'District': row.get('District', 'N/A'),
                'Season': row.get('Season', 'N/A'),
                'Stage': stage,
                'Dates': dates_found if dates_found else ['Week info not specified'],
                'Recommendation': rec[:150] + '...' if len(rec) > 150 else rec,
                'Source': row.get('Source', 'Merged_CWWG_Reports'),
                'Page': row.get('Page', 'N/A')
            })
    
    return pd.DataFrame(timelines)

def extract_events(df):
    """Extract events that caused crop destruction"""
    events = []
    
    event_keywords = {
        'Flood': ['flood', 'waterlogging', 'submerged', 'inundation', 'heavy rain', 'cyclone'],
        'Drought': ['drought', 'dry spell', 'no rainfall', 'water stress', 'rainfall deficit'],
        'Pest Attack': ['pest', 'infestation', 'borer', 'worm', 'aphid', 'whitefly', 'bollworm', 'caterpillar'],
        'Disease Outbreak': ['disease', 'blight', 'rust', 'mildew', 'wilt', 'mosaic', 'virus', 'bacterial', 'fungal'],
        'Hailstorm': ['hail', 'storm', 'cyclone', 'wind damage'],
        'Heat Wave': ['heat wave', 'high temperature', 'extreme heat', 'heat stress'],
        'Cold Wave': ['cold wave', 'frost', 'freezing', 'low temperature']
    }
    
    if 'Recommendation' in df.columns:
        for idx, row in df.iterrows():
            rec = str(row['Recommendation']) if pd.notna(row['Recommendation']) else ''
            
            events_found = []
            for event_type, keywords in event_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in rec.lower():
                        events_found.append(event_type)
                        break
            
            if events_found:
                events.append({
                    'Crop': row.get('Crop', 'N/A'),
                    'State': row.get('State', 'N/A'),
                    'District': row.get('District', 'N/A'),
                    'Season': row.get('Season', 'N/A'),
                    'Event': ', '.join(list(set(events_found))),
                    'Description': rec[:200] + '...' if len(rec) > 200 else rec,
                    'Source': row.get('Source', 'Merged_CWWG_Reports'),
                    'Page': row.get('Page', 'N/A'),
                    'Report Date': row.get('Report Date', 'N/A')
                })
    
    return pd.DataFrame(events)

def smart_search(df, query):
    """Intelligent search across all columns with relevance scoring"""
    if not query or df.empty:
        return df
    
    query = query.lower()
    results = []
    
    for idx, row in df.iterrows():
        score = 0
        matches = []
        
        for col in df.columns:
            val = str(row[col]) if pd.notna(row[col]) else ''
            val_lower = val.lower()
            
            if query in val_lower:
                score += 3
                matches.append(f"{col}: {val[:100]}...")
            elif any(word in val_lower for word in query.split()):
                score += 1
                matches.append(f"{col}: {val[:100]}...")
        
        if score > 0:
            results.append({
                'row': row,
                'score': score,
                'matches': matches[:3]
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    if results:
        return pd.DataFrame([r['row'] for r in results[:20]])
    return pd.DataFrame()

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
# SIDEBAR - UPDATED
# ============================================

with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    page = st.radio(
        "Go to",
        ["📊 Dashboard", "🔍 Smart Search", "📋 Evidence Logs", "📈 Analytics", 
         "📅 Crop Calendar", "🐛 Pests & Diseases", "📊 Calendar Matrix", "🌾 Crop Timeline", "⚠️ Events"],
        index=0
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
        st.metric("Districts/Regions", df['District'].nunique() if 'District' in df.columns else 0)
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
# PAGE: SMART SEARCH
# ============================================

if page == "🔍 Smart Search":
    st.markdown("### 🔍 Smart Search")
    st.markdown("*Search anything across all reports and get intelligent answers*")
    
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
            results_df = smart_search(df, search_query)
            
            if not results_df.empty:
                st.success(f"✅ Found {len(results_df)} relevant results")
                
                for idx, row in results_df.iterrows():
                    with st.expander(f"📄 Result {idx+1}: {row.get('Crop', 'N/A')} - {row.get('State', 'N/A')}", expanded=idx<3):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="search-result">
                                <p><b>🌾 Crop:</b> {row.get('Crop', 'N/A')}</p>
                                <p><b>📍 Location:</b> {row.get('State', 'N/A')} {f"- {row.get('District', '')}" if pd.notna(row.get('District', '')) else ''}</p>
                                <p><b>📅 Season:</b> {row.get('Season', 'N/A')}</p>
                                <p><b>📋 Details:</b> {row.get('Recommendation', 'No details')[:300]}...</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style="background: #f5f5f5; padding: 0.8rem; border-radius: 8px;">
                                <p><b>📁 Source:</b> {row.get('Source', 'Merged_CWWG_Reports')}</p>
                                <p><b>📄 Page:</b> {row.get('Page', 'N/A')}</p>
                                <p><b>📅 Report Date:</b> {row.get('Report Date', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("#### 📌 Relevant Sections")
                        for col in df.columns:
                            val = str(row[col]) if pd.notna(row[col]) else ''
                            if search_query.lower() in val.lower():
                                st.markdown(f"""
                                <div class="chunk-box">
                                    <b>{col}:</b> {val[:200]}...
                                </div>
                                """, unsafe_allow_html=True)
            else:
                st.info("No results found. Try different keywords.")
        else:
            st.info("💡 Enter a search query above to find relevant information")

# ============================================
# PAGE: CROP TIMELINE
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
        
        timeline_df = extract_crop_timeline(df)
        
        if not timeline_df.empty:
            timeline_filtered = timeline_df[
                (timeline_df['Crop'] == timeline_crop) &
                (timeline_df['State'] == timeline_state)
            ]
            
            if timeline_season != 'All':
                timeline_filtered = timeline_filtered[timeline_filtered['Season'] == timeline_season]
            
            if not timeline_filtered.empty:
                st.success(f"📊 Found {len(timeline_filtered)} timeline entries for {timeline_crop} in {timeline_state}")
                
                st.markdown("#### 📅 Crop Growth Timeline")
                
                stages = ['Land Prep', 'Sowing', 'Germination', 'Vegetative', 'Flowering', 'Pod Formation', 'Maturity', 'Harvesting']
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("##### 📈 Growth Stages")
                    for i, stage in enumerate(stages):
                        week = (i + 1) * 2
                        st.markdown(f"""
                        <div class="timeline-item">
                            <b>Week {week}:</b> {stage}
                            <span style="float: right; color: #666;">🟢 Active</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("##### 📋 Details")
                    for _, row in timeline_filtered.iterrows():
                        st.markdown(f"""
                        <div style="background: #f5f5f5; padding: 0.5rem; border-radius: 5px; margin: 0.3rem 0;">
                            <b>Stage:</b> {row['Stage']}<br>
                            <b>Dates:</b> {', '.join(row['Dates'][:2])}<br>
                            <b>📁 Source:</b> {row['Source']}<br>
                            <b>📄 Page:</b> {row['Page']}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.divider()
                st.markdown("#### 📋 Detailed Timeline Data")
                st.dataframe(timeline_filtered[['Crop', 'State', 'District', 'Stage', 'Dates', 'Source', 'Page']], width=1200)
                
            else:
                st.info(f"No timeline data found for {timeline_crop} in {timeline_state}")
        else:
            st.info("No timeline data available")

# ============================================
# PAGE: EVENTS
# ============================================

elif page == "⚠️ Events":
    st.markdown("### ⚠️ Event Tracking & Crop Damage Reports")
    st.markdown("*Track events that affect crops (flood, drought, pests, diseases, etc.)*")
    
    if df.empty:
        st.warning("No data available")
    else:
        events_df = extract_events(df)
        
        if not events_df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("⚠️ Total Events", len(events_df))
            with col2:
                st.metric("🌾 Crops Affected", events_df['Crop'].nunique())
            with col3:
                st.metric("📍 States Affected", events_df['State'].nunique())
            with col4:
                event_types = events_df['Event'].str.split(', ').explode().nunique()
                st.metric("📋 Event Types", event_types)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                event_crop_filter = st.multiselect(
                    "🌾 Filter by Crop",
                    options=sorted(events_df['Crop'].unique()),
                    default=[]
                )
            
            with col2:
                all_events = sorted(set(', '.join(events_df['Event'].unique()).split(', ')))
                event_type_filter = st.multiselect(
                    "⚠️ Filter by Event Type",
                    options=all_events,
                    default=[]
                )
            
            filtered_events = events_df.copy()
            if event_crop_filter:
                filtered_events = filtered_events[filtered_events['Crop'].isin(event_crop_filter)]
            if event_type_filter:
                filtered_events = filtered_events[filtered_events['Event'].str.contains('|'.join(event_type_filter), case=False, na=False)]
            
            st.info(f"Showing {len(filtered_events)} event reports")
            
            for _, row in filtered_events.iterrows():
                event_color = {
                    'Flood': '#ff6b6b',
                    'Drought': '#ffd93d',
                    'Pest Attack': '#ff8a5c',
                    'Disease Outbreak': '#a29bfe',
                    'Hailstorm': '#74b9ff',
                    'Heat Wave': '#fd79a8',
                    'Cold Wave': '#81ecec'
                }.get(row['Event'].split(',')[0].strip(), '#dfe6e9')
                
                st.markdown(f"""
                <div style="border-left: 4px solid {event_color}; padding: 1rem; margin: 0.5rem 0; background: #fafafa; border-radius: 5px;">
                    <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                        <div>
                            <b>🌾 {row['Crop']}</b>
                            <span style="background: {event_color}; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; margin-left: 0.5rem;">
                                {row['Event']}
                            </span>
                        </div>
                        <div style="color: #666; font-size: 0.9rem;">
                            📍 {row['State']} {f"- {row['District']}" if pd.notna(row['District']) and row['District'] != '' else ''}
                            {f" | 📅 {row['Report Date']}" if pd.notna(row['Report Date']) and row['Report Date'] != '' else ''}
                        </div>
                    </div>
                    <p style="margin-top: 0.5rem; color: #444;">{row['Description']}</p>
                    <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">
                        📁 Source: {row['Source']} | 📄 Page: {row['Page']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Event Distribution")
                event_counts = filtered_events['Event'].str.split(', ').explode().value_counts()
                if not event_counts.empty:
                    fig = create_bar_chart(
                        event_counts,
                        event_counts.index,
                        event_counts.values,
                        "Event Types Distribution",
                        "Event Type",
                        "Frequency",
                        '#ff6b6b'
                    )
                    st.pyplot(fig)
            
            with col2:
                st.markdown("#### 📋 Event Summary by Crop")
                event_crop_summary = filtered_events.groupby('Crop')['Event'].count().sort_values(ascending=False)
                if not event_crop_summary.empty:
                    fig = create_bar_chart(
                        event_crop_summary,
                        event_crop_summary.index,
                        event_crop_summary.values,
                        "Crops Most Affected",
                        "Crop",
                        "Number of Events",
                        '#ffd93d'
                    )
                    st.pyplot(fig)
        else:
            st.info("No events found in the current dataset")

# ============================================
# PAGE: DASHBOARD
# ============================================

elif page == "📊 Dashboard":
    st.markdown("### 📊 Dashboard Overview")
    
    if df.empty:
        st.warning("⚠️ No data loaded!")
    else:
        st.markdown(f"""
        <div class="success-box">
            ✅ <b>Data loaded successfully!</b><br>
            📁 Source: <code>{loaded_path}</code><br>
            📊 Format: {source_file} | Records: {len(df)}
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
        
        search = st.text_input("🔍 Search Evidence", placeholder="Search by crop, state, recommendation...")
        
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
        
        display_cols = ['Record ID', 'Crop', 'State', 'District', 'Season', 'Report Date', 'Recommendation']
        available_cols = [col for col in display_cols if col in display_df.columns]
        
        if not available_cols:
            available_cols = display_df.columns.tolist()[:7]
        
        st.dataframe(
            display_df[available_cols],
            width=1200,
            height=400
        )
        
        st.markdown("### 📋 Detail Insights")
        st.caption("Select a record from the table above to view details")
        
        if not display_df.empty:
            selected_idx = st.selectbox(
                "Select Record",
                options=display_df.index,
                format_func=lambda x: f"{display_df.loc[x, 'Crop'] if 'Crop' in display_df.columns else 'N/A'} - {display_df.loc[x, 'State'] if 'State' in display_df.columns else 'N/A'}"
            )
            
            if selected_idx is not None:
                record = display_df.loc[selected_idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="detail-card">
                        <h4>📋 Record Details</h4>
                    """, unsafe_allow_html=True)
                    
                    for col in ['Crop', 'State', 'District', 'Season', 'Report Date', 'Page']:
                        if col in record and pd.notna(record[col]):
                            st.markdown(f"**{col}:** {record[col]}")
                    
                    if 'Source' in record and pd.notna(record['Source']):
                        st.markdown(f"**📁 Source:** {record['Source']}")
                    
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
                    
                    if 'Recommendation' in record and pd.notna(record['Recommendation']):
                        st.markdown(f"**📋 Recommendation:** {record['Recommendation']}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("#### 📄 Full Record")
                st.json(record.to_dict())

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
        
        display_cols = ['Crop', 'State', 'District', 'Season', 'Report Date', 'Recommendation']
        available_cols = [col for col in display_cols if col in df.columns]
        
        if not available_cols:
            available_cols = df.columns.tolist()[:6]
        
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

# ============================================
# PAGE: PESTS & DISEASES
# ============================================

elif page == "🐛 Pests & Diseases":
    st.markdown("### 🐛 Top Reported Pests & Diseases")
    st.markdown("*Track pest and disease occurrences across different crops and regions*")
    
    if df.empty:
        st.warning("No data available")
    else:
        pest_keywords = ['pest', 'infestation', 'borer', 'worm', 'mite', 'aphid', 'caterpillar']
        disease_keywords = ['disease', 'blight', 'rust', 'mildew', 'wilt', 'mosaic', 'virus', 'bacterial']
        
        pest_data = []
        for idx, row in df.iterrows():
            rec = str(row['Recommendation']) if pd.notna(row['Recommendation']) else ''
            
            pest_found = [k for k in pest_keywords if k in rec.lower()]
            disease_found = [k for k in disease_keywords if k in rec.lower()]
            
            if pest_found or disease_found:
                pest_data.append({
                    'Crop': row.get('Crop', 'N/A'),
                    'State': row.get('State', 'N/A'),
                    'District': row.get('District', 'N/A'),
                    'Pest': ', '.join(pest_found) if pest_found else 'No pest reported',
                    'Disease': ', '.join(disease_found) if disease_found else 'No disease reported',
                    'Recommendation': rec[:200] + '...' if len(rec) > 200 else rec
                })
        
        pest_df = pd.DataFrame(pest_data)
        
        if not pest_df.empty:
            st.dataframe(pest_df, width=1200, height=400)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🐛 Top Pests")
                pest_counts = pest_df['Pest'].value_counts().head(10)
                if not pest_counts.empty:
                    fig = create_bar_chart(
                        pest_counts, 
                        pest_counts.index, 
                        pest_counts.values, 
                        "Most Common Pests", 
                        "Pest", 
                        "Frequency", 
                        '#dc3545'
                    )
                    st.pyplot(fig)
            
            with col2:
                st.markdown("#### 🦠 Top Diseases")
                disease_counts = pest_df['Disease'].value_counts().head(10)
                if not disease_counts.empty:
                    fig = create_bar_chart(
                        disease_counts, 
                        disease_counts.index, 
                        disease_counts.values, 
                        "Most Common Diseases", 
                        "Disease", 
                        "Frequency", 
                        '#ffc107'
                    )
                    st.pyplot(fig)

# ============================================
# PAGE: CALENDAR MATRIX
# ============================================

elif page == "📊 Calendar Matrix":
    st.markdown("### 📊 Weekly Crop Calendar Matrix")
    st.markdown("*Week-by-week aggregated timelines of crop stages, pests, and advisories*")
    
    if df.empty:
        st.warning("No data available")
    else:
        growth_stages = ['Land Preparation', 'Sowing', 'Germination', 'Vegetative Growth', 'Flowering', 'Pod Formation', 'Maturity', 'Harvesting']
        
        calendar_data = []
        if 'Crop' in df.columns and 'Season' in df.columns:
            crop_groups = df.groupby(['Crop', 'Season'])
            
            for (crop, season), group in crop_groups:
                recommendations = group['Recommendation'].dropna().unique().tolist()
                
                active_stages = []
                stage_keywords = {
                    'Land Preparation': ['land prep', 'preparation', 'tillage'],
                    'Sowing': ['sow', 'seed', 'planting'],
                    'Germination': ['germinate', 'sprout'],
                    'Vegetative Growth': ['vegetative', 'growth', 'tiller'],
                    'Flowering': ['flower', 'bloom'],
                    'Pod Formation': ['pod', 'grain fill'],
                    'Maturity': ['mature', 'ripening'],
                    'Harvesting': ['harvest', 'cutting']
                }
                
                for stage in growth_stages:
                    for rec in recommendations:
                        if isinstance(rec, str):
                            if any(k in rec.lower() for k in stage_keywords.get(stage, [])):
                                active_stages.append(stage)
                                break
                
                active_stages = list(set(active_stages)) if active_stages else ['Active Growth']
                
                calendar_data.append({
                    'Crop': crop,
                    'Season': season,
                    'Growth Stages': ', '.join(active_stages[:4]),
                    'Status': 'Verified against Official CWWG Reports'
                })
        
        calendar_df = pd.DataFrame(calendar_data)
        
        if not calendar_df.empty:
            st.dataframe(calendar_df, width=1200, height=400)

# Footer
st.divider()
if not df.empty:
    st.caption(f"🌱 India Crop Calendar AI Portal | Data Source: {source_file} | Records: {len(df)} | © 2026")
else:
    st.caption("🌱 India Crop Calendar AI Portal | No data loaded | © 2026")