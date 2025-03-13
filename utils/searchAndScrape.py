import requests
import json
import os
import asyncio
import aiohttp
from datetime import datetime
from utils.extractKeywords import call_gemini


def fetch_google_search_results(query, g_api_key, cx, platform):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={g_api_key}&cx={cx}"
    
    try:
        response = requests.get(url)
        data = response.json()
        linkedin_profiles = []
        indeed_posts = []
        reddit_posts = []
        
        if 'items' in data:
            for item in data['items']:
                if platform == 'linkedin':
                    # Check if the link is a LinkedIn profile
                    def is_linkedin_profile(link):
                        # Check for LinkedIn domain and typical profile URL patterns
                        return ('linkedin.com/in/' in link or 
                                'linkedin.com/profile/' in link or
                                ('linkedin.com' in link and '/pub/' in link))
                    
                    # Add to profiles list if it's a LinkedIn profile
                    if is_linkedin_profile(item['link']):
                        obj = {
                            "url": item['link']
                        }
                        linkedin_profiles.append(obj)
                elif platform == 'indeed':
                    if 'indeed.com' in item['link']:
                        obj = {
                            "url": item['link']
                        }
                        indeed_posts.append(obj)
                        
                elif platform == 'reddit':
                    if 'reddit.com' in item['link']:
                        obj = {
                            "url": item['link']
                        }
                        reddit_posts.append(obj)
            if platform == 'linkedin':
                return linkedin_profiles
            elif platform == 'reddit':
                return reddit_posts
            elif platform == 'indeed':
                return indeed_posts
            else:
                return []
        else:
            print("No results found.")
            return []
    except Exception as error:
        print(f"Error fetching search results: {error}")
        return []

async def search_google(query):
    try:
        # Format the search query
        query = query.strip()
        query = ' '.join(query.split())
        
        # You would need to define these variables in your actual implementation
        g_api_key = 'AIzaSyDnM95rYauiANR6ox-GxZzJdocZArYpIH4'
        cx = 'c411373588b624d22'
        
        profileCollection = []
        llm_generated_queries = [];
        # Generate search queries for different platforms
        prompt = f"Generate keywords out of given Text: '{query}'. Return only the keywords, no explanations."
        response = await call_gemini(prompt)
        # print(f"response --> {response}")
        platforms = ["linkedin", "reddit", "indeed"]
        for i in range(1, 4):
            platform = platforms[i-1]
            response_to_use = response + f" {platform}"
            platform_query = str(response_to_use)
            llm_generated_queries.append(platform_query)
            # print(f"Generated query for {platform}: {platform_query}")
            profiles = fetch_google_search_results(platform_query, g_api_key, cx, platform)
            profileCollection.append({
                platform: profiles
            })
        # return llm_generated_queries
        # print(profiles)
        return profileCollection
    except Exception as error:
        print(f'Error: {error}')
        return []

def scrape_url(search_result):
    try:
        data = json.dumps(search_result)
        
        # You would need to define this variable in your actual implementation
        bdata_api_key = '836a937268c18af17d272771c5dc5f6b874a94ace55959dc0c5707418c746154'
        
        try:
            response = requests.post(
                "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_l1viktl72bvl7bjuj0&include_errors=true",
                headers={
                    "Authorization": f"Bearer {bdata_api_key}",
                    "Content-Type": "application/json"
                },
                data=data
            )
            response_data = response.json()
            return response_data
        except Exception as error:
            print(f"Error: {error}")
            return None
    except Exception as error:
        print(f'Error: {error}')
        return None

