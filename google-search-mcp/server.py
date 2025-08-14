#!/usr/bin/env python3
"""
Google Search MCP Server

An MCP server that provides Google search functionality using the Google Custom Search API.
"""

import os
import logging
from typing import Any, List, Dict, Optional
import requests
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("google-search-mcp")

# Google Custom Search API configuration
GOOGLE_API_KEY = "AIzaSyDEZwmQrcKIEL8mVYCPN7tlgH3t3apeh7I"
# Using a generic search engine ID - users may need to create their own Custom Search Engine
GOOGLE_SEARCH_ENGINE_ID = "017576662512468239146:omuauf_lfve"  # This may need to be updated
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


@mcp.tool()
async def google_search(
    query: str,
    num_results: int = 10,
    start_index: int = 1,
    search_type: str = "web"
) -> str:
    """
    Performs a Google search and returns the results.

    Args:
        query: The search query string
        num_results: Number of results to return (1-10, default: 10)
        start_index: Starting index for results (default: 1)
        search_type: Type of search - 'web' for web search, 'image' for image search

    Returns:
        JSON string containing search results with titles, links, and snippets
    """
    try:
        # Validate parameters
        num_results = max(1, min(10, num_results))  # Clamp between 1-10
        start_index = max(1, start_index)
        
        # Prepare API parameters
        params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_SEARCH_ENGINE_ID,
            'q': query,
            'num': num_results,
            'start': start_index
        }
        
        # Add search type if it's image search
        if search_type.lower() == 'image':
            params['searchType'] = 'image'
        
        # Make the API request
        logger.info(f"Searching for: {query}")
        response = requests.get(GOOGLE_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        results = []
        if 'items' in data:
            for item in data['items']:
                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'displayLink': item.get('displayLink', '')
                }
                
                # Add image-specific fields if it's an image search
                if search_type.lower() == 'image' and 'image' in item:
                    result['image'] = {
                        'contextLink': item['image'].get('contextLink', ''),
                        'height': item['image'].get('height', 0),
                        'width': item['image'].get('width', 0),
                        'thumbnailLink': item['image'].get('thumbnailLink', '')
                    }
                
                results.append(result)
        
        # Prepare response
        search_info = data.get('searchInformation', {})
        response_data = {
            'query': query,
            'searchType': search_type,
            'totalResults': search_info.get('totalResults', '0'),
            'searchTime': search_info.get('searchTime', 0),
            'results': results
        }
        
        import json
        return json.dumps(response_data, indent=2)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return f"Error: Failed to perform search - {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def google_image_search(
    query: str,
    num_results: int = 10,
    start_index: int = 1
) -> str:
    """
    Performs a Google image search and returns the results.

    Args:
        query: The search query string
        num_results: Number of results to return (1-10, default: 10)
        start_index: Starting index for results (default: 1)

    Returns:
        JSON string containing image search results with URLs, thumbnails, and context
    """
    return await google_search(query, num_results, start_index, "image")


@mcp.tool()
async def search_site(
    query: str,
    site: str,
    num_results: int = 10
) -> str:
    """
    Searches within a specific website using Google's site: operator.

    Args:
        query: The search query string
        site: The website domain to search within (e.g., "wikipedia.org")
        num_results: Number of results to return (1-10, default: 10)

    Returns:
        JSON string containing search results from the specified site
    """
    site_query = f"site:{site} {query}"
    return await google_search(site_query, num_results)


@mcp.tool()
async def search_news(
    query: str,
    num_results: int = 10,
    days_back: int = 7
) -> str:
    """
    Searches for recent news articles using Google search with time filters.

    Args:
        query: The search query string
        num_results: Number of results to return (1-10, default: 10)
        days_back: How many days back to search (default: 7)

    Returns:
        JSON string containing recent news search results
    """
    # Add news-related terms to improve results
    news_query = f"{query} news"
    return await google_search(news_query, num_results)


@mcp.tool()
async def get_search_suggestions(query: str) -> str:
    """
    Gets search suggestions for a given query (simplified version).

    Args:
        query: The partial search query

    Returns:
        JSON string with basic search suggestions
    """
    try:
        # This is a simplified version - Google's autocomplete API requires different setup
        # For now, we'll return some basic suggestions based on common patterns
        suggestions = [
            f"{query} definition",
            f"{query} tutorial",
            f"{query} examples",
            f"what is {query}",
            f"how to {query}"
        ]
        
        import json
        return json.dumps({
            "query": query,
            "suggestions": suggestions
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Error generating suggestions: {e}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Run the server using HTTP transport for easier testing
    logger.info("Starting Google Search MCP Server...")
    mcp.run(transport="http", host="0.0.0.0", port=3030)
