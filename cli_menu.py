import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from dotenv import load_dotenv

console = Console()
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "KAEL")
APP_MODE = os.getenv("APP_MODE", "dev").lower()
SERVER_COMMAND = os.getenv("SERVER_COMMAND", "python3 main.py")

def show_ascii_animation():
    ascii_art = f"""
[bold magenta]
  ██████  ▒█████   ▄████▄   ██████ ▓█████     ▄████▄   ██▓    ▓█████▄ 
▒██    ▒ ▒██▒  ██▒▒██▀ ▀█ ▒██    ▒ ▓█   ▀    ▒██▀ ▀█  ▓██▒    ▒██▀ ██▌
░ ▓██▄   ▒██░  ██▒▒▓█    ▄░ ▓██▄   ▒███      ▒▓█    ▄ ▒██░    ░██   █▌
  ▒   ██▒▒██   ██░▒▓▓▄ ▄██▒ ▒   ██▒▒▓█  ▄    ▒▓▓▄ ▄██▒▒██░    ░▓█▄   ▌
▒██████▒▒░ ████▓▒░▒ ▓███▀ ░▒██████▒░░▒████▒  ▒ ▓███▀ ░░██████▒░▒████▓ 
▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░░░ ▒░ ░  ░ ░▒ ▒  ░░ ▒░▓  ░ ▒▒▓  ▒ 
░ ░▒  ░ ░  ░ ▒ ▒░   ░  ▒  ░ ░▒  ░ ░ ░ ░  ░    ░  ▒   ░ ░ ▒  ░ ░ ▒  ▒ 
░  ░  ░  ░ ░ ░ ▒  ░        ░  ░  ░     ░     ░        ░ ░    ░ ░  ░ 
      ░      ░ ░  ░ ░            ░     ░  ░  ░ ░        ░  ░   ░    
                   ░                          ░               ░      
[/bold magenta]
"""
    console.print(ascii_art)
    time.sleep(1.5)

def start_server():
    console.print("[bold green]\n🚀 Starting Kael server...[/bold green]")
    os.system(SERVER_COMMAND)

def show_examples():
    examples = [
        "Create a space for nouns.wtf",
        "Build a profile for a music artist",
        "Summarize latest Hacker News feeds",
    ]
    table = Table(title="🧪 Example Prompts")
    table.add_column("#", justify="right")
    table.add_column("Prompt", justify="left")
    for i, ex in enumerate(examples, 1):
        table.add_row(str(i), ex)
    console.print(table)

def view_settings():
    config_vars = [
        "OPENAI_MODEL", "TEMPERATURE", "MAX_TOKENS", 
        "GRID_WIDTH", "GRID_HEIGHT", "MIN_COVERAGE_PERCENTAGE",
        "SERVER_COMMAND", "APP_MODE"
    ]
    table = Table(title="⚙️ Settings")
    table.add_column("Variable")
    table.add_column("Value")
    for var in config_vars:
        table.add_row(var, os.getenv(var, "[red]Not Set[/red]"))
    console.print(table)

def check_status():
    import requests
    try:
        response = requests.get("http://localhost:10000/status", timeout=2)
        if response.status_code == 200:
            console.print("[green]✅ Kael is running![/green]")
        else:
            console.print(f"[yellow]⚠️ Unexpected status: {response.status_code}[/yellow]")
    except Exception:
        console.print("[red]❌ Kael is not responding at localhost:10000[/red]")

def view_logs():
    log_file = "kael.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()[-20:]
        console.print(Panel("".join(lines), title="📜 Last 20 Log Lines", border_style="dim"))
    else:
        console.print("[yellow]No log file found.[/yellow]")

def main_menu():
    if APP_MODE == "prod":
        start_server()
        return

    console.clear()
    show_ascii_animation()

    while True:
        console.print(Panel.fit(
            """\
🧠 KAEL - Space Agent Hub

[1] 🚀 Start Agent
[2] 🧪 Try Example Prompt
[3] ⚙️  Settings
[4] 📊 Status
[5] 📜 Show Last Logs
[6] ❌ Quit""",
            title=" Main Menu ",
            border_style="cyan",
            padding=(1, 2)
        ))

        choice = Prompt.ask("Select an option [1/2/3/4/5/6]").strip().lower()
        if choice == "1":
            start_server()
        elif choice == "2":
            show_examples()
        elif choice == "3":
            view_settings()
        elif choice == "4":
            check_status()
        elif choice == "5":
            view_logs()
        elif choice == "6" or choice == "q":
            console.print("👋 Goodbye!")
            break
        else:
            console.print("[red]❌ Invalid choice[/red]")

        input("\n[Press Enter to return to menu...]")
        console.clear()

if __name__ == "__main__":
    main_menu()
