import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time

all_products = []


for page in range(31,61): 
    
    url = f"https://www.emag.ro/genti-dama/brand/19v69-italia,calvin-kelin,calvin-klein,calvin-klein-jeans,guess,guess-jeans,jacquemus,karl-lagerfeld,karl-lagerfeld-jeans,lacoste,love-moschino,mango,marc-jacobs,mario-valentino,michael-kors,michael-michael-kors,tommy-hilfiger,tommy-jeans,valentino,valentino-bags/p{page}/c"
    driver = uc.Chrome()
    driver.get(url)
    time.sleep(7)
    
    if page == 1:
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]").click()
            time.sleep(1)
            
        except:
            pass

    for _ in range(1,2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    cards = driver.find_elements(By.CSS_SELECTOR, "a.js-product-url")
    print(f"Page {page}: Found {len(cards)} products.")

    for card in cards:
        parent = card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'card-v2')]")
        try:
            link = card.get_attribute('href')
            img = card.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
            title = card.find_element(By.CSS_SELECTOR, "img").get_attribute('alt')
            try:
                price_el = parent.find_element(By.CSS_SELECTOR, ".product-new-price")
                price = price_el.text.strip().replace('\n', '').replace('\xa0', ' ')
            except Exception as e:
                price = "N/A"
                
            try:
                model_no = parent.find_element(By.CSS_SELECTOR, ".product-code-display.hidden-xs").text.strip()
                if "Cod produs:" in model_no:
                    model_no = model_no.split("Cod produs:")[1].strip()
                elif "Product code:" in model_no:
                    model_no = model_no.split("Product code:")[1].strip()
            except Exception as e:
                model_no = "N/A"
                print(e)
            


            def extract_model_and_color(link):
                try:
                    url = link.rstrip('/')
                    before_pd = url.split('/pd/')[0]
                    parts = before_pd.split('-')
                    if len(parts) >= 2:
                        model_number_new = parts[-2].upper()
                        color_code = parts[-1].upper()
                        return model_number_new, color_code
                    else:
                        return "", ""
                except Exception:
                    return "", ""
                
            model_number_new, color_code = extract_model_and_color(link)
            all_products.append({
            "title": title,
            "link": link,
            "image_url": img,
            "price": price,
            "model_no": model_no,
            "model_no2": model_number_new,
            "color_code": color_code
        })
        except Exception as e:
            print("Error extracting product:", e)
   

driver.quit()
    


df = pd.DataFrame(all_products)
df.to_csv("/Users/ataberkcinetci/Desktop/emag_genti_dama_all_pages4.csv", index=False)
print("Saved all products to emag_genti_dama_all_pages.csv")
