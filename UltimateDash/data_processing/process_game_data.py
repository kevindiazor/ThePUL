import pandas as pd
import os
import re
import zipfile
from typing import Dict, List, Tuple
from dropbox_utils import download_folder_files

def process_dropbox_game_files(dropbox_folder_path: str = "/2024_game_day_info", local_dir: str = "game_day_info"):
    """Process game files from Dropbox folder"""
    # Download all files from Dropbox
    downloaded_files = download_folder_files(dropbox_folder_path, local_dir)
    return local_dir

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

# Rest of your code remains the same
