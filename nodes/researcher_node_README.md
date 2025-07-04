# Researcher Node

## Overview
The Researcher Node is designed to interact with the Image Search MCP server. It processes user input, sends requests for image searches, and handles the results.

## Features
- **Asynchronous Processing**: Utilizes asyncio for efficient handling of requests.
- **Integration with Image Search MCP**: Calls the image search tool to fetch images based on user queries.

## Setup
1. Ensure you have Python installed.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
The researcher node can be run as part of a larger workflow. It listens for user input and initiates image searches based on the provided prompt.

## Example Logic
The main logic of the researcher node includes:
- Logging the start of the research process.
- Calling the image search tool with parameters such as query, maximum results, minimum quality score, and minimum resolution.
- Handling the results and yielding them back to the user.

## Error Handling
The node includes error handling to manage failures in MCP requests and logs appropriate messages.

## License
This project is licensed under the MIT License.