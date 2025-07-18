import subprocess
import re
import os
import requests
import zipfile

def get_installed_chrome_version():
    try:
        output = subprocess.check_output(
            r'reg query "HKCU\\Software\\Google\\Chrome\\BLBeacon" /v version',
            shell=True
        ).decode()
        match = re.search(r"version\s+REG_SZ\s+([^\s]+)", output)
        return match.group(1) if match else None
    except Exception as e:
        print(f"⚠ Could not detect system Chrome version: {e}")
        return None

def download_chromedriver(driver_ver, out_dir):
    zip_url = f"https://chromedriver.storage.googleapis.com/{driver_ver}/chromedriver_win32.zip"
    zip_path = os.path.join(out_dir, "chromedriver.zip")
    with open(zip_path, "wb") as f:
        f.write(requests.get(zip_url).content)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(out_dir)
    os.remove(zip_path)

def download_chrome_binary(driver_ver, out_dir):
    zip_url = f"https://storage.googleapis.com/chrome-for-testing-public/{driver_ver}/win64/chrome-win64.zip"
    zip_path = os.path.join(out_dir, "chrome.zip")
    with open(zip_path, "wb") as f:
        f.write(requests.get(zip_url).content)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(out_dir)
    os.remove(zip_path)

def ensure_driver_and_browser():
    fallback_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    chrome_version = get_installed_chrome_version()
    if not chrome_version:
        print("⚠ Chrome version not detected — using fallback ChromeDriver.")
        driver_ver = requests.get(fallback_url).text.strip()
    else:
        major = chrome_version.split('.')[0]
        release_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major}"
        resp = requests.get(release_url)
        if resp.status_code != 200 or "<Error>" in resp.text:
            print(f"❌ No ChromeDriver for system Chrome {chrome_version} — using fallback.")
            driver_ver = requests.get(fallback_url).text.strip()
        else:
            driver_ver = resp.text.strip()

    base_path = os.path.join("stealth_selenium", "bin", f"Chrome_{driver_ver}")
    os.makedirs(base_path, exist_ok=True)

    driver_path = os.path.join(base_path, "chromedriver.exe")
    browser_path = os.path.join(base_path, "chrome-win64", "chrome.exe")

    if not os.path.exists(driver_path):
        print(f"⬇ Downloading ChromeDriver {driver_ver}...")
        download_chromedriver(driver_ver, base_path)

    if not os.path.exists(browser_path):
        print(f"⬇ Downloading Chrome binary {driver_ver}...")
        download_chrome_binary(driver_ver, base_path)

    return driver_path, browser_path