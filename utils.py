import streamlit as st

def load_css():
    st.markdown("""
        <style>
        .stMetric {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 5px;
        }
        .stDataFrame {
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def calculate_team_stats(games_df, team_name):
    team_games = games_df[
        (games_df['team1'] == team_name) | 
        (games_df['team2'] == team_name)
    ]
    
    wins = 0
    total_points = 0
    
    for _, game in team_games.iterrows():
        if game['team1'] == team_name:
            total_points += game['team1_score']
            if game['team1_score'] > game['team2_score']:
                wins += 1
        else:
            total_points += game['team2_score']
            if game['team2_score'] > game['team1_score']:
                wins += 1
    
    return wins, len(team_games), total_points
