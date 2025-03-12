import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
import google.generativeai as genai

# Download stopwords if not already available
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    nltk.download("punkt", quiet=True)
except:
    pass  # Handle case where downloads might fail (e.g., offline)

def extract_keywords(text, num_keywords=10):
    # Check if text is None or empty
    if not text:
        return []
        
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r"[^a-z\s]", "", text)

    # Tokenize words
    words = nltk.word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words and word.strip()]

    # Count word frequency
    word_counts = Counter(filtered_words)

    # Return top N keywords
    return " ".join([word for word, _ in word_counts.most_common(num_keywords)])

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

def call_gemini(text):
    genai.configure(api_key="AIzaSyBS0aour5C2lCBJJV60Bq4uad82bFO0bqs")
    client = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""{text}"""
    response = client.generate_content(prompt)
    res = response.candidates[0].content.parts[0].text
    return res