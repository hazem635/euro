import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(page_title="EURO 2024", layout="wide")
st.title("EURO 2024")

# Load the dataset
path = r"Euro_2024_Team_Stats_Reduced.csv"
euro = pd.read_csv(path)

# Display a subheader
st.subheader("Germany 2024")

# Sidebar for filtering data
st.sidebar.header("Filter Data by Country(s):")
selected_teams = st.sidebar.multiselect("Choose the Country(s)", euro['team'].unique())

# Filter the DataFrame based on the selection
if selected_teams:
    filtered_data = euro[euro['team'].isin(selected_teams)]
else:
    filtered_data = euro
aggregated_data = filtered_data.groupby('team').sum().reset_index()

# Define a custom continuous blue color scale
blue_color_scale = [
    [0.0, 'rgb(0, 0, 255)'],   # blue
    [0.5, 'rgb(0, 128, 255)'], # lighter blue
    [1.0, 'rgb(173, 216, 230)'] # light blue (avoid white)
    
# Create the choropleth map
fig = px.choropleth(data_frame=aggregated_data,
                    locations='team',
                    locationmode='country names',
                    scope="europe",
                    color="goals_scored",
                    hover_name="team",
                    hover_data=["goals_scored", "Shots on target"],
                    color_continuous_scale=blue_color_scale)

fig.update_layout(coloraxis_colorbar={'title': 'Goals by team'},
                  margin={"r":0,"t":0,"l":0,"b":0},  # Remove margins
                  width=1200,  # Set a fixed width
                  height=700)  # Set a fixed height

fig.update_layout(coloraxis_colorbar={'title': 'Goals by Team'})
st.plotly_chart(fig, use_container_width=True)

# Display the filtered DataFrame
st.subheader(" Data")
st.dataframe(aggregated_data)

st.subheader("Percentage of Shots on Target to Total Shots for Each Team")

for team in selected_teams:
    team_data = aggregated_data[aggregated_data['team'] == team]
    if not team_data.empty:
        total_shots = team_data['Total shots'].values[0]
        shots_on_target = team_data['Shots on target'].values[0]
        missed_shots = total_shots - shots_on_target
        pie_data = pd.DataFrame({
            'Category': ['Shots on Target', 'Missed Shots'],
            'Count': [shots_on_target, missed_shots]
        })
        
        fig_pie = px.pie(data_frame=pie_data, names='Category', values='Count',
                         title=f'{team} - Shots on Target vs Total Shots',
                         labels={'Count': 'Number of Shots'})
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
# Correlation heatmap
st.subheader("Correlation Heatmap")
corr_columns = ['goals_scored', 'Total shots', 'Accurate passes', 'Keeper saves']
corr_data = aggregated_data[corr_columns].corr()

plt.figure(figsize=(10, 6))
heatmap = sns.heatmap(corr_data, annot=True, cmap='coolwarm', cbar=True, square=True, fmt='.2f')
plt.title('Correlation Heatmap')

st.pyplot(plt)
