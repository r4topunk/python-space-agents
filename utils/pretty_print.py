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


def print_grid_layout(layout: dict):
    """
    Renders a grid preview and legend based on layoutConfig.
    """
    layout_config = layout.get("layout", [])
    grid = [["░"] * 12 for _ in range(10)]
    legend = []

    for idx, f in enumerate(layout_config):
        x, y, w, h = f["x"], f["y"], f["w"], f["h"]
        label = f"F{idx + 1}"
        for dy in range(h):
            for dx in range(w):
                gx = x + dx
                gy = y + dy
                if 0 <= gx < 12 and 0 <= gy < 10:
                    grid[gy][gx] = label if dx == 0 and dy == 0 else "."

        legend.append(f"   {label} = {f['i']} @ ({x},{y}) [{w}x{h}]")

    print("\n🧱 Grid Layout Preview:\n")
    for row in grid:
        print(" ", " ".join(row))
    print("\n📘 Legend:")
    for line in legend:
        print(line)
