# Intelligent MCP Image Search Server

## Overview
The Intelligent MCP Image Search Server is designed to facilitate image searches using the Unsplash API. It allows users to query images based on specific criteria and returns results that meet quality standards.

## Components
1. **imageSearchMCP.py**: The main server file that handles image search requests.
2. **researcher_node.py**: A node that interacts with the image search server to fetch images based on user input.
3. **main.py**: The entry point for the application, setting up the web server and handling WebSocket connections.

## Setup
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables in a `.env` file:
   ```
   UNSPLASH_ACCESS_KEY=your_access_key_here
   ```

## Running the Server
To run the image search server, execute the following command:
```bash
python mcp/imageSearchMCP.py --name MyImageMCP --debug
```

## Usage
- The server exposes an API endpoint for image searches.
- You can interact with the server through WebSocket connections to send queries and receive image results.

## Image Scoring
Images are scored based on:
- Resolution
- Aspect Ratio
- Sharpness (placeholder)
- Compression (placeholder)

## Example Query
To search for images, send a request with the desired query, maximum results, minimum quality score, and minimum resolution.

## License
This project is licensed under the MIT License.
