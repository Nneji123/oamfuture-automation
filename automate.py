from rich.console import Console

from utils import  automate_with_proxy, automate_without_proxy, check_chrome_and_chromedriver


def main():
    console = Console()

    console.print("Choose an automation method:", style="bold blue")
    console.print("[1] Automate with proxy")
    console.print("[2] Automate without proxy")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        automate_with_proxy()
    elif choice == "2":
        automate_without_proxy()
    else:
        console.print("Invalid choice. Please enter 1 or 2.", style="bold red")


if __name__ == "__main__":
    check_chrome_and_chromedriver()
    main()
