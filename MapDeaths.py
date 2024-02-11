import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset

def load_data():
    df = pd.read_csv("cause_of_deaths.csv", delimiter=",")
    return df

# Main function to create the web application
def set_dark_mode():
    # Custom HTML and CSS to set dark mode
    dark_mode_html = """
        <style>
            body {
                background-color: #1E1E1E;
                color: white;
            }
            .stApp {
                color: white;
            }
        </style>
    """
    st.markdown(dark_mode_html, unsafe_allow_html=True)

def main():
    st.title("Death Analysis of Every Country")

    # Load the data
    df = load_data()

    # Figure 1: Calculate total deaths for each country
    df['Total_Deaths'] = df.iloc[:, 3:].sum(axis=1)

    # Create a choropleth map using Plotly Express
    fig1 = px.choropleth(df,
                         locations="Country/Territory",
                         locationmode='country names',
                         color="Total_Deaths",
                         hover_name="Country/Territory",
                         color_continuous_scale=px.colors.sequential.Plasma)
    # Increase the title size and add an annotation
    fig1.update_layout(
        title=dict(
            text="Total Deaths by Country",
            font=dict(size=24)  # Adjust the size as needed
        )
    )

    # Description
    fig1.add_annotation(
        text="Total deaths based on various diseases, disorders, and accidents",
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.1,
        font=dict(size=15)
    )

    # Show the map
    st.plotly_chart(fig1)

    # Figure 2 Getting highest health concern

    # Remove "Exposure to Forces of Nature" and "Conflict and Terrorism" from the dataframe
    df_filtered = df.drop(columns=["Exposure to Forces of Nature", "Conflict and Terrorism"])

    # Melt the filtered dataframe to have one row per (Country/Territory, Year) combination
    df_melted = df_filtered.melt(id_vars=['Country/Territory', 'Code', 'Year'], var_name='Health_Concern',
                                 value_name='Deaths')

    # Calculate percent increase in deaths for each health concern
    df_melted['Deaths_Pct_Change'] = df_melted.groupby(['Country/Territory', 'Health_Concern'])[
                                         'Deaths'].pct_change() * 100

    # Find the health concern with the highest percent increase in deaths for each country
    max_increase = df_melted.groupby(['Country/Territory', 'Health_Concern'])['Deaths_Pct_Change'].max().reset_index()
    max_increase = max_increase.loc[max_increase.groupby('Country/Territory')['Deaths_Pct_Change'].idxmax()]

    # Merge with original dataframe to get additional information
    merged_df = max_increase.merge(df_melted, on=['Country/Territory', 'Health_Concern', 'Deaths_Pct_Change'],
                                   how='left')
    # Create a choropleth map using Plotly Express
    fig2 = px.choropleth(merged_df,
                        locations="Country/Territory",
                        locationmode='country names',
                        color="Health_Concern",
                        hover_name="Country/Territory",
                        hover_data=["Deaths"],
                        color_continuous_scale=px.colors.qualitative.Safe)
    # Increase the title size and add an annotation
    fig2.update_layout(
        title=dict(
            text="Health Concerns with Highest Percent Increase<br>in Deaths by Country",
            font=dict(size=24)  # Adjust the size as needed
        )
    )
    # Description
    fig2.add_annotation(
        text="Fastest-growing health concern in the last 20 years.",
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.1,
        font=dict(size=15)
    )
    # Show the map
    st.plotly_chart(fig2)

    # Dropdown for selecting a specific country
    selected_country = st.selectbox("Select a Country", df['Country/Territory'].unique())

    # Display causes of deaths and their numbers for the selected country
    st.header(f"Top Causes of Deaths in {selected_country}")

    # Filter the dataframe for the selected country
    selected_country_df_2019 = df[(df['Country/Territory'] == selected_country) & (df['Year'] == 2019)]
    # Display the filtered data
    st.write(selected_country_df_2019)

if __name__ == "__main__":
    main()
    # Set dark mode
    set_dark_mode()