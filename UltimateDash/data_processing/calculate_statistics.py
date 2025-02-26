import pandas as pd
import numpy as np
import os
from typing import Dict, Tuple

def calculate_team_statistics(points_df: pd.DataFrame, passes_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate team statistics both overall and per game"""
    # Overall team statistics
    team_goal_stats = points_df.groupby('team').agg({
        'Scored?': ['sum', 'count'],
        'Started on offense?': lambda x: sum((x == 1) & (points_df['Scored?'] == 1)),
        'Defensive blocks': 'sum',
        'Turnovers': 'sum'
    }).reset_index()

    team_pass_stats = passes_df.groupby('team').agg({
        'Turnover?': ['count', 'sum'],
        'Huck?': 'sum',
        'Forward distance (yd)': 'mean'
    }).reset_index()

    # Combine stats
    team_stats_overall = pd.merge(team_goal_stats, team_pass_stats, on='team')
    team_stats_overall.columns = [
        'team', 'goals', 'total_points', 'holds', 'blocks', 'turnovers',
        'pass_attempts', 'failed_passes', 'hucks', 'avg_throw_distance'
    ]

    # Calculate per-game statistics
    team_stats_game = points_df.groupby(['team', 'match', 'week']).agg({
        'Scored?': ['sum', 'count'],
        'Started on offense?': lambda x: sum((x == 1) & (points_df['Scored?'] == 1)),
        'Defensive blocks': 'sum',
        'Turnovers': 'sum'
    }).reset_index()

    return team_stats_overall, team_stats_game

def calculate_player_statistics(player_stats_df: pd.DataFrame, passes_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate player statistics both overall and per game"""
    # Overall player statistics
    player_stats_overall = player_stats_df.groupby(['Player', 'team']).agg({
        'Touches': 'sum',
        'Throws': 'sum',
        'Catches': 'sum',
        'Defensive blocks': 'sum',
        'Goals': 'sum',
        'Turnovers': 'sum',
        'Total completed throw gain (yd)': 'sum',
        'Total caught pass gain (yd)': 'sum',
        'Offense points played': 'sum',
        'Defense points played': 'sum',
        'Possessions initiated': 'sum',
        'Assists': 'sum'
    }).reset_index()

    # Calculate throwing and receiving averages from passes data
    throw_avg = passes_df[passes_df['Turnover?'] == 0].groupby('Thrower').agg({
        'Forward distance (yd)': 'mean'
    }).reset_index().rename(columns={'Thrower': 'Player', 'Forward distance (yd)': 'avg_throw_distance'})

    receive_avg = passes_df[passes_df['Turnover?'] == 0].groupby('Receiver').agg({
        'Forward distance (yd)': 'mean'
    }).reset_index().rename(columns={'Receiver': 'Player', 'Forward distance (yd)': 'avg_receive_distance'})

    # Merge averages into overall stats
    player_stats_overall = (player_stats_overall
        .merge(throw_avg, on='Player', how='left')
        .merge(receive_avg, on='Player', how='left'))

    # Per-game player statistics
    player_stats_game = player_stats_df.groupby(['Player', 'team', 'match', 'week']).agg({
        'Touches': 'sum',
        'Throws': 'sum',
        'Catches': 'sum',
        'Defensive blocks': 'sum',
        'Goals': 'sum',
        'Turnovers': 'sum',
        'Total completed throw gain (yd)': 'sum',
        'Total caught pass gain (yd)': 'sum',
        'Offense points played': 'sum',
        'Defense points played': 'sum',
        'Assists': 'sum'
    }).reset_index()

    return player_stats_overall, player_stats_game

def main():
    """Process all statistics and save results"""
    # Create stats directory
    os.makedirs('stats', exist_ok=True)

    try:
        # Read integrated data
        points_df = pd.read_csv('integ-data/Points.csv')
        passes_df = pd.read_csv('integ-data/Passes.csv')
        player_stats_df = pd.read_csv('integ-data/Player-Stats.csv')

        # Calculate team statistics
        team_stats_overall, team_stats_game = calculate_team_statistics(points_df, passes_df)

        # Calculate player statistics
        player_stats_overall, player_stats_game = calculate_player_statistics(player_stats_df, passes_df)

        # Save processed statistics
        team_stats_overall.to_csv('stats/team-stats-overall.csv', index=False)
        team_stats_game.to_csv('stats/team-stats-game.csv', index=False)
        player_stats_overall.to_csv('stats/player-stats-overall.csv', index=False)
        player_stats_game.to_csv('stats/player-stats-game.csv', index=False)

    except Exception as e:
        print(f"Error processing statistics: {str(e)}")

if __name__ == "__main__":
    main()