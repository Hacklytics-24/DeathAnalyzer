import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache
def load_data():
    df = pd.read_csv("cause_of_deaths.csv", delimiter=",")
    return df

# Main function to create the web application
def main():
    st.title("Health Concerns with Highest Percent Increase in Deaths by Country")

    # Load the data
    df = load_data()

    # Remove "Exposure to Forces of Nature" and "Conflict and Terrorism" from the dataframe
    df_filtered = df.drop(columns=["Exposure to Forces of Nature", "Conflict and Terrorism"])

    # Melt the filtered dataframe to have one row per (Country/Territory, Year) combination
    df_melted = df_filtered.melt(id_vars=['Country/Territory', 'Code', 'Year'], var_name='Health_Concern', value_name='Deaths')

    # Calculate percent increase in deaths for each health concern
    df_melted['Deaths_Pct_Change'] = df_melted.groupby(['Country/Territory', 'Health_Concern'])['Deaths'].pct_change() * 100

    # Find the health concern with the highest percent increase in deaths for each country
    max_increase = df_melted.groupby(['Country/Territory', 'Health_Concern'])['Deaths_Pct_Change'].max().reset_index()
    max_increase = max_increase.loc[max_increase.groupby('Country/Territory')['Deaths_Pct_Change'].idxmax()]

    # Merge with original dataframe to get additional information
    merged_df = max_increase.merge(df_melted, on=['Country/Territory', 'Health_Concern', 'Deaths_Pct_Change'], how='left')

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(merged_df, 
                        locations="Code", 
                        color="Health_Concern",
                        hover_name="Country/Territory",
                        hover_data=["Year", "Health_Concern", "Deaths"],
                        title="",
                        labels={'Health_Concern':'Health Concern'},
                        color_continuous_scale=px.colors.qualitative.Safe)

    # Show the map
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()