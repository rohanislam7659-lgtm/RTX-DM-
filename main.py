import os
import sys
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    # RTX DM ASCII Art Design
    ascii_art = """
    ██████╗ ████████╗██╗  ██╗    ██████╗ ███╗   ███╗
    ██╔══██╗╚══██╔══╝╚██╗██╔╝    ██╔══██╗████╗ ████║
    ██████╔╝   ██║    ╚███╔╝     ██║  ██║██╔████╔██║
    ██╔══██╗   ██║    ██╔██╗     ██║  ██║██║╚██╔╝██║
    ██║  ██║   ██║   ██╔╝ ██╗    ██████╔╝██║ ╚═╝ ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═════╝ ╚═╝     ╚═╝
    """
    styled_art = Text(ascii_art, style="bold cyan")
    console.print(styled_art)
    console.print(Panel.fit("🔥 Facebook Auto Comment Tool for Termux\nDeveloper: RTX DM Team", title="[bold yellow]WELCOME[/bold yellow]", border_style="green"))

def send_comment(token, post_id, comment):
    url = f"[https://graph.facebook.com/](https://graph.facebook.com/){post_id}/comments"
    payload = {
        'message': comment,
        'access_token': token
    }
    try:
        response = requests.post(url, data=payload)
        res_data = response.json()
        if 'id' in res_data:
            return True, res_data['id']
        else:
            error_msg = res_data.get('error', {}).get('message', 'Unknown Error')
            return False, error_msg
    except Exception as e:
        return False, str(e)

def main():
    banner()
    
    # User Inputs
    console.print("\n[bold yellow]>[/bold yellow] Enter Facebook Access Token / Cookie:")
    token = console.input("[bold green]Token ➔ [/bold green]").strip()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Target Facebook Post ID:")
    post_id = console.input("[bold green]Post ID ➔ [/bold green]").strip()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Comments (comma separated, e.g., Nice,Awesome,Cool):")
    comments_input = console.input("[bold green]Comments ➔ [/bold green]").strip()
    comments_list = [c.strip() for c in comments_input.split(',')]
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Delay time between comments (in seconds):")
    try:
        delay = int(console.input("[bold green]Delay (sec) ➔ [/bold green]").strip())
    except ValueError:
        delay = 10
        console.print("[bold red][-] Invalid input! Defaulting to 10 seconds.[/bold red]")

    console.print(f"\n[bold cyan][*] Starting Auto Comment on Post ID: {post_id}[/bold cyan]\n")
    
    count = 1
    try:
        while True:
            for comment in comments_list:
                success, result = send_comment(token, post_id, comment)
                if success:
                    console.print(f"[bold green][✔] Comment [{count}] Sent Successfully:[/bold green] {comment}")
                else:
                    console.print(f"[bold red][✖] Failed to send [{comment}]:[/bold red] {result}")
                
                count += 1
                time.sleep(delay)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Process stopped by user. Exiting...[/bold yellow]")
        sys.exit(0)

if __name__ == '__main__':
    main()
