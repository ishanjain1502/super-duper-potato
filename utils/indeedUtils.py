import requests
import json
import os

async def scrape_indeed_data(indeed_results):    
    # password = ishan1502HaHaHaHa_
    # username = "ishan_FB3Np"
    
    # Initialize list to store scraped data
    scraped_data = []
    print(f"indeed_results --> yahan tk pahunch gaya")
    # Loop through each Indeed URL
    for i, result in enumerate(indeed_results):
        try:
            # Prepare the API request
            url = "https://realtime.oxylabs.io/v1/queries"
            payload = {
                "source": "universal",
                "url": result["url"]
            }
            
            # Set up authentication
            auth = ("ishan_FB3Np", "ishan1502HaHaHaHa_")
            
            # Set headers
            headers = {
                "Content-Type": "application/json"
            }
            
            # Make the API request
            print(f"payload --> {payload}")
            response = requests.post(
                url,
                auth=auth,
                headers=headers,
                json=payload
            )
            print(f"response --> {response}")
            # Check if request was successful
            if response.status_code == 200:
                # Parse the response
                data = response.json()
                scraped_data.append(data)
                print(f"Successfully scraped data for URL {i+1}/{len(indeed_results)}: {result['url']}")
            else:
                print(f"Failed to scrape URL {i+1}/{len(indeed_results)}: {result['url']} - Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error scraping URL {i+1}/{len(indeed_results)}: {result['url']} - Error: {str(e)}")
    
    # Return the scraped data
    return scraped_data
