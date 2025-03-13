from typing import Optional

from fastapi import FastAPI
import os
import json
import sys
# import redis
# from utils.extractKeywords import extract_keywords
# from utils.searchAndScrape import search_and_scrape_parallel
from utils.searchAndScrape import search_google, scrape_url_linkedin, scrape_url_reddit, collect_snapshots, polling_data_from_brightdata
from utils.extractKeywords import extract_keywords_using_llm
from utils.personaUtils import generate_answers_from_profile
from utils.indeedUtils import scrape_indeed_data

app = FastAPI()

# db = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search/")
async def search(search_query: str):
    search_results = search_google(search_query)
    return {"search_results": search_results}

@app.get("/extractKeywords/")
async def extract_keywords(search_query: str):
    keywords = extract_keywords_using_llm(search_query)
    return {"keywords": keywords}

@app.get("/searchAndScrape/")
async def searchAndScrape(search_query: str):
    search_results = search_google(search_query)
    # Create a clone of search_results
    search_results_clone = search_results.copy()
    # Extract Indeed related data from search results
    for item in search_results:
        for platform, links in item.items():
            # if platform == 'indeed':
                # tempData = await scrape_indeed_data(links)
                # search_results_clone[platform] = tempData
                # indeed_results.append(tempData)
            if platform == 'linkedin':
                # print(f"Linkedin links --> {links}\n\n")
                tempData = scrape_url_linkedin(links)
                # # Since search_results_clone is a list, we need to update the current item
                # # Find the index of the current result in the original list
                index = search_results.index(item)
                # # Update the corresponding item in the clone
                search_results_clone[index]['linkedin'] = tempData
            if platform == 'reddit':
                tempData = scrape_url_reddit(links)
                index = search_results.index(item)
                search_results_clone[index]['reddit'] = tempData
                
    
    collected_snapshots = collect_snapshots(search_results_clone)
    print(f"Collected snapshots --> {collected_snapshots}\n\n")
    
    finalResponse = await polling_data_from_brightdata(collected_snapshots);
    

    return {"search_results": search_results, "finalResponse": finalResponse}


@app.get("/pollingDataFromBrightdata/")
async def pollingDataFromBrightdata(snapshot_id: str = None):
    snapshot_ids = ['s_m87eg5u6eia8jhek9', 's_m87eg6nc18ce9l0jlx']
    response = await polling_data_from_brightdata(snapshot_ids)
    return {"response": response}
