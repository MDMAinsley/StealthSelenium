import os
import json
import shutil
import tempfile

def find_chrome_profiles():
    base_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
    if not os.path.exists(base_path):
        print("⚠ Chrome profile directory not found.")
        return []

    profiles = []
    for folder in os.listdir(base_path):
        full_path = os.path.join(base_path, folder)
        if folder.lower().startswith("profile") or folder == "Default":
            pref_file = os.path.join(full_path, "Preferences")
            if os.path.exists(pref_file):
                try:
                    with open(pref_file, "r", encoding="utf-8") as f:
                        prefs = json.load(f)
                    name = prefs.get("profile", {}).get("name", folder)
                    profiles.append({
                        "folder": folder,
                        "name": name,
                        "profile_dir": folder,
                        "user_data_dir": base_path
                    })
                except:
                    pass
    return profiles

def prompt_profile_selection():
    profiles = find_chrome_profiles()
    if not profiles:
        print("No Chrome profiles detected.")
        return None, None

    print("\nAvailable Chrome profiles:\n")
    for i, prof in enumerate(profiles, start=1):
        print(f"{i}. {prof['name']} ({prof['folder']})")

    try:
        choice = int(input("\nSelect a profile [1 - %d]: " % len(profiles)))
        selected = profiles[choice - 1]
        return clone_profile(selected["profile_dir"], selected["user_data_dir"])
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return None, None

def clone_profile(profile_dir, user_data_dir):
    temp_root = tempfile.mkdtemp(prefix="ChromeProfile_")
    source = os.path.join(user_data_dir, profile_dir)
    target = os.path.join(temp_root, profile_dir)
    shutil.copytree(source, target, dirs_exist_ok=True)
    return temp_root, profile_dir  # Return path as user_data_dir + profile_dir

