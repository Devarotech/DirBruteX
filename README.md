# DirBruteX 🔍
### Web Directory Brute-force Tool
**Author:** Arojinle | Devarotech
**Language:** Python 3
**Category:** Web Security / Ethical Hacking Tool

## Overview
DirBruteX is a multi-threaded web directory brute-forcer
built to discover hidden files and directories on web servers
by testing paths from a custom wordlist and reporting
findings with HTTP status codes.

## Features
- Multi-threaded scanning (fast)
- Detects 200 Found, 301/302 Redirects, 403 Forbidden
- Custom wordlist support
- Auto-saves timestamped scan report

## Skills Demonstrated
- Python requests library
- Multi-threading with thread locking
- Web reconnaissance concepts
- HTTP status code analysis
- Report generation

## Ethical Disclaimer
For educational purposes and authorised testing only.
Never scan systems you don't own or have permission to test.

## How to Run
  python3 dirbutex.py

## Sample Output
  [200 FOUND]     http://127.0.0.1/index.html
  [403 FORBIDDEN] http://127.0.0.1/.htaccess
