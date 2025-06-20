import undetected_chromedriver as uc
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def inject_fingerprint_spoofing(driver):
    spoof_js = """
    const getContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, ...args) {
        const context = getContext.call(this, type, ...args);
        if (type === "2d") {
            const originalGetImageData = context.getImageData;
            context.getImageData = function(x, y, w, h) {
                const imageData = originalGetImageData.call(this, x, y, w, h);
                imageData.data[0] += 1;
                return imageData;
            };
        }
        return context;
    };

    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(param) {
        if (param === 37445) return "Intel Inc.";
        if (param === 37446) return "Intel Iris OpenGL Engine";
        return getParameter.call(this, param);
    };
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": spoof_js})

def get_stealth_browser(profile_dir=None, user_data_dir=None, proxy=None, cookie_path=None, load_cookies=False):
    if not user_data_dir and not (cookie_path and load_cookies):
        raise ValueError("You must provide either a Chrome user profile (user_data_dir) or load cookies for stealth.")

    options = uc.ChromeOptions()

    if user_data_dir:
        options.add_argument(f'--user-data-dir={user_data_dir}')
    if profile_dir:
        options.add_argument(f'--profile-directory={profile_dir}')

    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = False

    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    driver = uc.Chrome(options=options)
    inject_fingerprint_spoofing(driver)

    if load_cookies and cookie_path:
        try:
            load_cookies_from_file(driver, cookie_path)
            logger.info("Loaded cookies from %s", cookie_path)
        except Exception as e:
            logger.warning("Failed to load cookies: %s", str(e))

    return driver

def save_cookies_to_file(driver, path):
    cookies = driver.get_cookies()
    with open(path, 'w') as f:
        json.dump(cookies, f)
    logger.info("Cookies saved to %s", path)

def load_cookies_from_file(driver, path):
    with open(path, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    logger.debug("Cookies loaded from file")
