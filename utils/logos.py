import time
from rich.console import Console

console = Console()

KAEL_LOGO = r"""
     _  __     _     _ 
    | |/ /__ _| |__ (_)
    | ' // _` | '_ \| |
    | . \ (_| | | | | |
    |_|\_\__,_|_| |_|_|
    [ KAEL :: Dev Mode ]
"""

BUILDER_LOGO = r"""
     ____                  _            _ _           
    | __ )  ___  __ _  ___| | ___   ___| (_)_ __  ___ 
    |  _ \ / _ \/ _` |/ __| |/ _ \ / __| | | '_ \/ __|
    | |_) |  __/ (_| | (__| | (_) | (__| | | |_) \__ \
    |____/ \___|\__,_|\___|_|\___/ \___|_|_| .__/|___/
                                            |_|       
    [ SPACE BUILDER :: Prod Mode ]
"""

def show_kael_logo():
    for line in KAEL_LOGO.strip("\n").splitlines():
        console.print(f"[bold magenta]{line}[/bold magenta]")
        time.sleep(0.05)

def show_builder_logo():
    for line in BUILDER_LOGO.strip("\n").splitlines():
        console.print(f"[bold green]{line}[/bold green]")
        time.sleep(0.05)
