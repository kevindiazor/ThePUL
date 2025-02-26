import os
import tempfile
import pandas as pd
from dropbox import Dropbox
from dropbox.files import FileMetadata, FolderMetadata
from typing import List, Dict, Optional
import streamlit as st

def get_dropbox_client():
    """Get authenticated Dropbox client"""
    access_token = st.secrets["dropbox"]["access_token"]
    return Dropbox(access_token)

def list_folder_contents(dbx, path: str = "") -> List[Dict]:
    """List contents of a Dropbox folder"""
    result = dbx.files_list_folder(path)
    
    files = []
    for entry in result.entries:
        if isinstance(entry, FileMetadata) and entry.name.endswith('.csv'):
            files.append({
                'path': entry.path_display,
                'name': entry.name,
                'size': entry.size
            })
            
    # Continue if there are more files
    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)
        for entry in result.entries:
            if isinstance(entry, FileMetadata) and entry.name.endswith('.csv'):
                files.append({
                    'path': entry.path_display,
                    'name': entry.name,
                    'size': entry.size
                })
                
    return files

def download_file(dbx, dropbox_path: str, local_path: Optional[str] = None) -> str:
    """Download a file from Dropbox to local storage"""
    if local_path is None:
        # Create a temporary file with the same name
        filename = os.path.basename(dropbox_path)
        local_path = os.path.join(tempfile.gettempdir(), filename)
        
    # Make sure the directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # Download the file
    dbx.files_download_to_file(local_path, dropbox_path)
    
    return local_path

def download_folder_files(folder_path: str = "/2024_game_day_info", local_dir: str = "game_data") -> List[str]:
    """Download all CSV files from a Dropbox folder"""
    dbx = get_dropbox_client()
    
    # List all CSV files in the folder
    all_files = list_folder_contents(dbx, folder_path)
    
    # Create local directory
    os.makedirs(local_dir, exist_ok=True)
    
    # Download each file
    downloaded_files = []
    for file_info in all_files:
        dropbox_path = file_info['path']
        local_path = os.path.join(local_dir, os.path.basename(dropbox_path))
        download_file(dbx, dropbox_path, local_path)
        downloaded_files.append(local_path)
        
    return downloaded_files

def read_csv_from_dropbox(file_path: str) -> pd.DataFrame:
    """Read a CSV file directly from Dropbox into a pandas DataFrame"""
    dbx = get_dropbox_client()
    
    # Download the file to a temporary location
    local_path = download_file(dbx, file_path)
    
    # Read the file
    df = pd.read_csv(local_path)
    
    # Clean up
    if os.path.exists(local_path):
        os.remove(local_path)
        
    return df
