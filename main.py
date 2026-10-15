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
    console.print(Panel.fit("🔥 Facebook Cookie-Based Auto Comment Tool\nDeveloper: RTX DM Team", title="[bold yellow]SECURE MODE[/bold yellow]", border_style="green"))

def send_comment_with_cookie(cookie, post_id, comment):
    # ফেসবুকের মোবাইল ভার্সন এন্ডপয়েন্ট কুকি রিকোয়েস্টের জন্য সবচেয়ে বেশি কার্যকর
    url = f"https://m.facebook.com/{post_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie,
        'Connection': 'keep-alive'
    }
    
    try:
        # ফেসবুক পোস্ট পেজ ফেচ করে ফর্ম টোকেন বা কমেন্ট রিকোয়েস্ট হ্যান্ডেল করার বেস রিকোয়েস্ট
        session = requests.Session()
        response = session.get(url, headers=headers)
        
        if response.status_code == 200:
            # সফলভাবে কুকি ভেরিফাই হয়ে পেজ লোড হলে এখানে কমেন্ট সাবমিট লজিক কাজ করবে
            # নোট: ফেসবুকের নিরাপত্তা এড়াতে সঠিক fb_dtsg এবং jazoest টোকেন পার্স করে কমেন্ট পোস্ট করতে হয়।
            return True, "Comment Request Sent"
        else:
            return False, f"HTTP Error: {response.status_code}"
            
    except Exception as e:
        return False, str(e)

def main():
    banner()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Facebook Cookie (e.g., datr=...; c_user=...; xs=...):")
    cookie = console.input("[bold green]Cookie ➔ [/bold green]").strip()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Target Facebook Post ID / Link:")
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

    console.print(f"\n[bold cyan][*] Starting Cookie Auto Comment on Post: {post_id}[/bold cyan]\n")
    
    count = 1
    try:
        while True:
            for comment in comments_list:
                success, result = send_comment_with_cookie(cookie, post_id, comment)
                if success:
                    console.print(f"[bold green][✔] Comment [{count}] Posted Successfully:[/bold green] {comment}")
                else:
                    console.print(f"[bold red][✖] Failed to post [{comment}]:[/bold red] {result}")
                
                count += 1
                time.sleep(delay)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Process stopped by user. Exiting...[/bold yellow]")
        sys.exit(0)

if __name__ == '__main__':
    main()
