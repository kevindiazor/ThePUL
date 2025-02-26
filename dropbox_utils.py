import os
import tempfile
import requests
import zipfile
from typing import Optional

def download_dropbox_file(dropbox_link: str, local_filename: Optional[str] = None) -> str:
    """
    Download a file from Dropbox shared link
    
    Args:
        dropbox_link: Dropbox shared link (make sure it's a direct download link)
        local_filename: Optional local filename to save to
    
    Returns:
        Path to the downloaded file
    """
    # Convert dropbox.com/s/ links to direct download links
    if 'dropbox.com/s/' in dropbox_link and '?dl=0' in dropbox_link:
        dropbox_link = dropbox_link.replace('?dl=0', '?dl=1')
    
    # If no filename provided, create a temporary file
    if not local_filename:
        temp_dir = tempfile.gettempdir()
        local_filename = os.path.join(temp_dir, "game_data.zip")
    
    # Download the file
    with requests.get(dropbox_link, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    
    return local_filename
