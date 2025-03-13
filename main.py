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
# from utils.indeedUtils import scrape_indeed_data

app = FastAPI()

# db = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search/")
async def search(search_query: str):
    search_results = await search_google(search_query)
    return {"search_results": search_results}

@app.get("/extractKeywords/")
async def extract_keywords(search_query: str):
    keywords = extract_keywords_using_llm(search_query)
    return {"keywords": keywords}

@app.get("/searchAndScrape/")
async def searchAndScrape(search_query: str):
    search_results = await search_google(search_query)
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
                index = search_results.index(item)
                search_results_clone[index]['linkedin'] = tempData
            # if platform == 'reddit':
            #     tempData = scrape_url_reddit(links)
            #     index = search_results.index(item)
            #     search_results_clone[index]['reddit'] = tempData
                
    
    collected_snapshots = collect_snapshots(search_results_clone)
    print(f"Collected snapshots --> {collected_snapshots}\n\n")
    
    finalResponse = await polling_data_from_brightdata(collected_snapshots)
    if finalResponse[0].get('status') == 'failed':
        return {"data": "scraping results failed on bridght data"}
    
    # Define feature questions for persona generation
    featureQuestions = [
    {
      "category": "Behavior",
      "requirement": "Variable",
      "subCategory": "Preferred device and platform",
      "description": "What are the OS and device preferences of these users?",
      "options": [{ "label": "iOS" }, { "label": "Android" }, { "label": "windows" }]
    },
    {
      "category": "Learning and cognitive",
      "requirement": "Variable",
      "subCategory": "Tolerance for Trial and Error",
      "description":
        "What's their comfort level with experimenting when using a new interface?",
      "options": [
        { "label": "Very low comfort" },
        { "label": "Low comfort" },
        { "label": "Moderate Comfort" },
        { "label": "High Comfort" }
      ]
    },
    {
      "category": "Environmental ",
      "requirement": "Variable",
      "subCategory": "General tool usage",
      "description": "What's the tools these users use on a regular basis?",
      "options": [
        { "label": "Zoho" },
        { "label": "Slack" },
        { "label": "Microsoft Teams" }
      ]
    },
    {
      "category": "Demographic and contextual",
      "requirement": "Fixed",
      "subCategory": "Age",
      "description": "Age range of the target users",
      "options": [
        { "label": "18-24" },
        { "label": "25-34" },
        { "label": "35-44" },
        { "label": "45-54" },
        { "label": "55+" },
      ],
    },
    {
      "category": "Demographic and contextual",
      "requirement": "Fixed",
      "subCategory": "Gender",
      "description": "Gender distribution of users",
      "options": [
        { "label": "Male" },
        { "label": "Female" },
        { "label": "Non-binary" },
        { "label": "Prefer not to say" },
      ],
    },
    {
      "category": "Demographic and contextual",
      "requirement": "Variable",
      "subCategory": "Education Level",
      "description": "Highest level of education completed",
      "options": [
        { "label": "High School" },
        { "label": "Bachelor's" },
        { "label": "Master's" },
        { "label": "PhD" }
      ]
    },
    {
      "category": "Demographic and contextual",
      "requirement": "Variable",
      "subCategory": "Tech Savviness",
      "description": "Level of technological proficiency",
      "options": [
        { "label": "Beginner" },
        { "label": "Intermediate" },
        { "label": "Advanced" },
        { "label": "Expert" }
      ],
    },
    {
      "category": "Experience and familiarity",
      "requirement": "Variable",
      "subCategory": "Domain Expertise",
      "description": "Level of expertise in the relevant domain",
      "options": [
        { "label": "Novice" },
        { "label": "Intermediate" },
        { "label": "Expert" }
      ]
    },
    {
      "category": "Environmental ",
      "requirement": "Variable",
      "subCategory": "Device Usage",
      "description": "Primary devices used",
      "options": [
        { "label": "Desktop" },
        { "label": "Laptop" },
        { "label": "Tablet" },
        { "label": "Mobile" }
      ]
    },
    {
      "category": "Privacy & safety",
      "requirement": "Variable",
      "subCategory": "Data Sensitivity",
      "description": "Level of data privacy concerns",
      "options": [
        { "label": "Very concerned" },
        { "label": "Moderately concerned" },
        { "label": "Slightly concerned" },
        { "label": "Not concerned" }
      ]
    },
    {
      "category": "Decision making",
      "requirement": "Variable",
      "subCategory": "Decision Style",
      "description": "Approach to making decisions",
      "options": [
        { "label": "Analytical" },
        { "label": "Intuitive" },
        { "label": "Collaborative" },
        { "label": "Directive" }
      ]
    }
  ]
    
    # Process each profile in finalResponse to generate persona answers
    persona_results = []
    for platform_data in finalResponse:
        for profile in platform_data:
            # print(f"Profile --> {profile}\n\n")
            answers = await generate_answers_from_profile(profile, featureQuestions)
            persona_results.append({
                "profile": profile.get('url'),
                "persona_answers": answers
            })

    return {"persona_results": persona_results}


@app.get("/pollingDataFromBrightdata/")
async def pollingDataFromBrightdata(snapshot_id: str = None):
    snapshot_ids =  ['s_m87fh8av2ec7bmcs9o', 's_m87fh8iuuf1qd5oen']
    response = await polling_data_from_brightdata(snapshot_ids)
    
    return {"response": response}