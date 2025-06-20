# stealth_selenium

A stealth-focused Selenium wrapper for Python that avoids detection by simulating human behavior, using undetected-chromedriver, and masking fingerprinting (canvas/WebGL).

## Features

- ✅ Uses `undetected-chromedriver` to bypass detection
- 👤 Uses real Chrome profiles or cookies for persistence
- 🐭 Human-like scrolls, delays, and dwell time before clicks
- 🖼️ Canvas and WebGL fingerprint spoofing
- 🔁 Retry mechanism for fragile interactions
- 📜 Basic logging included for observability

## Installation

```bash
pip install -r requirements.txt
```

Or install from GitHub in other projects:

```bash
pip install git+https://github.com/YOUR_USER/stealth_selenium.git
```

## Example

```python
from stealth_selenium.browser import get_stealth_browser
from stealth_selenium.interactions import find_and_click, type_like_human
from selenium.webdriver.common.by import By

driver = get_stealth_browser(profile_dir="Default", user_data_dir="C:/Users/you/AppData/Local/Google/Chrome/User Data")
driver.get("https://example.com")

box = driver.find_element(By.NAME, "q")
type_like_human(box, "stealth selenium")
find_and_click(driver, By.NAME, "btnK")
```
