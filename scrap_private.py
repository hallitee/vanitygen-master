import requests
from bs4 import BeautifulSoup
import csv

# URL of the web page containing the table
url = 'https://privatekeys.pw/puzzles/bitcoin-puzzle-tx'

# Define a user agent to mimic a browser (you can change this to match a specific browser)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

# Set the user agent in the headers of the HTTP request
headers = {'User-Agent': user_agent}

# Send an HTTP GET request to the URL with the specified headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    

    # Find the table using HTML tag and class, adjust this based on the structure of the target webpage
    table = soup.find('table', {'class': 'table'})

    if table:
        # Initialize an empty list to store data
        data = []

        # Loop through the table rows
        rows = table.find_all('tr')
        # Remove the header row if necessary
        if len(rows) > 0 and rows[0]: 
            header = rows[0]
            rows = rows[1:]        
        for row in rows:
            cols = row.find_all('td')
            colls = []
            colls.append(cols[0].get_text(strip=True))
            colls.append(cols[1].get_text(strip=True).split("\n")[0].split("...")[1])
            colls.append(cols[2].get_text(strip=True))
            colls.append(cols[3].get_text(strip=True))
            colls.append(cols[4].get_text(strip=True))

            # cols = [col.get_text(strip=True) for col in cols]
            # # cols[1].get_text(strip=True).split("\n")[0].split("...")[1]
            data.append(colls)



        # Specify the CSV file name
        csv_file_name = 'scraped_data.csv'

        # Save the data to a CSV file
        with open(csv_file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            # if header:
            # csv_writer.writerow(header)  # Write the header row
            csv_writer.writerows(data)  # Write the data rows

        print(f"Data has been saved to {csv_file_name}")
    else:
        print("Table not found on the page.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
