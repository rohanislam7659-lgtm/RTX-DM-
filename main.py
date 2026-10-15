import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
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
    console.print(Panel.fit("🔥 RTX DM - Advanced Facebook Auto Comment Tool\nDeveloper: RTX DM Team [Power Mode v2]", title="[bold yellow]SECURE & STABLE[/bold yellow]", border_style="green"))

def send_comment_with_cookie(post_url, cookie, comment):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2185 Build/RP1A.201005.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        session = requests.Session()
        
        # Convert desktop/share link to mobile link securely
        if "www.facebook.com" in post_url:
            target_url = post_url.replace("www.facebook.com", "m.facebook.com")
        elif "m.facebook.com" in post_url:
            target_url = post_url
        else:
            target_url = f"https://m.facebook.com/{post_url}"

        # Step 1: Fetch the target post page
        response = session.get(target_url, headers=headers)
        
        if response.status_code != 200:
            return False, f"HTTP Error {response.status_code}: Invalid URL or Post not found."

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the comment form
        form = soup.find('form', method='post')
        if not form:
            return False, "Comment form not found (Post might be private or restricted)"

        action = form.get('action')
        comment_url = f"https://m.facebook.com{action}" if action and action.startswith('/') else (action or target_url)

        # Extract hidden form inputs (fb_dtsg, jazoest, etc.)
        data = {}
        for input_tag in soup.find_all('input'):
            if input_tag.get('name'):
                data[input_tag.get('name')] = input_tag.get('value', '')

        # Add comment text
        data['comment_text'] = comment
        
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Referer'] = target_url

        # Step 2: Post the comment
        post_response = session.post(comment_url, headers=headers, data=data, allow_redirects=True)
        
        if post_response.status_code == 200:
            if 'error' in post_response.text.lower() or 'checkpoint' in post_response.url:
                return False, "Account Checkpoint or Blocked by FB"
            return True, "Comment Posted Successfully"
        else:
            return False, f"Submission Failed (HTTP {post_response.status_code})"
            
    except Exception as e:
        return False, str(e)

def main():
    banner()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Facebook Cookie (c_user=...; xs=...):")
    cookie = console.input("[bold green]Cookie ➔ [/bold green]").strip()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Full Facebook Post Link:")
    post_link = console.input("[bold green]Post Link ➔ [/bold green]").strip()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Comments (comma separated, e.g., Nice,Awesome,Cool):")
    comments_input = console.input("[bold green]Comments ➔ [/bold green]").strip()
    comments_list = [c.strip() for c in comments_input.split(',')]
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Delay time between comments (in seconds, recommended >= 15):")
    try:
        delay = int(console.input("[bold green]Delay (sec) ➔ [/bold green]").strip())
    except ValueError:
        delay = 15
        console.print("[bold red][-] Invalid input! Defaulting to 15 seconds.[/bold red]")

    console.print(f"\n[bold cyan][*] Starting Power Mode Auto Comment...[/bold cyan]\n")
    
    count = 1
    try:
        while True:
            for comment in comments_list:
                success, result = send_comment_with_cookie(post_link, cookie, comment)
                if success:
                    console.print(f"[bold green][✔] Comment [{count}] Sent:[/bold green] {comment}")
                else:
                    console.print(f"[bold red][✖] Failed [{comment}]:[/bold red] {result}")
                
                count += 1
                time.sleep(delay)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Process stopped by user. Exiting...[/bold yellow]")
        sys.exit(0)

if __name__ == '__main__':
    main()
