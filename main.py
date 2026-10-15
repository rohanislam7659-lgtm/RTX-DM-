#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    print("=" * 60)
    print("         RTX DM - Advanced Facebook Auto Comment Tool")
    print("         Developer: RTX DM Team [Professional Edition]")
    print("=" * 60)

def send_comment(post_url, cookie, comment):
    # প্রফেশনাল ব্রাউজার হেডার্স যা ফেসবুকের সিকিউরিটি বাইপাস করতে সাহায্য করবে
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        session = requests.Session()
        
        # লিংকটিকে ফেসবুকের মোবাইল বেসিক ভার্সনে কনভার্ট করা (সবচেয়ে স্টেবল মেথড)
        if "mbasic.facebook.com" in post_url:
            target_url = post_url
        elif "www.facebook.com" in post_url:
            target_url = post_url.replace("www.facebook.com", "mbasic.facebook.com")
        elif "m.facebook.com" in post_url:
            target_url = post_url.replace("m.facebook.com", "mbasic.facebook.com")
        else:
            target_url = f"https://mbasic.facebook.com/{post_url}"

        # পেজটি ফেচ করে ফর্ম এবং টোকেন বা ইউআরএল যাচাই করা
        response = session.get(target_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return False, f"HTTP Error {response.status_code}: Target unreachable"

        # কমেন্ট সাবমিট করার জন্য পে-লোড ডেটা
        payload = {
            'comment_text': comment
        }
        
        # পোস্ট রিকোয়েস্ট পাঠানো
        post_response = session.post(target_url, headers=headers, data=payload, timeout=15)
        
        if post_response.status_code == 200:
            res_text = post_response.text.lower()
            if 'checkpoint' in post_response.url or 'login' in post_response.url or 'checkpoint' in res_text:
                return False, "Account Checkpoint / Cookie Expired"
            return True, "Comment Posted Successfully"
        else:
            return False, f"Submission Failed (HTTP {post_response.status_code})"
            
    except requests.exceptions.Timeout:
        return False, "Request Timeout! Check your internet connection."
    except Exception as e:
        return False, str(e)

def main():
    banner()
    
    print("\n[+] Enter Facebook Cookie (c_user=...; xs=...):")
    cookie = input("Cookie ➔ ").strip()
    if not cookie:
        print("[-] Error: Cookie cannot be empty!")
        sys.exit(1)
    
    print("\n[+] Enter Full Facebook Post Link:")
    post_link = input("Post Link ➔ ").strip()
    if not post_link:
        print("[-] Error: Post link cannot be empty!")
        sys.exit(1)
    
    print("\n[+] Enter Comments (comma separated, e.g., Nice,Awesome,Cool):")
    comments_input = input("Comments ➔ ").strip()
    if not comments_input:
        print("[-] Error: Comments list cannot be empty!")
        sys.exit(1)
    
    comments_list = [c.strip() for c in comments_input.split(',')]
    
    print("\n[+] Enter Delay time between comments (in seconds, recommended >= 15):")
    try:
        delay = int(input("Delay (sec) ➔ ").strip())
    except ValueError:
        delay = 15
        print("[!] Invalid input! Defaulting to 15 seconds.")

    print(f"\n[*] Starting RTX DM Auto Comment Engine...\n")
    
    count = 1
    try:
        while True:
            for comment in comments_list:
                if not comment:
                    continue
                success, result = send_comment(post_link, cookie, comment)
                if success:
                    print(f"[✔] Comment [{count}] Sent: {comment}")
                else:
                    print(f"[✖] Failed [{comment}]: {result}")
                
                count += 1
                print(f"[*] Waiting {delay} seconds for next comment...")
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[!] Process aborted by user. Exiting safely...")
        sys.exit(0)

if __name__ == '__main__':
    main()
