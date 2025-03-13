# import re
# import nltk
# from nltk.corpus import stopwords
# from collections import Counter
import google.generativeai as genai
import asyncio

def extract_keywords_using_llm(text):
    # Initialize the gemini-1.5-flash model
    genai.configure("AIzaSyBS0aour5C2lCBJJV60Bq4uad82bFO0bqs")
    client = genai.GenerativeModel('gemini-1.5-flash')

    # Generate keywords using the gemini-1.5-flash model
    # Create a prompt to extract keywords for Google search
    prompt = f"""get the keywords out of the given text so as to make best search on google, return with just the text output only of text

Text: {text}"""
    response = client.generate_content(prompt)
    keywords = response

    return keywords

async def call_gemini(text):
    return await asyncio.to_thread(_call_gemini_sync, text)

def _call_gemini_sync(text):
    try:
        genai.configure(api_key="AIzaSyBS0aour5C2lCBJJV60Bq4uad82bFO0bqs")
        client = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""{text}"""
        response = client.generate_content(prompt)
        res = response.candidates[0].content.parts[0].text
        return res
    except Exception as error:
        print(f"Error in _call_gemini_sync: {error}")
        return ""