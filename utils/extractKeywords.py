# import re
# import nltk
# from nltk.corpus import stopwords
# from collections import Counter
import google.generativeai as genai
import asyncio
import time

async def extract_keywords_using_llm(text):
    # Initialize the gemini-1.5-flash model
    # Use a list of API keys and rotate through them

    # Generate keywords using the gemini-1.5-flash model
    # Create a prompt to extract keywords for Google search
    prompt = f"""get the keywords out of the given text so as to make best search on google, return with just the text output only of text

    Text: {text}"""
    response = await call_gemini(prompt)

    return response

async def call_gemini(text):
    return await asyncio.to_thread(_call_gemini_sync, text)

def _call_gemini_sync(text):
    try:
        api_keys = [
            "AIzaSyBS0aour5C2lCBJJV60Bq4uad82bFO0bqs",
            "AIzaSyCeJ9TDbCFww4Ix-4VWzmX6K4uS_HbmeEY",
            "AIzaSyBtKRxMRkZKnwzqxo0rXuNLNPgVGsd03HM"
        ]
        key_index = int(time.time() * 100) % len(api_keys)
        genai.configure(api_key=api_keys[key_index])
        client = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""{text}"""
        response = client.generate_content(prompt)
        res = response.candidates[0].content.parts[0].text
        return res
    except Exception as error:
        print(f"Error in _call_gemini_sync: {error}")
        return ""