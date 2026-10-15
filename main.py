#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    console.print(Panel.fit("🔥 RTX DM - Professional Facebook Auto Comment Tool\nDeveloper: RTX DM Team [UI & Pro Mode]", title="[bold yellow]SECURE & STABLE[/bold yellow]", border_style="green"))

def send_comment(post_url, cookie, comment):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        session = requests.Session()
        
        # লিংকটিকে মোবাইল বেসিক ভার্সনে কনভার্ট করা
        if "www.facebook.com" in post_url:
            target_url = post_url.replace("www.facebook.com", "mbasic.facebook.com")
        elif "m.facebook.com" in post_url:
            target_url = post_url.replace("m.facebook.com", "mbasic.facebook.com")
        else:
            target_url = f"https://mbasic.facebook.com/{post_url}"

        # পেজ ফেচ করে ফর্ম টোকেন সংগ্রহ করা
        response = session.get(target_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return False, f"HTTP Error {response.status_code}: Target unreachable"

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # কমেন্ট ফর্ম খুঁজে বের করা
        form = soup.find('form', method='post')
        if not form:
            return False, "Comment form not found or Post is private"

        action = form.get('action')
        comment_url = f"https://mbasic.facebook.com{action}" if action and action.startswith('/') else (action or target_url)

        # হিডেন ইনপুট ফিল্ডগুলো (fb_dtsg, jazoest ইত্যাদি) সংগ্রহ করা
        data = {}
        for input_tag in form.find_all('input'):
            if input_tag.get('name'):
                data[input_tag.get('name')] = input_tag.get('value', '')

        # কমেন্ট টেক্সট যুক্ত করা
        data['comment_text'] = comment
        
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Referer'] = target_url

        # কমেন্ট সাবমিট রিকোয়েস্ট পাঠানো
        post_response = session.post(comment_url, headers=headers, data=data, timeout=15)
        
        if post_response.status_code == 200:
            res_text = post_response.text.lower()
            if 'checkpoint' in post_response.url or 'login' in post_response.url or 'checkpoint' in res_text:
                return False, "Account Checkpoint / Cookie Expired"
            return True, "Comment Posted Successfully"
        else:
            return False, f"Submission Failed (HTTP {post_response.status_code})"
            
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

    console.print(f"\n[bold cyan][*] Starting RTX DM Professional Auto Comment Engine...[/bold cyan]\n")
    
    count = 1
    try:
        while True:
            for comment in comments_list:
                if not comment:
                    continue
                success, result = send_comment(post_link, cookie, comment)
                if success:
                    console.print(f"[bold green][✔] Comment [{count}] Sent:[/bold green] {comment}")
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
