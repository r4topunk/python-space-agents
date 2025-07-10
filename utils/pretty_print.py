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


def pretty_print_message(message):
    content = getattr(message, "content", None) or message.get("content", "")
    
    # Detect stage by keywords in message content
    if "Found resources" in content:
        header = "🔍 [Researcher]"
    elif "Planned layout" in content:
        header = "🧠 [Planner]"
    elif "Designed layout" in content:
        header = "🎨 [Designer]"
    elif "Final layout" in content:
        header = "🛠️ [Builder]"
    else:
        header = "💬 [Message]"

    print(f"\n{header}\n{content}\n")

from typing import Union

def print_grid_layout(layout, grid_width=12, grid_height=10):
    grid = [[" . " for _ in range(grid_width)] for _ in range(grid_height)]
    legend = []

    for idx, item in enumerate(layout, 1):
        i = item.get("i", "?")
        x, y, w, h = item.get("x", 0), item.get("y", 0), item.get("w", 1), item.get("h", 1)

        if x + w > grid_width or y + h > grid_height:
            print(f"❌ Invalid position/size for: {i}")
            continue

        label = f"F{idx}"
        for dy in range(h):
            for dx in range(w):
                grid_y = y + dy
                grid_x = x + dx
                grid[grid_y][grid_x] = f"{label:>3}" if dy == 0 and dx == 0 else " ░ "
        legend.append(f"{label} = {i} @ ({x},{y}) [{w}x{h}]")

    print("\n🧱 Grid Layout Preview:\n")
    for row in grid:
        print("".join(row))
    print("\n📘 Legend:")
    for l in legend:
        print("  ", l)
    print()