import json, time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

def wait_css(d, sel, t=12): 
    return WebDriverWait(d, t).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
def click_css(d, sel, t=12, attempts=3):
    for _ in range(attempts):
        try:
            el = WebDriverWait(d, t).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
            )
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            el.click()
            return
        except StaleElementReferenceException:
            time.sleep(0.3)  # DOM baru, coba lagi
    # kalau masih gagal, lempar error normal
    el = WebDriverWait(d, t).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
    )
    el.click()

def wait_url_contains(d, snippet, t=12):
    WebDriverWait(d, t).until(EC.url_contains(snippet))

def run(steps):
    d = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
        for s in steps:
            a = s["action"]
            if a=="open_url": d.get(s["value"])
            elif a=="fill": el = wait_css(d, s["selector"]); el.clear(); el.send_keys(s["value"])
            elif a=="click": click_css(d, s["selector"])
            elif a=="wait": wait_css(d, s["selector"], s.get("timeout",12))
            elif a=="sleep": time.sleep(s.get("seconds",1))
            elif a=="wait_text":
                el = wait_css(d, s["selector"]); WebDriverWait(d, s.get("timeout",12)).until(lambda _: s["value"] in el.text)
        input("✅ E2E done. Press Enter to close...")
    finally:
        d.quit()

if __name__ == "__main__":
    steps = json.loads((Path(__file__).parent/"steps.json").read_text(encoding="utf-8"))
    run(steps)
