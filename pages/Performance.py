import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_data
from utils.visualizations import plot_performance_vs_attendance

# Load data
df = load_data()

# Calculate performance statistics
avg_performance = df['A_Percentage'].mean()
performance_std = df['A_Percentage'].std()
performance_range = df['A_Percentage'].max() - df['A_Percentage'].min()

# Calculate correlation between performance and absenteeism
correlation = df[['A_Percentage', 'Absenteeism_Rate']].corr().iloc[0,1]

# District performance analysis
district_performance = df.groupby('DistrictName')['A_Percentage'].agg(['mean', 'count']).sort_values('mean', ascending=False)
top_district = district_performance.index[0]
bottom_district = district_performance.index[-1]
district_diff = district_performance['mean'].iloc[0] - district_performance['mean'].iloc[-1]

# Set up page
st.title("🎓 ACADEMIC PERFORMANCE ANALYSIS")
st.markdown("""
### Evidence-Based Insights on School Performance
Quantitative analysis of Grade "A" achievement patterns across Northern Uganda
""")

# Performance vs Attendance
st.header("Performance vs Absenteeism Relationship")
fig = plot_performance_vs_attendance(df)
st.plotly_chart(fig)

# Performance Statistics
st.header("Key Performance Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Grade 'A' %", f"{avg_performance:.1f}%")
col2.metric("Performance Range", f"{performance_range:.1f}%")
col3.metric("Performance Std Dev", f"{performance_std:.1f}%")

# Top performing schools
st.header("Top 10 Performing Schools")
top_schools = df.nlargest(10, 'A_Percentage')[['CentreName', 'DistrictName', 'A_Percentage', 'Total']]
st.dataframe(
    top_schools.style.format({'A_Percentage': '{:.1f}%', 'Total': '{:,}'}),
    height=400
)

# District performance comparison
st.header("District Performance Comparison")
st.dataframe(
    district_performance.style.format({'mean': '{:.1f}%'}),
    height=400
)

# Statistical Conclusions
st.header("📊 Statistical Findings")
st.markdown(f"""
1. **Attendance-Performance Relationship**: 
   - Correlation coefficient: {correlation:.2f}
   - {'Strong negative' if correlation < -0.5 else 'Moderate negative' if correlation < -0.3 else 'Weak negative' if correlation < 0 else 'No significant'} correlation between absenteeism and performance

2. **Performance Distribution**:
   - Average Grade "A" rate: {avg_performance:.1f}% ± {performance_std:.1f}%
   - Range: {performance_range:.1f}% between highest and lowest performing schools

3. **District Variations**:
   - Highest performing district: {top_district} ({district_performance['mean'].iloc[0]:.1f}%)
   - Lowest performing district: {bottom_district} ({district_performance['mean'].iloc[-1]:.1f}%)
   - Difference: {district_diff:.1f} percentage points
""")

# Practical Recommendations
st.header("🎯 Actionable Recommendations")
st.markdown(f"""
1. **For High-Performing Schools** ({top_district} district):
   - Document and share teaching methodologies from {top_schools.iloc[0]['CentreName']} (top performer at {top_schools.iloc[0]['A_Percentage']:.1f}%)
   - Establish peer learning programs with neighboring schools

2. **For Low-Performing Schools** ({bottom_district} district):
   - Implement targeted teacher training focusing on core subjects
   - Address absenteeism in schools showing >20% absentee rate
   - Pair with mentor schools from {top_district}

3. **Attendance Improvement**:
   - Prioritize schools where absenteeism >15% and performance <{avg_performance:.1f}%
   - Investigate transportation barriers in rural schools with high absenteeism

4. **Resource Allocation**:
   - Direct additional teaching materials to schools below {avg_performance - performance_std:.1f}% Grade "A" rate
   - Consider redistributing teaching staff to balance experience levels
""")

# Data Export
st.download_button(
    label="📥 Download Performance Data",
    data=df[['CentreName', 'DistrictName', 'A_Percentage', 'Absenteeism_Rate', 'Total']].to_csv(index=False),
    file_name='uganda_school_performance.csv',
    mime='text/csv'
)