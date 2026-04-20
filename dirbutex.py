#!/usr/bin/env python3
# ============================================================
#   DirBruteX - Web Directory Brute-forcer
#   Author  : Arojinle (Najeem Omokunmi Atanda)
#   Brand   : Devarotech
#   Version : 1.0
#   Purpose : Ethical web reconnaissance tool
#   Usage   : python3 dirbutex.py
# ============================================================

import requests
import threading
import datetime
import sys
import os

# ── Colour codes ───────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

found_dirs   = []
lock         = threading.Lock()


def print_banner():
    print(f"""{CYAN}{BOLD}
╔══════════════════════════════════════════════════╗
║        DirBruteX - by Arojinle / Devarotech      ║
║          Web Directory Brute-force Tool          ║
║               For Ethical Use Only               ║
╚══════════════════════════════════════════════════╝
{RESET}""")


def check_dir(base_url, word):
    """Check if a directory or file exists on the target."""
    url = f"{base_url}/{word}"
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)

        if response.status_code == 200:
            with lock:
                found_dirs.append((url, response.status_code, "FOUND"))
                print(f"  {GREEN}[200 FOUND]{RESET}     {BOLD}{url}{RESET}")

        elif response.status_code == 301 or response.status_code == 302:
            with lock:
                found_dirs.append((url, response.status_code, "REDIRECT"))
                print(f"  {YELLOW}[{response.status_code} REDIRECT]{RESET}  {url}")

        elif response.status_code == 403:
            with lock:
                found_dirs.append((url, response.status_code, "FORBIDDEN"))
                print(f"  {YELLOW}[403 FORBIDDEN]{RESET} {url} (exists but restricted)")

    except requests.ConnectionError:
        print(f"  {RED}[-] Connection error on {url}{RESET}")
    except requests.Timeout:
        pass


def save_report(target, start_time, end_time):
    """Save results to a report file."""
    filename = f"dirbutex_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("     DirBruteX Report — by Arojinle / Devarotech\n")
        f.write("=" * 60 + "\n")
        f.write(f"Target     : {target}\n")
        f.write(f"Scan Start : {start_time}\n")
        f.write(f"Scan End   : {end_time}\n")
        f.write(f"Found      : {len(found_dirs)} directories/files\n")
        f.write("=" * 60 + "\n\n")
        if found_dirs:
            f.write("DISCOVERED PATHS:\n\n")
            for url, status, label in found_dirs:
                f.write(f"[{status}] {label:<10} → {url}\n")
        else:
            f.write("No directories found.\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("DISCLAIMER: For authorised testing only.\n")
        f.write("=" * 60 + "\n")
    print(f"\n{GREEN}[+] Report saved → {filename}{RESET}")


def main():
    print_banner()

    target = input(f"{CYAN}[?] Enter target URL (e.g. http://127.0.0.1): {RESET}").strip()

    # Add http:// if missing
    if not target.startswith("http"):
        target = "http://" + target

    wordlist = input(f"{CYAN}[?] Wordlist path (press Enter for wordlist.txt): {RESET}").strip()
    if not wordlist:
        wordlist = "wordlist.txt"

    if not os.path.exists(wordlist):
        print(f"{RED}[-] Wordlist not found: {wordlist}{RESET}")
        sys.exit(1)

    with open(wordlist, "r") as f:
        words = [line.strip() for line in f if line.strip()]

    print(f"\n{YELLOW}[*] Target   : {target}{RESET}")
    print(f"{YELLOW}[*] Words    : {len(words)}{RESET}")
    print(f"{YELLOW}[*] Started  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    threads    = []

    for word in words:
        t = threading.Thread(target=check_dir, args=(target, word))
        threads.append(t)
        t.start()

        if len(threads) >= 10:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{CYAN}{'─'*52}{RESET}")
    print(f"{GREEN}[+] Scan Complete. {len(found_dirs)} path(s) discovered.{RESET}")

    save_report(target, start_time, end_time)


if __name__ == "__main__":
    main()
