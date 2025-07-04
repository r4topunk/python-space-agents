# Image Search MCP

## Overview
The Image Search MCP is a server that allows users to search for images using the Unsplash API. It evaluates images based on quality metrics and returns results that meet specified criteria.

## Features
- **Image Scoring**: Images are scored based on resolution, aspect ratio, sharpness, and compression.
- **API Integration**: Fetches images from Unsplash based on user queries.

## Setup
1. Ensure you have Python installed.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables in a `.env` file:
   ```
   UNSPLASH_ACCESS_KEY=your_access_key_here
   ```

## Running the Server
To start the server, run:
```bash
python imageSearchMCP.py --name MyImageMCP --debug
```

## API Endpoints
- **Image Search**: 
  - Endpoint: `/mcp/image_search`
  - Method: POST
  - Parameters:
    - `query`: The search term.
    - `max_results`: Maximum number of results to return.
    - `min_quality_score`: Minimum quality score for images.
    - `min_resolution`: Minimum resolution as a list of [width, height].

## Example Usage
To search for images, send a request with the desired parameters.

## Logging
The server supports debug logging to help with troubleshooting.

## License
This project is licensed under the MIT License.