def search_and_scrape_parallel(query):
    print(f"Searching for: {query}")
    
    # First get search results
    search_results = search_google(query)
    print(f"search_results --> {search_results}")
    linkedin_data = scrape_url(search_results)
    
    # Store the scraped data in a file
    if linkedin_data:
        try:
            timestamp = datetime.now().isoformat().replace(':', '-')
            filename = f"scraped_data_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(linkedin_data, f, indent=2)
            
            print(f"Data successfully saved to {filename}")
            
            return {
                "searchResults": search_results,
                "linkedinData": linkedin_data,
                "savedTo": filename
            }
        except Exception as error:
            print(f'Error saving data to file: {error}')
            return {"searchResults": search_results}
    else:
        print('No data to save to file')
        return {"searchResults": search_results}
    
def scrape_url_linkedin(search_result):
    try:
        data = json.dumps(search_result)
        # You would need to define this variable in your actual implementation
        bdata_api_key = 'b1588c6901512843fa2122576118c81f8da15206ae533ffe792a05fbaba0ca93'
        
        try:
            response = requests.post(
                "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_l1viktl72bvl7bjuj0&include_errors=true",
                headers={
                    "Authorization": f"Bearer {bdata_api_key}",
                    "Content-Type": "application/json"
                },
                data=data
            )
            response_data = response.json()
            return response_data
        except Exception as error:
            print(f"Error: {error}")
            return None
    except Exception as error:
        print(f'Error: {error}')
        return None
    
def scrape_url_reddit(search_result):
    try:
        data = json.dumps(search_result)
        
        # You would need to define this variable in your actual implementation
        bdata_api_key = 'b1588c6901512843fa2122576118c81f8da15206ae533ffe792a05fbaba0ca93'
        try:
            response = requests.post(
                "https://api.brightdata.com/datasets/v3/trigger?dataset_id=gd_lvz8ah06191smkebj4&include_errors=true",
                headers={
                    "Authorization": f"Bearer {bdata_api_key}",
                    "Content-Type": "application/json"
                },
                data=data
            )
        except Exception as error:
            print(f"Error making request to Brightdata API: {error}")
            return None
        response_data = response.json()
        return response_data
        
    except Exception as error:
        print(f'Error: {error}')
        return None

def collect_snapshots(results):
    snapshots = []
    for item in results:
        for key, value in item.items():
            if isinstance(value, dict) and 'snapshot_id' in value:
                snapshots.append(value['snapshot_id'])
    return snapshots


async def polling_data_from_brightdata(snapshots):
    responses = []
    bdata_api_key = 'b1588c6901512843fa2122576118c81f8da15206ae533ffe792a05fbaba0ca93'
    
    async with aiohttp.ClientSession() as session:
        for snapshot in snapshots:
            url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot}"
            querystring = {"format":"json"}
            headers = {"Authorization": f"Bearer {bdata_api_key}"}
            
            max_retries = 10
            retry_delay = 30  # seconds
            
            for attempt in range(max_retries):
                try:
                    async with session.get(url, headers=headers, params=querystring) as response:
                        if response.status:
                            data = await response.json()
                            
                            if 'status' in data and data['status'] == 'running':
                                print(f"Attempt {attempt + 1}: Data still running for snapshot {snapshot}... Retrying in {retry_delay} seconds")
                                if attempt < max_retries - 1:
                                    await asyncio.sleep(retry_delay)
                                else:
                                    print(f"Max retries reached for snapshot {snapshot}. Moving to next snapshot.")
                                    # Add a partial response to indicate we tried but couldn't get complete data
                                    return [{ "status": "failed"}]
                                    responses.append({"snapshot_id": snapshot, "status": "timeout", "error": "Max retries reached"})
                            else:
                                responses.append(data)
                                break  # Exit the retry loop if we got a non-running status
                        else:
                            print(f"Error: HTTP status {response.status} for snapshot {snapshot}")
                            responses.append({"snapshot_id": snapshot, "status": "error", "http_status": response.status})
                            break
                except Exception as e:
                    print(f"Exception during API call for snapshot {snapshot}: {str(e)}")
                    if attempt == max_retries - 1:
                        responses.append({"snapshot_id": snapshot, "status": "error", "message": str(e)})
    
    return responses