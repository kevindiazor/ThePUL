import streamlit as st
import pandas as pd
import plotly.express as px

st.title("League Standings")

# Calculate current standings
standings = []
for _, team in st.session_state.teams_df.iterrows():
    wins = team['wins']
    losses = team['losses']
    win_percentage = wins / (wins + losses) if (wins + losses) > 0 else 0
    
    standings.append({
        'team': team['name'],
        'wins': wins,
        'losses': losses,
        'win_percentage': win_percentage,
        'points_for': team['points_for'],
        'points_against': team['points_against'],
        'point_differential': team['points_for'] - team['points_against']
    })

standings_df = pd.DataFrame(standings)
standings_df = standings_df.sort_values('win_percentage', ascending=False)

# Display standings table
st.dataframe(
    standings_df.round(3),
    use_container_width=True
)

# Visualization of standings
st.subheader("Win-Loss Record")
fig = px.bar(
    standings_df,
    x='team',
    y=['wins', 'losses'],
    title="Team Records",
    barmode='group'
)
st.plotly_chart(fig, use_container_width=True)

# Point differential chart
st.subheader("Point Differential")
fig = px.bar(
    standings_df,
    x='team',
    y='point_differential',
    title="Team Point Differential",
    color='point_differential'
)
st.plotly_chart(fig, use_container_width=True)
