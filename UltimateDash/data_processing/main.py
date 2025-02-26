import os
from data_processing.process_game_data import integrate_raw_game_data
from data_processing.calculate_statistics import main as calculate_stats

def process_zip_data(zip_path: str):
    """Process game data from zip file"""
    # Step 1: Process raw game data
    print("Processing raw game data...")
    integrate_raw_game_data(zip_path, "integ-data")

    # Step 2: Calculate statistics
    print("Calculating season statistics...")
    calculate_stats()

    print("Data processing complete!")

if __name__ == "__main__":
    # Specify the path to your zip file
    zip_path = "2024_game_day_info.zip"

    if not os.path.exists(zip_path):
        print(f"Error: Zip file not found at {zip_path}")
    else:
        process_zip_data(zip_path)