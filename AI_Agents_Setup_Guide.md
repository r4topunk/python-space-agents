# AI Agents Setup Guide

## Overview
This guide provides a comprehensive setup for developers to replicate the Intelligent MCP Image Search system across various tools, agents, and workers. It aims to facilitate understanding and usage for developers, particularly those working with Large Language Models (LLMs).

## Components
1. **Image Search MCP**: A server that handles image search requests.
2. **Researcher Node**: A component that interacts with the Image Search MCP to fetch images based on user input.
3. **Main Application**: The entry point that sets up the web server and manages WebSocket connections.

## Setup Instructions

### Prerequisites
- Ensure Python is installed on your system.
- Install necessary dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Environment Configuration
1. Create a `.env` file in the project root directory.
2. Add the following environment variable:
   ```
   UNSPLASH_ACCESS_KEY=your_access_key_here
   ```

### Running the Components
- **Image Search MCP**:
  ```bash
  python mcp/imageSearchMCP.py --name MyImageMCP --debug
  ```
- **Main Application**:
  ```bash
  python main.py
  ```

### Interacting with the System
- Connect to the WebSocket server to send user requests.
- Use the image search functionality by sending queries to the Image Search MCP.

## Updating the System
1. **Code Changes**: Modify the respective Python files as needed.
2. **Documentation**: Update the README files to reflect any changes in functionality or usage.
3. **Testing**: Ensure to run tests after making changes to verify functionality.

## Best Practices
- Maintain clear and concise documentation for each component.
- Use version control (e.g., Git) to track changes and collaborate with other developers.
- Regularly update dependencies to keep the system secure and efficient.

## Conclusion
This guide serves as a foundational resource for developers looking to replicate and extend the Intelligent MCP Image Search system. By following these instructions, developers can effectively set up, use, and update the system in their own environments.

## License
This project is licensed under the MIT License.