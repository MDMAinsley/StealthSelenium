import os
import json
import shutil
import tempfile

def find_chrome_profiles():
    base_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    if not os.path.exists(base_path):
        print("⚠ Chrome profile directory not found.")
        return []

    profiles = []
    for folder in os.listdir(base_path):
        full_path = os.path.join(base_path, folder)
        if folder.lower().startswith("profile") or folder == "default":
            pref_file = os.path.join(full_path, "Preferences")
            if os.path.exists(pref_file):
                try:
                    with open(pref_file, "r", encoding="utf-8") as f:
                        prefs = json.load(f)
                    name = prefs.get("profile", {}).get("name", folder)
                    last_used = prefs.get("profile", {}).get("last_used", "Unknown")
                    profiles.append({
                        "folder": folder,
                        "name": name,
                        "last_used": last_used,
                        "profile_dir": folder,
                        "user_data_dir": base_path
                    })
                except Exception as e:
                    print(f"⚠ Skipped corrupt profile {folder}: {e}")
    return profiles

def prompt_profile_selection():
    profiles = find_chrome_profiles()
    if not profiles:
        print("No Chrome profiles detected.")
        return None, None

    print("\n🧭 Available Chrome profiles:\n")
    for i, prof in enumerate(profiles, start=1):
        print(f"{i}. {prof['name']} ({prof['folder']})")

    try:
        choice = int(input("\nSelect a profile [1 - %d]: " % len(profiles)))
        selected = profiles[choice - 1]
        temp_dir, cloned_folder = clone_profile(selected["profile_dir"], selected["user_data_dir"])
        if validate_cloned_profile(temp_dir, cloned_folder):
            return temp_dir, cloned_folder
        else:
            print("❌ Profile clone invalid or missing required data.")
            return None, None
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return None, None

def clone_profile(profile_dir, user_data_dir):
    temp_root = tempfile.mkdtemp(prefix="ChromeProfile_")
    source = os.path.join(user_data_dir, profile_dir)
    target = os.path.join(temp_root, profile_dir)
    shutil.copytree(source, target, dirs_exist_ok=True)
    return temp_root, profile_dir

def validate_cloned_profile(temp_dir, profile_folder):
    pref_path = os.path.join(temp_dir, profile_folder, "Preferences")
    if not os.path.exists(pref_path):
        return False
    try:
        with open(pref_path, "r", encoding="utf-8") as f:
            prefs = json.load(f)
        # Check for basic keys that signal usability
        return "profile" in prefs and prefs["profile"].get("name")
    except:
        return False
