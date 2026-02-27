from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

MACRO_LIMIT = 255

def fetch_names(event_url):
    opt = Options()
    opt.add_argument("--headless=new")

    driver = webdriver.Chrome(options=opt)
    driver.get(event_url)

    time.sleep(2)

    names = set()

    container = driver.find_element(By.ID, "classes")
    elements = container.find_elements(By.XPATH,".//span[contains(@style,'font-weight: 700')]")

    for e in elements:
        name = e.text.strip()
        if 2 <= len(name) <= 12 and name.replace("-", "").isalpha():
            names.add(name)

    driver.quit()
    return sorted(names)

def generate_macros(names):
    macros = []
    current_macro = ""
    
    for n in names:
        line = f"/invite {n}\n"
        if len(current_macro) + len(line) > MACRO_LIMIT:
            macros.append(current_macro.strip())
            current_macro = line
        else:
            current_macro += line
    
    if current_macro:
        macros.append(current_macro.strip())
        
    return macros

def main():
    event_url = input("Paste the Raid-Helper event URL and press Enter:\n> ").strip()
    if not event_url.startswith("https://raid-helper.dev/event/"):
        print("Invalid Raid-Helper event URL.")
        return
    
    names = fetch_names(event_url)
    if not names:
        print("No names found. The page may require login or different selectors.")
        return
    
    macros = generate_macros(names)
    

    print("\n========================")
    print(f"Found {len(names)} players")
    print(f"Generated {len(macros)} macro(s)")
    print("========================\n")
    
    for i, macro in enumerate(macros, 1):
        print(f"--- Macro {i} ---\n")
        print(macro)
        print("\n")
        
if __name__ == "__main__":
    main()