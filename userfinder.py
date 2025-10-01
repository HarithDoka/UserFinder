#!/usr/bin/env python3
"""
UserFinder - Username Checker
Author: NaldyDjafar
License: MIT
Github: https://github.com/NaldyDjafar/userfinder
"""

import argparse
import concurrent.futures
import json
import sys
import time
from urllib.parse import quote_plus

try:
    import requests
except Exception:
    print("Module 'requests' belum terinstall!\nJalankan: pip install -r requirements.txt")
    sys.exit(1)

# --- Website List ---
SITES = {
    "Instagram": "https://www.instagram.com/{u}/",
    "Facebook": "https://www.facebook.com/{u}",
    "Twitter": "https://twitter.com/{u}",
    "YouTube": "https://www.youtube.com/@{u}",
    "Reddit": "https://www.reddit.com/user/{u}",
    "GitHub": "https://github.com/{u}",
    "Pinterest": "https://www.pinterest.com/{u}/",
    "SoundCloud": "https://soundcloud.com/{u}",
    "Steam": "https://steamcommunity.com/id/{u}",
    "Flickr": "https://www.flickr.com/people/{u}/",
    "VK": "https://vk.com/{u}",
    "Spotify": "https://open.spotify.com/user/{u}",
    "Mixcloud": "https://www.mixcloud.com/{u}/",
    "Behance": "https://www.behance.net/{u}",
    "Keybase": "https://keybase.io/{u}",
    "Instructables": "https://www.instructables.com/member/{u}/",
    "Badoo": "https://www.badoo.com/en/{u}",
    "CashMe": "https://cash.me/{u}",
    "DeviantArt": "https://www.deviantart.com/{u}",
    "Tumblr": "https://{u}.tumblr.com/",
    "WordPress": "https://{u}.wordpress.com/",
    "Medium": "https://medium.com/@{u}",
    "GoodReads": "https://www.goodreads.com/{u}",
    "LinkedIn": "https://www.linkedin.com/in/{u}",
    "Telegram": "https://t.me/{u}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
}

# --- Colors ---
class C:
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    B = "\033[94m"
    END = "\033[0m"
    BOLD = "\033[1m"

# --- Banner ---
def banner():
    art = f"""
{C.B}
 _    _                 _____ _           _           
| |  | |               |  ___(_)         | |          
| |  | |___  ___ _ __  | |_   _ _ __   __| | ___ _ __ 
| |  | / __|/ _ \ '__| |  _| | | '_ \ / _` |/ _ \ '__|
| |__| \__ \  __/ |    | |   | | | | | (_| |  __/ |   
 \____/|___/\___|_|    \_|   |_|_| |_|\__,_|\___|_|   
{C.END}
{C.BOLD}Author: NaldyDjafar | UserFinder v1.0{C.END}
"""
    print(art)

# --- Core Check ---
def check_site(site, url, username):
    target = url.format(u=quote_plus(username))
    try:
        r = requests.get(target, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            return (site, target, True)
        return (site, target, False)
    except:
        return (site, target, False)

def run(username, workers=15):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as exe:
        futures = [exe.submit(check_site, s, u, username) for s, u in SITES.items()]
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())
    return sorted(results, key=lambda x: x[0].lower())

# --- Save Results ---
def save(results, file, fmt):
    if fmt == "json":
        with open(file, "w", encoding="utf-8") as f:
            json.dump(
                [{"site": s, "url": u, "found": f} for s, u, f in results],
                f, indent=2, ensure_ascii=False
            )
    elif fmt == "txt":
        with open(file, "w", encoding="utf-8") as f:
            for s, u, f in results:
                f.write(f"[{'FOUND' if f else 'NOT'}] {s}: {u}\n")
    elif fmt == "csv":
        import csv
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Site", "URL", "Found"])
            for s, u, f in results:
                writer.writerow([s, u, f])

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="UserFinder by NaldyDjafar")
    parser.add_argument("-u", "--username", required=True, help="Username target")
    parser.add_argument("-o", "--output", help="Save ke file (results.json / results.txt / results.csv)")
    parser.add_argument("-f", "--format", choices=["json","txt","csv"], default="txt", help="Format output")
    parser.add_argument("-w", "--workers", type=int, default=15, help="Jumlah thread (default 15)")
    args = parser.parse_args()

    banner()
    print(f"{C.BOLD}Mengecek username: {args.username}{C.END}\n")

    start = time.time()
    results = run(args.username, args.workers)
    elapsed = time.time() - start

    found_count = 0
    for s, u, f in results:
        if f:
            print(f"{C.G}[FOUND]{C.END} {s}: {u}")
            found_count += 1
        else:
            print(f"{C.R}[NOT]{C.END}   {s}: {u}")

    print(f"\nSelesai dalam {elapsed:.2f}s | {found_count}/{len(results)} akun ditemukan")

    if args.output:
        save(results, args.output, args.format)
        print(f"Hasil disimpan ke: {args.output}")

if __name__ == "__main__":
    main()
