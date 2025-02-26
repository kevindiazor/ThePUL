import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.title("Team Statistics")

# Team selector
selected_team = st.selectbox(
    "Select Team",
    options=st.session_state.teams_df['name'].tolist()
)

# Display team stats
team_data = st.session_state.teams_df[st.session_state.teams_df['name'] == selected_team].iloc[0]

# Basic stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Wins", team_data['wins'])
with col2:
    st.metric("Losses", team_data['losses'])
with col3:
    win_pct = round(team_data['wins'] / (team_data['wins'] + team_data['losses']) * 100, 1)
    st.metric("Win %", f"{win_pct}%")
with col4:
    point_diff = team_data['points_for'] - team_data['points_against']
    st.metric("Point Differential", point_diff)

# Advanced stats
st.subheader("Advanced Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    break_pct = round(team_data['break_conversions'] / team_data['break_opportunities'] * 100, 1)
    st.metric("Break Conversion %", f"{break_pct}%")

with col2:
    red_zone_pct = round(team_data['red_zone_scores'] / team_data['red_zone_attempts'] * 100, 1)
    st.metric("Red Zone Efficiency", f"{red_zone_pct}%")

with col3:
    st.metric("Completion %", f"{round(team_data['completion_percentage'] * 100, 1)}%")

# Team roster with advanced stats
st.subheader("Team Roster")

# Add stat type selector
stat_type = st.radio(
    "Statistics Type",
    ["Basic Stats", "Advanced Stats", "Usage & Impact"],
    horizontal=True
)

team_players = st.session_state.players_df[st.session_state.players_df['team'] == selected_team]

if stat_type == "Basic Stats":
    display_cols = ['name', 'points', 'assists', 'blocks', 'turnovers']
elif stat_type == "Advanced Stats":
    display_cols = ['name', 'completion_percentage', 'throwing_yards', 'receiving_yards', 'red_zone_scores']
else:  # Usage & Impact
    display_cols = ['name', 'usage_rate', 'offensive_impact_score', 'handler_cutter_score', 'offense_defense_score']

st.dataframe(
    team_players[display_cols].sort_values('name'),
    use_container_width=True
)

# Team performance visualizations
st.subheader("Performance Analysis")

# Game flow chart
team_games = st.session_state.games_df[
    (st.session_state.games_df['team1'] == selected_team) |
    (st.session_state.games_df['team2'] == selected_team)
].copy()

# Process game data for visualization
team_games['score'] = team_games.apply(
    lambda x: x['team1_score'] if x['team1'] == selected_team else x['team2_score'],
    axis=1
)
team_games['opponent_score'] = team_games.apply(
    lambda x: x['team2_score'] if x['team1'] == selected_team else x['team1_score'],
    axis=1
)

# Create score trend chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=team_games['date'],
    y=team_games['score'],
    name='Team Score',
    line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=team_games['date'],
    y=team_games['opponent_score'],
    name='Opponent Score',
    line=dict(color='red')
))
fig.update_layout(
    title=f"{selected_team} Score Trends",
    xaxis_title="Date",
    yaxis_title="Score"
)
st.plotly_chart(fig, use_container_width=True)

# Player role distribution
st.subheader("Player Roles Distribution")
role_fig = px.scatter(
    team_players,
    x='handler_cutter_score',
    y='offense_defense_score',
    hover_data=['name'],
    labels={
        'handler_cutter_score': 'Handler (0) to Cutter (100)',
        'offense_defense_score': 'Offense (0) to Defense (100)'
    },
    title="Player Role Matrix"
)
st.plotly_chart(role_fig, use_container_width=True)