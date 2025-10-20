import requests
import json
import re

# Load settings.json
settings_file = "settings.json"

with open(settings_file, mode="r") as file:
    settings = json.load(file)

base_url = settings["url"]

res = requests.get(base_url + "_sidebar.md")

if res.status_code == 200:
    print("[+] Fetched KB successfully")
else:
    print("[-] An error occured")
    exit()

regexp = r"[A-Za-z0-9_]+.md"
sidebar = res.text

files = re.findall(regexp, sidebar)
kb_file = settings["kb_filename"]

kb = ""

for i in files:
    url = f"{base_url}/{i}"
    res = requests.get(url)
    if res.status_code == 200:
        print(f"[+] Fetched data from {url} successfully")
    else:
        print(f"[-] Error fetching from {url}")
        continue

    kb_content = res.text
    kb += kb_content
    kb += "\n\n\n\n"
    kb += "_" * 100
    kb += "\n"

with open(kb_file, mode="w", encoding="utf-8") as file:
    file.write(kb)
