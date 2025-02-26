import os
import pandas as pd
import streamlit as st
from typing import Tuple
from data_processing.main import process_dropbox_data
from data_generator import generate_all_data

# Use Streamlit cache to avoid redownloading data frequently
@st.cache_data(ttl=3600)  # Cache for 1 hour
def process_and_load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Process game data from Dropbox and load the results
    Falls back to sample data if processing fails
    """
    try:
        # Process the Dropbox folder
        process_dropbox_data("/2024_game_day_info")  # Adjust path based on your Dropbox structure

        # Load the processed data
        teams_df, players_df, games_df = load_stats_data()
        if all(df is not None for df in [teams_df, players_df, games_df]):
            return teams_df, players_df, games_df

        print("Using sample data as fallback...")
        return generate_all_data()

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return generate_all_data()
