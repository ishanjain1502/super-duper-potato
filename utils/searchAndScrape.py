import requests
import json
import os
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
            print("Search Results:")
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

def search_google(query):
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
        response = call_gemini(prompt)
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
            print(f"responseData --> {response_data}")
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