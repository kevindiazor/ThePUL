import os
from data_processing.process_game_data import process_dropbox_game_files, integrate_raw_game_data
from data_processing.calculate_statistics import main as calculate_stats

def process_dropbox_data(dropbox_folder: str = "/2024_game_day_info"):
    """Process game data from Dropbox folder"""
    # Step 1: Process raw game data
    print("Processing raw game data from Dropbox...")
    local_dir = process_dropbox_game_files(dropbox_folder, "game_day_info")

    # Step 2: Process the downloaded data
    integrate_raw_game_data(None, "integ-data", local_dir)  # Pass None for zip_path

    # Step 3: Calculate statistics
    print("Calculating season statistics...")
    calculate_stats()

    print("Data processing complete!")
