"""
Pretty printing utilities for agent outputs.
"""

from typing import Any, Dict
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
import json


console = Console()


def pretty_print_message(message: Any) -> None:
    """
    Pretty print a message with rich formatting.
    
    Args:
        message: Message object to print
    """
    if hasattr(message, 'content'):
        content = message.content
        role = getattr(message, 'type', 'unknown')
        
        # Determine color based on role
        if role == 'human':
            color = "green"
            title = "👤 Human"
        elif role == 'ai':
            color = "blue" 
            title = "🤖 AI Assistant"
        elif role == 'tool':
            color = "yellow"
            title = "🔧 Tool"
        else:
            color = "white"
            title = f"📝 {role.title()}"
        
        # Handle content formatting
        if isinstance(content, str):
            if content.startswith('{') and content.endswith('}'):
                # Try to format as JSON
                try:
                    parsed = json.loads(content)
                    formatted_content = Syntax(
                        json.dumps(parsed, indent=2), 
                        "json", 
                        theme="monokai",
                        background_color="default"
                    )
                except json.JSONDecodeError:
                    formatted_content = Text(content)
            else:
                formatted_content = Text(content)
        else:
            formatted_content = Text(str(content))
        
        panel = Panel(
            formatted_content,
            title=title,
            border_style=color,
            expand=False
        )
        console.print(panel)
    else:
        # Fallback for other message types
        console.print(f"[dim]Message: {str(message)}[/dim]")


def pretty_print_json(data: Dict[str, Any], title: str = "JSON Output") -> None:
    """
    Pretty print JSON data with syntax highlighting.
    
    Args:
        data: Dictionary to print as JSON
        title: Title for the panel
    """
    json_str = json.dumps(data, indent=2)
    syntax = Syntax(json_str, "json", theme="monokai", background_color="default")
    
    panel = Panel(
        syntax,
        title=f"📊 {title}",
        border_style="cyan",
        expand=False
    )
    console.print(panel)


def pretty_print_step(step_name: str, content: str) -> None:
    """
    Pretty print a workflow step.
    
    Args:
        step_name: Name of the step
        content: Content of the step
    """
    panel = Panel(
        Text(content),
        title=f"⚡ {step_name}",
        border_style="magenta",
        expand=False
    )
    console.print(panel)


def pretty_print_error(error: str) -> None:
    """
    Pretty print an error message.
    
    Args:
        error: Error message to display
    """
    panel = Panel(
        Text(error, style="bold red"),
        title="❌ Error",
        border_style="red",
        expand=False
    )
    console.print(panel)


def pretty_print_success(message: str) -> None:
    """
    Pretty print a success message.
    
    Args:
        message: Success message to display
    """
    panel = Panel(
        Text(message, style="bold green"),
        title="✅ Success",
        border_style="green",
        expand=False
    )
    console.print(panel)
