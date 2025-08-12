import streamlit as st
from utils.data_loader import load_data
from utils.visualizations import plot_missing_values

df = load_data()

st.title("🏫 DATASET OVERVIEW")
st.markdown("""
### Understanding the Northern Uganda Schools Dataset
This page provides an overview of the dataset structure, completeness, and basic statistics.
""")

# Basic info
st.header("Dataset Structure")
st.write(f"The dataset contains {len(df)} schools across {df['DistrictName'].nunique()} districts.")
st.dataframe(df.head())

# Missing values
st.header("Data Completeness")
st.markdown("""
The missing values matrix below shows patterns of data availability. 
White lines indicate missing values - we want to see as few as possible.
""")
st.pyplot(plot_missing_values(df))

# Statistics
st.header("Key Statistics")
st.dataframe(df.describe())

st.markdown("""
**Practical Conclusions:**
1. The dataset appears to have [describe completeness]
2. Key metrics like [important columns] show [interesting patterns]
3. Data quality is [good/needs improvement] for [specific aspects]
""")