import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

def safe_load_data():
    """Wrapper with error handling for data loading"""
    try:
        return load_data()
    except Exception as e:
        st.error(f"❌ Data loading failed: {str(e)}")
        st.stop()
    return None

def main():
    st.title("MADI SUB-REGION ANALYSIS")
    st.markdown("### Focused Analysis of Adjumani and Moyo Districts")
    
    # Load data safely
    df = safe_load_data()
    
    # Validate data structure
    required_columns = {'DistrictName', 'Total'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        st.error(f"Missing required columns: {', '.join(missing)}")
        st.stop()
    
    # Filter for Madi sub-region (using uppercase to match your data)
    madi_districts = ['ADJUMANI', 'MOYO']
    available_districts = [d for d in madi_districts if d in df['DistrictName'].unique()]
    
    if not available_districts:
        st.warning("⚠️ No Madi sub-region districts found in data")
        st.stop()
    
    madi_df = df[df['DistrictName'].isin(available_districts)].copy()
    
    # Calculate key metrics
    total_schools = len(madi_df)
    total_students = madi_df['Total'].sum()
    avg_school_size = madi_df['Total'].mean()
    
    # Performance metrics (if available)
    if 'A_Percentage' in madi_df.columns:
        avg_performance = madi_df['A_Percentage'].mean()
        performance_by_district = madi_df.groupby('DistrictName')['A_Percentage'].mean()
        top_school = madi_df.loc[madi_df['A_Percentage'].idxmax()]
    
    # Overview metrics
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Schools", total_schools)
        col2.metric("Total Students", f"{total_students:,}")
        col3.metric("Avg School Size", f"{avg_school_size:.1f}")
    
    # District comparison tabs
    tab1, tab2 = st.tabs(["📊 Enrollment", "🏆 Performance"])
    
    with tab1:
        # Enrollment analysis
        enrollment_by_district = madi_df.groupby('DistrictName')['Total'].sum().reset_index()
        fig_enrollment = px.bar(enrollment_by_district,
                               x='DistrictName', y='Total', 
                               color='DistrictName',
                               title='Total Enrollment by District',
                               labels={'Total': 'Number of Students'})
        st.plotly_chart(fig_enrollment, use_container_width=True)
        
        # Enrollment insights
        st.subheader("Enrollment Insights")
        st.markdown(f"""
        - **{enrollment_by_district.iloc[0]['DistrictName']}** has {enrollment_by_district.iloc[0]['Total']:,} students across {len(madi_df[madi_df['DistrictName']==enrollment_by_district.iloc[0]['DistrictName']])} schools
        - **{enrollment_by_district.iloc[1]['DistrictName']}** has {enrollment_by_district.iloc[1]['Total']:,} students across {len(madi_df[madi_df['DistrictName']==enrollment_by_district.iloc[1]['DistrictName']])} schools
        - Average class size differs by {abs(madi_df[madi_df['DistrictName']==enrollment_by_district.iloc[0]['DistrictName']]['Total'].mean() - madi_df[madi_df['DistrictName']==enrollment_by_district.iloc[1]['DistrictName']]['Total'].mean()):.1f} students between districts
        """)
    
    with tab2:
        if 'A_Percentage' in madi_df.columns:
            # Performance analysis
            fig_performance = px.box(madi_df, 
                                   x='DistrictName', y='A_Percentage',
                                   color='DistrictName', 
                                   points="all",
                                   title='Academic Performance Distribution',
                                   labels={'A_Percentage': 'Grade "A" Percentage (%)'})
            st.plotly_chart(fig_performance, use_container_width=True)
            
            # Performance insights
            st.subheader("Performance Insights")
            st.markdown(f"""
            - **Top Performing School**: {top_school['CentreName']} ({top_school['DistrictName']}) with {top_school['A_Percentage']:.1f}% Grade "A"s
            - **District Averages**:
              - {performance_by_district.index[0]}: {performance_by_district.iloc[0]:.1f}%
              - {performance_by_district.index[1]}: {performance_by_district.iloc[1]:.1f}%
            - Performance gap between districts: {abs(performance_by_district.iloc[0] - performance_by_district.iloc[1]):.1f} percentage points
            """)
        else:
            st.warning("Performance data not available")
    
    # Actionable Recommendations
    st.header("🎯 Strategic Recommendations")
    if 'A_Percentage' in madi_df.columns:
        better_district = performance_by_district.idxmax()
        weaker_district = performance_by_district.idxmin()
        
        st.markdown(f"""
        1. **Knowledge Transfer Program**:
           - Establish mentorship between top-performing {better_district} schools and {weaker_district} schools
           - Focus on {top_school['CentreName']}'s best practices (achieving {top_school['A_Percentage']:.1f}% Grade "A"s)
        
        2. **Resource Allocation**:
           - Prioritize teaching materials to schools below {avg_performance:.1f}% Grade "A" rate
           - Balance teacher distribution (current range: {madi_df['Total'].min():,}-{madi_df['Total'].max():,} students per school)
        
        3. **District-Specific Interventions**:
           - {better_district}: Maintain excellence through advanced teacher training
           - {weaker_district}: Implement remedial programs targeting core subject weaknesses
        """)
    else:
        st.markdown("""
        1. **Enrollment-Based Planning**:
           - Optimize class sizes where enrollment exceeds district average
           - Consider redistricting for balanced school populations
        
        2. **Infrastructure Development**:
           - Prioritize expansions in schools nearing capacity
           - Upgrade facilities in oldest/most crowded schools first
        """)
    
    # Data download
    st.download_button(
        "📥 Download Madi Region Data",
        madi_df.to_csv(index=False),
        "madi_schools_data.csv",
        "text/csv"
    )

if __name__ == "__main__":
    main()