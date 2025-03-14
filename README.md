# API Live Link

You can access the live API at the following link:

[Live API](https://featurely-draft1.onrender.com/)

Available routes write now:

"""
API Endpoints:

1. @app.get("/search/")
    - **Description**: This endpoint performs a search operation using the provided search query.
    - **Parameters**: 
      - `search_query` (str): The query string to search for.
    - **Returns**: A JSON object containing the search results.
    - **Access**: This endpoint can be accessed via an HTTP GET request to `/search/`.

2. @app.get("/extractKeywords/")
    - **Description**: This endpoint extracts keywords from the provided search query using a language model.
    - **Parameters**: 
      - `search_query` (str): The query string from which to extract keywords.
    - **Returns**: A JSON object containing the extracted keywords.
    - **Access**: This endpoint can be accessed via an HTTP GET request to `/extractKeywords/`.

3. @app.get("/searchAndScrape/")
    - **Description**: This endpoint performs a search operation and scrapes the results.
    - **Parameters**:(str): The query string from which to extract keywords.
    - **Returns**: This will return, persona results, for the features that have been harcoded.
    - **Access**: This endpoint can be accessed via an HTTP GET request to `/searchAndScrape/`.

Other API routes for LLM based persona generation have been muted as of now, as the link in between is broken, though the related code can be found at utils.personaUtils.py

"""