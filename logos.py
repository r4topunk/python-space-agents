import time
from rich.console import Console

console = Console()

KAEL_LOGO = r"""
  _  __           _ 
 | |/ / __ _ _ __| |
 | ' / / _` | '__| |
 | . \| (_| | |  | |
 |_|\_\\__,_|_|  |_|

  KAEL - Dev CLI Mode
"""

BUILDER_LOGO = r"""
  ____                      _     
 | __ )  __ _ _ __ ___  ___| |__  
 |  _ \ / _` | '__/ __|/ __| '_ \ 
 | |_) | (_| | |  \__ \ (__| | | |
 |____/ \__,_|_|  |___/\___|_| |_| 

  SPACE BUILDER - Production Mode
"""

def show_kael_logo():
    for line in KAEL_LOGO.strip("\n").splitlines():
        console.print(f"[bold magenta]{line}[/bold magenta]")
        time.sleep(0.05)
    console.print()

def show_builder_logo():
    for line in BUILDER_LOGO.strip("\n").splitlines():
        console.print(f"[bold blue]{line}[/bold blue]")
        time.sleep(0.05)
    console.print()
