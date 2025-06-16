import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time

def extract_model_and_color(code_text):
    code_text = code_text.strip()
    if ":" in code_text:
        code_text = code_text.split(":")[1].strip()
    parts = code_text.replace(" ", "").split("-")
    if len(parts) >= 2:
        model_no = "-".join(parts[:-1]).upper()
        color_code = parts[-1].upper()
        return model_no, color_code
    else:
        return code_text.upper(), ""

category_base = f"https://www.emag.ro/genti-dama/brand/19v69-italia,calvin-kelin,calvin-klein,calvin-klein-jeans,guess,guess-jeans,jacquemus,karl-lagerfeld,karl-lagerfeld-jeans,lacoste,love-moschino,mango,marc-jacobs,mario-valentino,michael-kors,michael-michael-kors,tommy-hilfiger,tommy-jeans,valentino,valentino-bags/"
product_links = set()

# Step 1: Collect product links from first 10 pages
driver = uc.Chrome()
for page in range(1, 11):  # 1 to 10
    url = f"{category_base}p{page}/c"
    driver.get(url)
    time.sleep(6)
    cards = driver.find_elements(By.CSS_SELECTOR, "a.js-product-url")
    for card in cards:
        link = card.get_attribute("href")
        if link:
            product_links.add(link)
    print(f"Page {page}: Collected {len(cards)} links, total unique: {len(product_links)}")
driver.quit()

# Step 2: Visit each product detail page and extract model_no/color_code
driver = uc.Chrome()
all_products = []
for idx, link in enumerate(product_links):
    try:
        driver.get(link)
        time.sleep(4)
        try:
            code_span = driver.find_element(By.CSS_SELECTOR, ".product-code-display")
            code_text = code_span.text.strip()
            model_no, color_code = extract_model_and_color(code_text)
        except Exception as e:
            print(f"Could not extract code from {link}: {e}")
            model_no, color_code = "", ""
        all_products.append({
            "url": link,
            "model_no": model_no,
            "color_code": color_code
        })
        print(f"[{idx+1}/{len(product_links)}] Got: {model_no} / {color_code}")
    except Exception as e:
        print(f"Failed to process {link}: {e}")
        all_products.append({
            "url": link,
            "model_no": "",
            "color_code": ""
        })
driver.quit()

# Step 3: Save to CSV
df = pd.DataFrame(all_products)
print(df.head())  # Show the first few rows for debug
df.to_csv("/Users/ataberkcinetci/Desktop/untitled folder/emag_products_first_10pages.csv", index=False)
print("Done! Saved all results to emag_products_first_10pages.csv.")
