import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import missingno as msno

def plot_district_enrollment(df):
    """Plot student enrollment by district"""
    district_totals = df.groupby('DistrictName')['Total'].sum().sort_values()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=district_totals.values, y=district_totals.index,hue=district_totals.index, palette='viridis', legend=False)
    plt.title('Total Students by District')
    plt.xlabel('Number of Students')
    plt.ylabel('District')
    return fig

def plot_performance_vs_attendance(df):
    """Scatter plot of academic performance vs absenteeism"""
    fig = px.scatter(df, x='A_Percentage', y='Absenteeism_Rate',
                     color='DistrictName', size='Total',
                     title='Academic Performance vs Absenteeism Rate',
                     labels={'A_Percentage': 'Grade "A" Percentage (%)',
                            'Absenteeism_Rate': 'Absenteeism Rate (%)'})
    return fig

def plot_missing_values(df):
    """Visualize missing values in the dataset"""
    fig, ax = plt.subplots(figsize=(10, 4))
    msno.matrix(df, color=(0.2, 0.5, 0.7), ax=ax, sparkline=False)
    plt.title('Missing Values Pattern')
    return fig