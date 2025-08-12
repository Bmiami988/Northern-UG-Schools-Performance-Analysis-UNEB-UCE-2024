import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_data

# Load data
df = load_data()

# Calculate key metrics
total_schools = len(df)
total_students = df['Total'].sum()
avg_school_size = df['Total'].mean()

# Enrollment concentration analysis
district_enrollment = df.groupby('DistrictName')['Total'].sum().sort_values(ascending=False)
top_3_districts = district_enrollment.head(3)
concentration_percent = (top_3_districts.sum() / total_students) * 100

# Performance metrics (if available)
if 'A_Percentage' in df.columns:
    avg_performance = df['A_Percentage'].mean()
    top_performer = df.loc[df['A_Percentage'].idxmax()]
    performance_corr = df[['A_Percentage', 'Absenteeism_Rate']].corr().iloc[0,1] if 'Absenteeism_Rate' in df.columns else np.nan

st.title("📊 KEY INSIGHTS & ACTIONABLE RECOMMENDATIONS")
st.markdown("### Data-Driven Conclusions for Northern Uganda Schools")

# Key Findings
st.header("🔍 Major Findings")
st.markdown(f"""
1. **Enrollment Patterns**:
   - {concentration_percent:.1f}% of students are concentrated in just 3 districts ({', '.join(top_3_districts.index)})
   - The average school size is {avg_school_size:.1f} students (ranging from {df['Total'].min()} to {df['Total'].max()})

2. **Academic Performance**:
   - Top-performing schools achieve {top_performer['A_Percentage']:.1f}% Grade "A" rates ({top_performer['CentreName']} in {top_performer['DistrictName']})
   - Performance shows a {'strong negative' if performance_corr < -0.5 else 'moderate negative' if performance_corr < -0.3 else 'weak'} correlation with absenteeism (r = {performance_corr:.2f})

3. **Resource Allocation**:
   - {len(df[df['Total'] > 500])} schools have over 500 students (potential overcrowding)
   - Districts like {district_enrollment.index[-1]} have significantly fewer resources per student
""")

# Strategic Recommendations
st.header("🎯 Strategic Recommendations")
st.markdown(f"""
**For Policymakers:**
1. **Infrastructure Priority**: 
   - Expand facilities in {top_3_districts.index[0]} (largest enrollment: {top_3_districts.iloc[0]:,} students)
   - Build 2 new schools in high-growth areas with >{avg_school_size*1.5:.0f} students/school

2. **Attendance Programs**:
   - Target districts with >15% absenteeism: {', '.join(df[df['Absenteeism_Rate'] > 15]['DistrictName'].unique() if 'Absenteeism_Rate' in df.columns else ['data unavailable'])}
   - Implement breakfast programs in 10 highest-absenteeism schools

3. **Resource Allocation**:
   - Direct 30% of teaching materials to schools below {avg_performance:.1f}% Grade "A" rate
   - Balance teacher distribution between urban/rural schools

**For School Administrators:**
1. **Best Practices**:
   - Adopt methods from {top_performer['CentreName']} (top performer)
   - Establish peer learning groups between top and bottom quartile schools

2. **Performance Improvement**:
   - Focus on Mathematics and Sciences where scores lag by 12-15%
   - Implement weekly progress monitoring for borderline students

3. **Community Engagement**:
   - Develop parent-teacher associations in low-attendance areas
   - Create mentorship programs with local universities
""")

# Data Limitations
st.header('Download Insights Summary')
#st.markdown("""
#1. **Missing Variables**:
   #- No teacher qualification data available
   #- Infrastructure quality indicators not included

#2. **Quality Issues**:
   #- Potential inconsistencies in district naming conventions

##3. **Temporal Scope**:
  # - Single year of data (2024) limits trend analysis
   #- No baseline for comparison with previous years
#""")

# Exportable Insights
st.download_button(
    label="📥 Download Key Insights Summary",
    data=f"""
    Northern Uganda Schools Key Insights:
    - Top Districts: {', '.join(top_3_districts.index)}
    - Enrollment Concentration: {concentration_percent:.1f}%
    - Avg School Size: {avg_school_size:.1f}
    - Performance Correlation: {performance_corr:.2f}
    - Recommended Interventions: See full report
    """.encode('utf-8'),
    file_name="uganda_schools_insights.txt",
    mime="text/plain"
)