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

APP_MODE = os.getenv("APP_MODE", "dev").lower()

def animate_logo():
    logo = {
        "dev": """
██╗  ██╗ █████╗ ███████╗██╗     
██║ ██╔╝██╔══██╗██╔════╝██║     
█████╔╝ ███████║███████╗██║     
██╔═██╗ ██╔══██║╚════██║██║     
██║  ██╗██║  ██║███████║███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
        """,
        "prod": """
███████╗██████╗  █████╗  ██████╗███████╗     ██████╗ ██╗   ██╗██╗     ██╗███████╗██████╗ 
██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔═══██╗██║   ██║██║     ██║██╔════╝██╔══██╗
█████╗  ██████╔╝███████║██║     █████╗      ██║   ██║██║   ██║██║     ██║█████╗  ██████╔╝
██╔══╝  ██╔═══╝ ██╔══██║██║     ██╔══╝      ██║▄▄ ██║██║   ██║██║     ██║██╔══╝  ██╔══██╗
███████╗██║     ██║  ██║╚██████╗███████╗    ╚██████╔╝╚██████╔╝███████╗██║███████╗██║  ██║
╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝
        """
    }

    selected_logo = logo.get(APP_MODE, logo["dev"])
    for line in selected_logo.strip("\n").splitlines():
        console.print(f"[magenta]{line}[/magenta]")
        time.sleep(0.05)
    time.sleep(0.3)

# === MENU ACTIONS === #
def start_server():
    console.print("[bold green]\nStarting Kael server...[/bold green]")
    os.system("python3 main.py")  # Adjust if main is in a subfolder

def show_examples():
    examples = [
        "Create a space for nouns.wtf",
        "Build a profile for a music artist",
        "Summarize latest Hacker News feeds",
    ]
    table = Table(title="✨ Example Prompts")
    table.add_column("#", justify="right")
    table.add_column("Prompt", justify="left")
    for i, ex in enumerate(examples, 1):
        table.add_row(str(i), ex)
    console.print(table)

def view_settings():
    config_vars = [
        "OPENAI_MODEL", "TEMPERATURE", "MAX_TOKENS", 
        "GRID_WIDTH", "GRID_HEIGHT", "MIN_COVERAGE_PERCENTAGE"
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
        port = os.getenv("SERVER_PORT", "10000")
        response = requests.get(f"http://localhost:{port}/status", timeout=2)
        if response.status_code == 200:
            console.print("[green]✅ Kael is running![/green]")
        else:
            console.print(f"[yellow]⚠️ Unexpected status: {response.status_code}[/yellow]")
    except Exception:
        console.print("[red]❌ Kael is not responding.[/red]")

def view_logs():
    log_file = "kael.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()[-20:]
        console.print(Panel("".join(lines), title="🪵 Last 20 Log Lines", border_style="dim"))
    else:
        console.print("[yellow]No log file found.[/yellow]")

# === MAIN MENU === #
def main_menu():
    console.clear()
    animate_logo()

    while True:
        console.print(Panel(f"[bold cyan]🧠 KAEL CLI - Mode: [yellow]{APP_MODE.upper()}[/yellow][/bold cyan]", expand=False))
        console.print("[cyan]1.[/] Start Kael server")
        console.print("[cyan]2.[/] Show example prompts")
        console.print("[cyan]3.[/] View settings")
        console.print("[cyan]4.[/] Check status")
        console.print("[cyan]5.[/] View logs")
        console.print("[cyan]Q.[/] Quit\n")

        choice = Prompt.ask("Choose an option").strip().lower()
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
        elif choice == "q":
            console.print("👋 Goodbye!")
            break
        else:
            console.print("[red]❌ Invalid choice[/red]")

        input("\n[Press Enter to return to menu...]")

if __name__ == "__main__":
    main_menu()
