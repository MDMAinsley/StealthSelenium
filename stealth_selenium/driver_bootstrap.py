import subprocess
import re
import os
import requests
import zipfile

def get_installed_chrome_version():
    try:
        output = subprocess.check_output(
            r'reg query "HKCU\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        ).decode()
        match = re.search(r"version\s+REG_SZ\s+([^\s]+)", output)
        return match.group(1) if match else None
    except Exception as e:
        print(f"⚠ Could not detect Chrome version: {e}")
        return None

def get_or_download_chromedriver(storage_dir="drivers"):
    version = get_installed_chrome_version()
    if not version:
        print("⚠ No installed Chrome version detected.")
        return None

    major = version.split('.')[0]
    release_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major}"
    resp = requests.get(release_url)
    driver_version = "Empty"

    print("Driver metadata response:", resp.text[:200])

    if resp.status_code != 200 or "<Error>" in resp.text:
        print(f"❌ No ChromeDriver available for version: {version} — falling back.")
        latest_resp = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        fallback_version = latest_resp.text.strip()
        print(f"🔁 Using fallback ChromeDriver: {fallback_version}")
        driver_version = fallback_version

    target_dir = os.path.join(storage_dir, f"ChromeDriver_{driver_version}")
    os.makedirs(target_dir, exist_ok=True)
    exe_path = os.path.join(target_dir, "chromedriver.exe")

    if not os.path.exists(exe_path):
        zip_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
        zip_path = os.path.join(target_dir, "driver.zip")
        with open(zip_path, "wb") as f:
            f.write(requests.get(zip_url).content)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_dir)
        os.remove(zip_path)

    return exe_path

if __name__ == "__main__":
    get_or_download_chromedriver()
