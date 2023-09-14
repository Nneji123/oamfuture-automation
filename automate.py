import pyfiglet
from rich.console import Console
from rich import print as rprint

from utils import (
    automate_with_proxy,
    automate_without_proxy,
    check_chrome_and_chromedriver,
)


def main():
    console = Console()

    console.print("Choose an automation method:", style="bold blue")
    console.print("[1] Automate with Rotating IP Method")
    console.print("[2] Automate without Rotating IP Method")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        try:
            choice_time = int(input("Enter Refresh time interval (in seconds): "))
            automate_with_proxy(interval_time=choice_time)
        except ValueError:
            console.print("Invalid input for time interval. Please enter a valid integer.", style="bold red")
    elif choice == "2":
        try:
            choice_time = int(input("Enter Refresh time interval (in seconds): "))
            automate_without_proxy(interval_time=choice_time)
        except ValueError:
            console.print("Invalid input for time interval. Please enter a valid integer.", style="bold red")
    else:
        console.print("Invalid choice. Please enter 1 or 2.", style="bold red")


if __name__ == "__main__":
    title_text = pyfiglet.figlet_format("OamFuture", font="slant")
    print(title_text)
    script_info = """
[bold cyan]Automation Script Information[/bold cyan]
[bold green]Purpose:[/bold green] This script automates the process of signing up for an account on OamFuture website.
[bold green]Functionality:[/bold green] It generates random numbers, fills out a signup form with these numbers,
and rotates IP's for anonymity.
[bold yellow]Instructions:[/bold yellow]
1. Make sure you have Chrome browser installed.
2. Download Chromedriver from 'https://chromedriver.chromium.org/downloads' and place it in C:\\chromedriver\\chromedriver.exe.
3. Run the script and follow the prompts.
    """
    rprint(script_info)
    check_chrome_and_chromedriver()
    main()
