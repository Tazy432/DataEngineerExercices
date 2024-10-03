import requests
from tqdm import tqdm  # Progress bar
import pandas as pd
import zipfile
import os

# List of download URLs
download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",  # Invalid URL for testing
]

def download_file(url):
    folder_name = "downloads"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    file_name = url.split('/')[-1]
    file_path = os.path.join(folder_name, file_name)
    
    # Stream the download with a progress bar
    response = requests.get(url, stream=True)
    if response.status_code != 404:
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024  # 1 KB chunks
        with open(file_path, 'wb') as file:
            for data in tqdm(response.iter_content(chunk_size), total=total_size // chunk_size, unit='KB', desc=file_name):
                file.write(data)

        # Extract the zip file
        with zipfile.ZipFile(file_path, 'r') as extractor:
            extractor.extractall(folder_name)
        
        # Process extracted CSV files
        for extracted_file in extractor.namelist():
            if extracted_file.endswith('.csv'):
                csv_file_path = os.path.join(folder_name, extracted_file)
                try:
                    # Try to read with UTF-8 encoding first
                    df = pd.read_csv(csv_file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    # If UTF-8 fails, fall back to ISO-8859-1 encoding
                    print(f"UTF-8 failed for {extracted_file}, trying ISO-8859-1 encoding.")
                    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
                df.to_csv(csv_file_path, index=False)
        os.remove(file_path)
    else:
        print(f"The zipfile {file_name} does not exist.")

def main():
    for url in download_uris:
        download_file(url)

if __name__ == "__main__":
    main()
