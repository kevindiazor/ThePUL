import streamlit as st
import pandas as pd

st.title("Game Results")

# Week filter
week_numbers = sorted(st.session_state.games_df['week'].unique())
selected_week = st.selectbox(
    "Select Week",
    options=week_numbers,
    format_func=lambda x: f"Week {x}"
)

# Filter games by selected week
filtered_games = st.session_state.games_df[st.session_state.games_df['week'] == selected_week]

# Display games for the selected week
st.subheader(f"Week {selected_week} Games")

for _, game in filtered_games.iterrows():
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.write(game['team1'])
    with col2:
        st.write(f"{game['team1_score']} - {game['team2_score']}")
    with col3:
        st.write(game['team2'])

    # Add game details in an expander
    with st.expander("Game Details"):
        # Create two columns for team stats
        team1_col, team2_col = st.columns(2)

        with team1_col:
            st.subheader(game['team1'])
            st.write(f"Breaks: {game['team1_breaks']}")
            st.write(f"Turnovers: {game['team1_turnovers']}")
            st.write(f"Completion %: {game['team1_completion_pct']*100:.1f}%")
            st.write(f"Total Yards: {game['team1_yards']}")

        with team2_col:
            st.subheader(game['team2'])
            st.write(f"Breaks: {game['team2_breaks']}")
            st.write(f"Turnovers: {game['team2_turnovers']}")
            st.write(f"Completion %: {game['team2_completion_pct']*100:.1f}%")
            st.write(f"Total Yards: {game['team2_yards']}")

    st.divider()