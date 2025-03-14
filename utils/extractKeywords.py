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
        
        # Track request timestamps per API key
        if not hasattr(_call_gemini_sync, 'request_timestamps'):
            _call_gemini_sync.request_timestamps = {key: [] for key in api_keys}
            
        # Try each key until one works
        for attempt in range(len(api_keys) * 3):  # Allow multiple attempts
            key_index = attempt % len(api_keys)
            current_key = api_keys[key_index]
            
            # Check if we're within rate limits (15 requests per second per key)
            current_time = time.time()
            timestamps = _call_gemini_sync.request_timestamps[current_key]
            
            # Remove timestamps older than 1 second
            timestamps = [t for t in timestamps if current_time - t < 1.0]
            _call_gemini_sync.request_timestamps[current_key] = timestamps
            
            # If we have capacity with this key, use it
            if len(timestamps) < 15:
                genai.configure(api_key=current_key)
                client = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""{text}"""
                
                # Add timestamp before making request
                _call_gemini_sync.request_timestamps[current_key].append(current_time)
                
                try:
                    response = client.generate_content(prompt)
                    res = response.candidates[0].content.parts[0].text
                    return res
                except Exception as e:
                    # If this key fails, try the next one
                    print(f"Key {key_index} failed: {e}")
                    continue
            
            # If we're rate limited on this key, sleep a bit before trying the next one
            time.sleep(0.10)
            
        # If all attempts failed
        print("All API keys are rate limited or failing")
        return ""
    except Exception as error:
        print(f"Error in _call_gemini_sync: {error}")
        return ""
    