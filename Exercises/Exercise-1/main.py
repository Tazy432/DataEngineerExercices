import requests
from tqdm import tqdm  # Progress bar
import os

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
    # Get the file name
    file_name = url.split('/')[-1]
    
    # Make the request with stream=True to download in chunks
    response = requests.get(url, stream=True)
    
    if response.status_code != 404:
        # Get the total file size from the headers (if available)
        total_size = int(response.headers.get('content-length', 0))

        # Open the file in binary write mode
        with open(file_name, "wb") as file:
            # Create a progress bar with tqdm
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name) as progress_bar:
                # Write the content in chunks
                for chunk in response.iter_content(chunk_size=1024):  # 1KB chunks
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))  # Update progress bar
    else:
        print(f"The zipfile {file_name} does not exist.")

def main():
    for url in download_uris:
        download_file(url)

if __name__ == "__main__":
    main()
