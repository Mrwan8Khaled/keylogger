import os
import sys
import time
import requests
import subprocess

# ---------------- CONFIG ----------------
CURRENT_VERSION = "1.0.0"  # your current version
GITHUB_USERNAME = "USERNAME"
REPO_NAME = "REPO"
TOKEN = ""  # read token from env variable
VERSION_FILE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/version.txt"
EXE_BASE_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/releases/download"

LOCAL_EXE_NAME = "mytool.exe"
NEW_EXE_NAME = "mytool_new.exe"
# ----------------------------------------

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def get_latest_version():
    try:
        r = requests.get(VERSION_FILE_URL, headers=HEADERS)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        print("[!] Failed to fetch latest version:", e)
        return None

def download_new_exe(version):
    exe_url = f"{EXE_BASE_URL}/v{version}/{LOCAL_EXE_NAME}"
    try:
        r = requests.get(exe_url, headers=HEADERS)
        r.raise_for_status()
        with open(NEW_EXE_NAME, "wb") as f:
            f.write(r.content)
        print(f"[+] Downloaded new exe: {NEW_EXE_NAME}")
        return True
    except Exception as e:
        print("[!] Failed to download new exe:", e)
        return False

def restart_new_exe():
    try:
        subprocess.Popen([NEW_EXE_NAME])
        time.sleep(2)  # let new exe start
        # Optionally delete old exe after restart
        try:
            os.remove(LOCAL_EXE_NAME)
        except Exception:
            pass
        # rename new exe to original name
        os.rename(NEW_EXE_NAME, LOCAL_EXE_NAME)
        sys.exit(0)
    except Exception as e:
        print("[!] Failed to restart new exe:", e)

def main():
    print(f"Current version: {CURRENT_VERSION}")
    latest_version = get_latest_version()
    if not latest_version:
        return

    if latest_version != CURRENT_VERSION:
        print(f"[+] Update available! {latest_version}")
        if download_new_exe(latest_version):
            restart_new_exe()
    else:
        print("[-] Already up to date!")

if __name__ == "__main__":
    main()
