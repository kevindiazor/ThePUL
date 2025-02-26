import os
import pandas as pd
from typing import Tuple
from data_processing.main import process_zip_data
from data_generator import generate_all_data

def load_stats_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the processed statistics from the stats directory
    Returns:
        Tuple containing (teams_df, players_df, games_df)
    """
    try:
        # Load team stats
        teams_df = pd.read_csv('stats/team-stats-overall.csv')

        # Load player stats
        players_df = pd.read_csv('stats/player-stats-overall.csv')

        # Load game stats
        games_df = pd.read_csv('stats/team-stats-game.csv')

        return teams_df, players_df, games_df

    except Exception as e:
        print(f"Error loading statistics: {str(e)}")
        return None, None, None

def process_and_load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Process game data from zip file and load the results
    Falls back to sample data if processing fails
    """
    zip_path = "2024_game_day_info.zip"

    try:
        if os.path.exists(zip_path):
            # Process the zip file
            process_zip_data(zip_path)

            # Load the processed data
            teams_df, players_df, games_df = load_stats_data()
            if all(df is not None for df in [teams_df, players_df, games_df]):
                return teams_df, players_df, games_df

        print("Using sample data as fallback...")
        return generate_all_data()

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return generate_all_data()
