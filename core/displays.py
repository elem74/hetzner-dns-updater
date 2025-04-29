from datetime import datetime

from rich.table import Table
from rich.console import Console
from rich.text import Text

console = Console()

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def display_section(text):

    minus_count = 12

    output = Text()
    output.append(minus_count * "-" + '| ', style="bold white")
    output.append(text, style="bold white")
    output.append(' |' + minus_count * "-", style="bold white")
    console.print(output)

def display_error(text):
    output = Text()
    output.append("ERROR ", style="bold red")
    output.append(text, style="bold white")
    console.print(output)

def display_info(text):
    output = Text()
    output.append("INFO ", style="bold yellow")
    output.append(text, style="bold white")
    console.print(output)


def display_message(texts, status_code = ''):
    output = Text()

    colors = ["bold bright_cyan", "bold magenta", "bold yellow", "bold dark_goldenrod"]

    output.append(f"{get_time()} ", style=f"bold white")

    for index, item in enumerate(texts):
            output.append(f"{item} ", style=f"{colors[index]}")

    if status_code != '':
        if status_code == 200 or status_code == True:
            output.append("SUCCESS", style="bold green")
        else:
            output.append("FAILED", style="bold red")

    console.print(output)