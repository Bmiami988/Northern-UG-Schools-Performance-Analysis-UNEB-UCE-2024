import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data(ttl=10)  # Refresh every 10 seconds
def load_data():
    """Load data with automatic refresh when file changes"""
    data_path = Path(__file__).parent.parent / "data" / "northern_uganda_schools.csv"
    
    try:
        df = pd.read_csv(data_path)
        df.columns = df.columns.str.strip()
        
        # Calculate metrics
        if 'Total' in df.columns and 'As' in df.columns:
            df['A_Percentage'] = (df['As'] / df['Total']) * 100
        if 'Absent' in df.columns and 'Total' in df.columns:
            df['Absenteeism_Rate'] = (df['Absent'] / df['Total']) * 100
            
        return df
    except Exception as e:
        st.error(f"⚠️ Failed to load data: {str(e)}")
        return pd.DataFrame()  # Return empty dataframe as fallback