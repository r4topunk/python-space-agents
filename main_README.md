# Main Application

## Overview
The main application serves as the entry point for the Intelligent MCP Image Search system. It sets up a web server to handle WebSocket connections and manage user interactions.

## Features
- **WebSocket Support**: Allows real-time communication with connected clients.
- **Integration with LangChain**: Utilizes LangChain for managing workflows and processing user requests.

## Setup
1. Ensure you have Python installed.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
To start the application, run:
```bash
python main.py
```

## WebSocket Endpoints
- **Connection**: Clients can connect to the server via WebSocket to send messages and receive responses.
- **Status Check**: The server provides a status endpoint to check if it is running.

## Example Workflow
1. A client connects to the WebSocket server.
2. The client sends a user request.
3. The server processes the request and interacts with the Researcher Node to fetch images.
4. The server sends back the results to the client.

## Error Handling
The application includes error handling for various scenarios, including missing dependencies and workflow errors.

## License
This project is licensed under the MIT License.