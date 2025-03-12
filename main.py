from typing import Optional

from fastapi import FastAPI
import os
import json
import sys
# from utils.extractKeywords import extract_keywords
from utils.searchAndScrape import search_and_scrape_parallel
from utils.searchAndScrape import search_google
from utils.extractKeywords import extract_keywords_using_llm
from utils.personaUtils import generate_answers_from_profile
from utils.indeedUtils import scrape_indeed_data

app = FastAPI()


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
        
    # Extract Indeed related data from search results
    indeed_results = []
    for result in search_results:
        if 'indeed' in result:
            indeed_results.extend(result['indeed'])
    
    # If there are Indeed results, scrape them
    if indeed_results:
        indeed_data = await scrape_indeed_data(indeed_results)
        return {"search_results": search_results, "indeed_data": indeed_data}

    return {"search_results": search_results}