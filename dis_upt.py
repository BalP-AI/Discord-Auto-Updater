# Discord Auto Update Script
# Created by Chrysovalantis Pateiniotis 12/10/2025
# Ver 1.0
import json
import requests
import re
import urllib.request
import os
import subprocess
import sys

def download_file(link, filename):
    # Set headers to avoid 403 Forbidden
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
    urllib.request.install_opener(opener)

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = downloaded * 100 / total_size if total_size > 0 else 0
        print(f"\rDownloading... {percent:.2f}%", end="")
    urllib.request.urlretrieve(link, filename, reporthook)
    print("\n✅ Download complete!")
    return True

def install_file(filename):
    try:
        subprocess.run(["sudo", "dpkg", "-i", filename], check=True)
        print("✅ Installation successful!")
    except subprocess.CalledProcessError as e:
        print("❌ Installation failed.")
        print("Error output:\n", e.stderr)
    return None

# --- Get current version ---
try:
    with open("/usr/share/discord/resources/build_info.json") as f:
        data = json.load(f)
        curr_version = data["version"]
        print("Current Discord version:", curr_version)
except FileNotFoundError:
    print("⚠️ Discord not installed or build_info.json missing.")
    curr_version = "0.0.0"

# --- Get latest version ---
link = "https://discord.com/api/download?platform=linux&format=deb"
resp = requests.head(link, allow_redirects=True)

# Extract version number from redirected URL
match = re.search(r"discord-([\d\.]+)\.deb", resp.url)
if not match:
    print("❌ Could not determine latest Discord version.")
    sys.exit(1)

latest_version = match.group(1)
print("Latest Discord version:", latest_version)

# --- Compare versions ---
def version_tuple(v):
    #seperate the version into list of strings then applies the int() method with the use of map to each element of the list and then makes it into a tuple
    return tuple(map(int, v.split(".")))

if version_tuple(latest_version) > version_tuple(curr_version):
    print("🔄 New version available! Downloading...")
    filename = os.path.expanduser("~/Downloads/discord_latest.deb")
    done = download_file(link, filename)
    if done:
        install_file(filename)
else:
    print("✅ Discord is up to date.")
