#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    console.print(Panel.fit("🔥 RTX DM - Professional Facebook Auto Comment Tool\nDeveloper: RTX DM Team [API Direct Mode]", title="[bold yellow]ULTIMATE EDITION[/bold yellow]", border_style="green"))

def extract_post_id(url):
    import re
    # লিংকের ভেতর থেকে মূল পোস্ট আইডি বা সংখ্যা আলাদা করে বের করা
    match = re.search(r'(?:story_fbid=|posts/|fbid=|\/)([0-9]{10,20})', url)
    if match:
        return match.group(1)
    # যদি সরাসরি সংখ্যা দেওয়া হয়
    digits = re.findall(r'\d+', url)
    if digits:
        return max(digits, key=len)
    return None

def send_comment(post_url, cookie, comment):
    post_id = extract_post_id(post_url)
    if not post_id:
        return False, "Invalid Post Link or ID could not be extracted."

    # ফেসবুকের মোবাইল কমেন্ট এন্ডপয়েন্ট (সরাসরি আইডি দিয়ে কমেন্ট পোস্ট করার আধুনিক পদ্ধতি)
    target_url = f"https://m.facebook.com/a/comment.php?ft_ent_identifier={post_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie,
        'Origin': 'https://m.facebook.com',
        'Referer': f"https://m.facebook.com/story.php?story_fbid={post_id}&id={post_id}",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    payload = {
        'comment_text': comment
    }
    
    try:
        session = requests.Session()
        response = session.post(target_url, headers=headers, data=payload, timeout=15)
        
        if response.status_code == 200:
            res_text = response.text.lower()
            if 'checkpoint' in response.url or 'login' in response.url or 'checkpoint' in res_text:
                return False, "Account Checkpoint / Cookie Expired"
            
            # সফলভাবে কমেন্ট সাবমিট হলে
            return True, f"Comment Posted Successfully (ID: {post_id})"
        else:
            return False, f"HTTP Error {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Request Timeout!"
    except Exception as e:
        return False, str(e)

def main():
    banner()
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Facebook Cookie (c_user=...; xs=...):")
    cookie = console.input("[bold green]Cookie ➔ [/bold green]").strip()
    if not cookie:
        console.print("[bold red][-] Cookie cannot be empty![/bold red]")
        sys.exit(1)
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Full Facebook Post Link:")
    post_link = console.input("[bold green]Post Link ➔ [/bold green]").strip()
    if not post_link:
        console.print("[bold red][-] Post link cannot be empty![/bold red]")
        sys.exit(1)
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Comments (comma separated, e.g., Nice,Awesome,Cool):")
    comments_input = console.input("[bold green]Comments ➔ [/bold green]").strip()
    if not comments_input:
        console.print("[bold red][-] Comments cannot be empty![/bold red]")
        sys.exit(1)
    
    comments_list = [c.strip() for c in comments_input.split(',')]
    
    console.print("\n[bold yellow]>[/bold yellow] Enter Delay time between comments (in seconds, recommended >= 15):")
    try:
        delay = int(console.input("[bold green]Delay (sec) ➔ [/bold green]").strip())
    except ValueError:
        delay = 15
        console.print("[bold red][!] Invalid input! Defaulting to 15 seconds.[/bold red]")

    console.print(f"\n[bold cyan][*] Starting Direct API Auto Comment Engine...[/bold cyan]\n")
    
    count = 1
    try:
        while True:
            for comment in comments_list:
                if not comment:
                    continue
                success, result = send_comment(post_link, cookie, comment)
                if success:
                    console.print(f"[bold green][✔] Comment [{count}] Sent:[/bold green] {comment} [{result}]")
                else:
                    console.print(f"[bold red][✖] Failed [{comment}]:[/bold red] {result}")
                
                count += 1
                console.print(f"[bold yellow][*] Waiting {delay} seconds for next comment...[/bold yellow]")
                time.sleep(delay)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Process aborted by user. Exiting safely...[/bold yellow]")
        sys.exit(0)

if __name__ == '__main__':
    main()
