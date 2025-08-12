
import streamlit as st
from utils.data_loader import load_data
from datetime import datetime

# Configure the app
st.set_page_config(
    page_title="Northern Uganda Schools Analysis",
    page_icon="🏫",
    layout="wide"
)

@st.cache_resource(ttl=300)  # Refresh data every 5 minutes
def get_data():
    """Cached data loading with refresh capability"""
    try:
        return load_data()
    except Exception as e:
        st.error(f"Data loading failed: {str(e)}")
        st.stop()

def main():
    # Load data with progress indicator
    with st.spinner("Loading latest school data..."):
        df = get_data()
    
    # Sidebar - Data freshness indicator
    st.sidebar.markdown(f"**Data last loaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if st.sidebar.button("🔄 Refresh Data Now"):
        st.cache_data.clear()
        st.rerun()
    
    # Sidebar filters
    st.sidebar.title("Filters")
    selected_districts = st.sidebar.multiselect(
        "Select Districts",
        options=sorted(df['DistrictName'].unique()),
        default=sorted(df['DistrictName'].unique()),
        help="Filter schools by district"
    )
    
    # Filter data
    filtered_df = df[df['DistrictName'].isin(selected_districts)]
    
    # Main content
    st.title("🏫 Northern Uganda Schools Analysis (2024 UNEB Results)")
    st.markdown("""
    ### Interactive Education Dashboard
    Explore performance metrics and enrollment patterns across Northern Uganda schools.
    """)
    
    # Overview metrics with error handling
    try:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Schools", len(filtered_df), 
                   help="Number of schools in selected districts")
        col2.metric("Total Students", f"{filtered_df['Total'].sum():,}",
                   help="Combined enrollment across selected schools")
        col3.metric("Average School Size", f"{filtered_df['Total'].mean():.1f}",
                   delta=f"Range: {filtered_df['Total'].min()} - {filtered_df['Total'].max()}",
                   help="Mean student count per school")
    except Exception as e:
        st.warning(f"Could not display metrics: {str(e)}")
    
    # Navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    - [🏠 Overview](#)
    - [📊 Enrollment](#)
    - [🎓 Performance](#)
    - [🌍 Madi Sub-Region](#)
    """)
    
    # Data summary
    with st.expander("🔍 View Filtered Data"):
        st.dataframe(filtered_df.head(10), 
                    use_container_width=True,
                    hide_index=True)
        st.download_button(
            "📥 Download Current Data",
            filtered_df.to_csv(index=False),
            "filtered_schools_data.csv",
            "text/csv"
        )

if __name__ == "__main__":
    main()