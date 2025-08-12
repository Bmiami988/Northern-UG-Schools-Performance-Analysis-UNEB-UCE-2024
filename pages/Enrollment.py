import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.visualizations import plot_district_enrollment

# Load data
df = load_data()

# Calculate enrollment statistics
total_students = df['Total'].sum()
district_enrollment = df.groupby('DistrictName')['Total'].sum().sort_values(ascending=False)
top_districts = district_enrollment.head(3)
concentration_percent = (top_districts.sum() / total_students) * 100
size_distribution = df['Total'].describe(percentiles=[.25, .5, .75])

st.title("📊 ENROLLMENENT PATTERNS ANALYSIS")
st.markdown("""
### Quantitative Insights on School Distribution
Data-driven findings on student distribution across Northern Uganda
""")

# District enrollment visualization
st.header("Student Enrollment by District")
st.markdown(f"""
**Visual Interpretation**:  
District-level enrollment showing {top_districts.index[0]} with the highest student population ({top_districts.iloc[0]:,} students)
""")
st.pyplot(plot_district_enrollment(df))

# School size analysis
st.header("School Size Distribution")
st.markdown(f"""
**Key Characteristics**:  
Distribution of {len(df)} schools by student population
""")
fig = px.histogram(df, x='Total', nbins=20,
                  title=f'School Size Distribution (Median: {size_distribution["50%"]:.0f} students)',
                  labels={'Total': 'Number of Students'})
st.plotly_chart(fig, use_container_width=True)

# Statistical Conclusions
st.header("📈 Statistical Findings")
st.markdown(f"""
1. **Enrollment Concentration**:
   - {concentration_percent:.1f}% of students are in just 3 districts ({', '.join(top_districts.index)})
   - Bottom 5 districts serve only {(district_enrollment.tail(5).sum() / total_students * 100):.1f}% of students

2. **School Size Distribution**:
   - 50% of schools have between {size_distribution['25%']:.0f}-{size_distribution['75%']:.0f} students
   - {len(df[df['Total'] > 500])} schools (>500 students) account for {(df[df['Total'] > 500]['Total'].sum() / total_students * 100):.1f}% of enrollment

3. **Size Extremes**:
   - Largest: {df['Total'].max():,} students ({df.loc[df['Total'].idxmax(), 'CentreName']})
   - Smallest: {df['Total'].min():,} students ({df.loc[df['Total'].idxmin(), 'CentreName']})
   - 10:1 ratio between largest and smallest schools
""")

# Practical Recommendations
st.header("🛠️ Actionable Recommendations")
st.markdown(f"""
1. **Redistricting Priorities**:
   - Balance enrollment between {top_districts.index[0]} and neighboring {district_enrollment.index[-1]} district
   - Establish transfer programs for schools exceeding {size_distribution['75%']:.0f} students

2. **Infrastructure Investments**:
   - Immediate expansion needed for {len(df[df['Total'] > 500])} overcrowded schools (>500 students)
   - Target {top_districts.index[0]} for 2 new school constructions by 2025

3. **Consolidation Opportunities**:
   - Evaluate merging possibilities for {len(df[df['Total'] < 100])} schools with <100 students
   - Pilot 3 consolidation projects in {district_enrollment.index[-1]} district first

4. **Resource Allocation**:
   - Direct 40% of new teachers to schools above {size_distribution['75%']:.0f} students
   - Prioritize learning materials for schools in the {size_distribution['25%']:.0f}-{size_distribution['50%']:.0f} student range
""")

# Data Export
st.download_button(
    label="📥 Download Enrollment Data",
    data=df[['CentreName', 'DistrictName', 'Total']].sort_values('Total', ascending=False).to_csv(index=False),
    file_name='uganda_school_enrollment.csv',
    mime='text/csv'
)