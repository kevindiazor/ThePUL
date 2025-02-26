import pandas as pd
import os
import re
import zipfile
from typing import Dict, List, Tuple

def extract_game_files(zip_path: str, extract_path: str = "game_day_info"):
    """Extract game files from zip archive"""
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    return extract_path

def identify_game_info(file_path: str) -> Dict[str, str]:
    """Extract game information from file path and name"""
    path_parts = file_path.split(os.sep)

    # Extract week number
    week_match = re.search(r'(?:Week|WEEK)_?(\d+)', file_path)
    week = week_match.group(1) if week_match else None

    # Extract teams
    teams_match = re.search(r'(\w+)\s*@\s*(\w+)', path_parts[-2] if len(path_parts) > 1 else "")
    team1 = teams_match.group(1) if teams_match else None
    team2 = teams_match.group(2) if teams_match else None

    return {
        'week': week,
        'team1': team1,
        'team2': team2,
        'file_path': file_path
    }

def process_raw_stats(game_day_folder: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Process all raw game statistics files"""
    # Initialize empty lists for each stat type
    possessions = []
    player_stats = []
    defensive_blocks = []
    points = []
    passes = []

    # Walk through the game day folder
    for root, _, files in os.walk(game_day_folder):
        for file in files:
            if not file.endswith('.csv'):
                continue

            file_path = os.path.join(root, file)
            game_info = identify_game_info(file_path)

            try:
                df = pd.read_csv(file_path)
                df['match'] = f"{game_info['team1']} @ {game_info['team2']}"
                df['week'] = game_info['week']

                # Sort files into appropriate lists based on filename
                if 'Possession' in file:
                    possessions.append(df)
                elif 'Player Stats' in file:
                    player_stats.append(df)
                elif 'Defensive Blocks' in file or 'Defensive_Blocks' in file:
                    defensive_blocks.append(df)
                elif 'Points' in file:
                    points.append(df)
                elif 'Passes' in file:
                    passes.append(df)

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

    # Combine all dataframes
    return (
        pd.concat(possessions, ignore_index=True) if possessions else pd.DataFrame(),
        pd.concat(player_stats, ignore_index=True) if player_stats else pd.DataFrame(),
        pd.concat(defensive_blocks, ignore_index=True) if defensive_blocks else pd.DataFrame(),
        pd.concat(points, ignore_index=True) if points else pd.DataFrame(),
        pd.concat(passes, ignore_index=True) if passes else pd.DataFrame()
    )

def integrate_raw_game_data(zip_path: str, output_dir: str = "integ-data"):
    """Main function to process game files from zip"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Extract files
    game_day_folder = extract_game_files(zip_path)

    # Process raw stats
    possessions_df, player_stats_df, defensive_blocks_df, points_df, passes_df = process_raw_stats(game_day_folder)

    # Save processed data
    possessions_df.to_csv(os.path.join(output_dir, "Possessions.csv"), index=False)
    player_stats_df.to_csv(os.path.join(output_dir, "Player-Stats.csv"), index=False)
    defensive_blocks_df.to_csv(os.path.join(output_dir, "Defensive-Blocks.csv"), index=False)
    points_df.to_csv(os.path.join(output_dir, "Points.csv"), index=False)
    passes_df.to_csv(os.path.join(output_dir, "Passes.csv"), index=False)

if __name__ == "__main__":
    integrate_raw_game_data("2024_game_day_info.zip")