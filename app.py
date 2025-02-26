import streamlit as st
import pandas as pd
from data_loader import process_and_load_data
from utils import load_css

# Page config
st.set_page_config(
    page_title="Ultimate Frisbee League Stats",
    page_icon="🥏",
    layout="wide"
)

# Load custom CSS
load_css()

# Add refresh button in sidebar
with st.sidebar:
    st.title("Data Controls")
    if st.button("🔄 Refresh Data"):
        st.session_state.data_loaded = False
        st.rerun()

# Initialize session state for data
if 'data_loaded' not in st.session_state:
    with st.spinner("Loading latest statistics..."):
        st.session_state.teams_df, st.session_state.players_df, st.session_state.games_df = process_and_load_data()
        st.session_state.data_loaded = True

# Main page
st.title("🥏 Ultimate Frisbee League Statistics")

# Dashboard overview
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Teams", len(st.session_state.teams_df))

with col2:
    st.metric("Total Players", len(st.session_state.players_df))

with col3:
    st.metric("Games Played", len(st.session_state.games_df))

# Recent games
st.subheader("Recent Games")
recent_games = st.session_state.games_df.sort_values('date', ascending=False).head(5)
st.dataframe(
    recent_games[['date', 'team1', 'team1_score', 'team2', 'team2_score']],
    use_container_width=True
)

# Top performers
st.subheader("Top Performers")
top_players = st.session_state.players_df.nlargest(5, 'points')
st.dataframe(
    top_players[['name', 'team', 'points', 'assists', 'completions']],
    use_container_width=True
)

# Add data source information
st.sidebar.markdown("---")
st.sidebar.info("""
Data is processed from game statistics files stored in Google Drive.
Click the refresh button to load the latest data.
""")
