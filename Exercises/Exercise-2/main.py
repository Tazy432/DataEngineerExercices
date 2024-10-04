import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL for the NOAA Local Climatological Data
url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a')

    # Iterate over links to find the target timestamp
    target_timestamp = "2022-02-07 14:03"
    file_link = None

    for link in links:
        href = link.get('href')
        if href and href.endswith('.csv'):
            # Scrape the modification date for each file
            modified_time = link.find_next('span')  # Assuming there is a span or similar tag with timestamp
            if modified_time and target_timestamp in modified_time.text:
                file_link = href
                break

    if file_link:
        print("File found:", file_link)
    else:
        print("No file found with the specified timestamp.")

else:
    print("Failed to retrieve the webpage.")
