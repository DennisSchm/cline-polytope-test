# Google Search MCP Server

An MCP (Model Context Protocol) server that provides Google search functionality using the Google Custom Search API. This server exposes various search tools that can be used by MCP clients to perform web searches, image searches, site-specific searches, and more.

## Features

- 🔍 **Web Search** - Perform general Google web searches
- 🖼️ **Image Search** - Search for images with metadata
- 🌐 **Site-Specific Search** - Search within specific websites
- 📰 **News Search** - Search for recent news articles
- 💡 **Search Suggestions** - Get search query suggestions
- 🚀 **Fast & Reliable** - Built with FastMCP for optimal performance

## Available Tools

### 1. `google_search`
Performs a general Google web search.

**Parameters:**
- `query` (string): The search query
- `num_results` (int, optional): Number of results (1-10, default: 10)
- `start_index` (int, optional): Starting index for pagination (default: 1)
- `search_type` (string, optional): "web" or "image" (default: "web")

### 2. `google_image_search`
Performs a Google image search with image-specific metadata.

**Parameters:**
- `query` (string): The search query
- `num_results` (int, optional): Number of results (1-10, default: 10)
- `start_index` (int, optional): Starting index for pagination (default: 1)

### 3. `search_site`
Searches within a specific website using Google's site: operator.

**Parameters:**
- `query` (string): The search query
- `site` (string): Website domain to search (e.g., "wikipedia.org")
- `num_results` (int, optional): Number of results (1-10, default: 10)

### 4. `search_news`
Searches for recent news articles.

**Parameters:**
- `query` (string): The search query
- `num_results` (int, optional): Number of results (1-10, default: 10)
- `days_back` (int, optional): Days back to search (default: 7)

### 5. `get_search_suggestions`
Gets search suggestions for a given query.

**Parameters:**
- `query` (string): The partial search query

## Setup and Running

### Using Polytope (Recommended)

1. **Start the MCP Server:**
   ```bash
   pt run google-search-mcp
   ```

2. **Start MCP Inspector for testing:**
   ```bash
   pt run mcp-inspector
   ```
   Then open http://localhost:6274 in your browser to test the tools interactively.

### Manual Setup

1. **Initialize the environment:**
   ```bash
   cd google-search-mcp
   ./bin/init
   ```

2. **Run the server:**
   ```bash
   ./bin/run
   ```

## API Configuration

The server uses the Google Custom Search API with the following configuration:
- **API Key**: Pre-configured (AIzaSyDEZwmQrcKIEL8mVYCPN7tlgH3t3apeh7I)
- **Search Engine ID**: Default programmable search engine
- **Rate Limits**: Follows Google's API rate limits

## Response Format

All search tools return JSON responses with the following structure:

```json
{
  "query": "search query",
  "searchType": "web",
  "totalResults": "1000000",
  "searchTime": 0.123456,
  "results": [
    {
      "title": "Page Title",
      "link": "https://example.com",
      "snippet": "Page description...",
      "displayLink": "example.com"
    }
  ]
}
```

For image searches, additional image metadata is included:

```json
{
  "image": {
    "contextLink": "https://example.com/page",
    "height": 480,
    "width": 640,
    "thumbnailLink": "https://example.com/thumb.jpg"
  }
}
```

## Usage Examples

### Basic Web Search
```python
# Search for Python tutorials
result = await google_search("Python programming tutorial")
```

### Image Search
```python
# Search for cat images
result = await google_image_search("cute cats", num_results=5)
```

### Site-Specific Search
```python
# Search Wikipedia for information about AI
result = await search_site("artificial intelligence", "wikipedia.org")
```

### News Search
```python
# Search for recent technology news
result = await search_news("technology innovation", days_back=3)
```

## Error Handling

The server includes comprehensive error handling for:
- API request failures
- Invalid parameters
- Network timeouts
- Rate limiting
- Malformed responses

All errors are returned as JSON strings with descriptive error messages.

## Dependencies

- **FastMCP** - MCP server framework
- **requests** - HTTP client for API calls
- **Python 3.10+** - Modern Python with type hints

## Testing

Use the MCP Inspector to test all tools interactively:

1. Start the server: `pt run google-search-mcp`
2. Start inspector: `pt run mcp-inspector`
3. Open http://localhost:6274
4. Connect to the server and test each tool

## Limitations

- Maximum 10 results per search (Google API limitation)
- Rate limits apply based on Google's API quotas
- Search suggestions are simplified (not using Google's autocomplete API)
- Requires active internet connection

## License

This MCP server is provided as-is for educational and development purposes.
