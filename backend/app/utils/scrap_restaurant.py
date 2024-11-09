import json
import asyncio
from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
# Function to set up Selenium asynchronously and interact with the webpage

async def setup_selenium(url):
    print("Setting up selenium driver for ", url)
    selenium_url = "http://172.18.0.2:4444/wd/hub"
    # Configure Selenium options (headless)
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    # options.add_argument("--disable-software-rasterizer")
    # options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Remote(command_executor=selenium_url, options=options)
        driver.get(url)

        read_more_click_script = """
        const buttons = document.getElementsByClassName("sc-ya2zuu-0 SWRrQ");
        for(const button of buttons) {
            button.click();
        }
        """

        driver.execute_script(read_more_click_script)

        scroll_script = """
        async function scrollToBottomSmoothly() {
            const distance = document.documentElement.scrollHeight - window.pageYOffset;
            const duration = 500;
            let startTime = Date.now();

            while (Date.now() - startTime < duration) {
                const progress = Math.min((Date.now() - startTime) / duration, 1);
                window.scrollTo(0, window.pageYOffset + distance * progress);
                await new Promise(r => setTimeout(r, 16));
            }
        }
        scrollToBottomSmoothly();
        """
        driver.execute_script(scroll_script)
        
        # Wait for specific elements to load
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
        driver.implicitly_wait(2)

        return driver
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error setting up Selenium: {str(e)}")

# Function to scrape restaurant data asynchronously
async def scrape_restaurant_data(url):
    driver = await setup_selenium(url)
    restaurant_data = {
        "name": "",
        "description": "",
        "location": "",
        "menu": []
    }
    print("Extracting the data")
    # Extract name
    name_elem = driver.find_element(By.CSS_SELECTOR, 'h1.sc-7kepeu-0.sc-iSDuPN.fwzNdh')  # Update with actual class name
    restaurant_data["name"] = name_elem.text.strip() if name_elem else ""

    # Extract location
    location_elem = driver.find_element(By.CSS_SELECTOR, 'a.sc-clNaTc.vNCcy')  # Update with actual class name
    restaurant_data["location"] = location_elem.text.strip() if location_elem else ""

    # Extract menu categories and items
    menu_categories = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1hp8d8a-0')  # Update with actual class name
    for category in menu_categories:
        category_name = category.text.strip()
        parent = category.find_element(By.XPATH, '..')
        menu_items = parent.find_elements(By.CSS_SELECTOR, 'div.sc-1s0saks-17')  # Update with actual class name
        
        category_items = []
        for item in menu_items:
            item_name = item.find_element(By.TAG_NAME, 'h4').text.strip() if item.find_elements(By.TAG_NAME, 'h4') else ""
            item_description = item.find_element(By.TAG_NAME, 'p').text.strip() if item.find_elements(By.TAG_NAME, 'p') else ""
            item_price = item.find_element(By.CSS_SELECTOR, 'span.sc-17hyc2s-1').text.strip().replace("\u20b9", "") if item.find_elements(By.CSS_SELECTOR, 'span.sc-17hyc2s-1') else ""
            
            # Handle images from lazy-loading attributes
            item_image_url = item.find_element(By.TAG_NAME, 'img') if item.find_elements(By.TAG_NAME, 'img') else None
            image_url = item_image_url.get_attribute('src') if item_image_url else ""

            item_type = item.find_element(By.CLASS_NAME, 'sc-1tx3445-0.kcsImg.sc-1s0saks-0.jcidl') if item.find_elements(By.CLASS_NAME, 'sc-1tx3445-0.kcsImg.sc-1s0saks-0.jcidl') else None

            # Prepare menu item dictionary
            category_item = {
                "name": item_name,
                "price": item_price,
                "description": item_description,
                "image_url": image_url,
                "type": item_type.get_attribute("type") if item_type else ""
            }

            category_items.append(category_item)

        restaurant_data["menu"].append({
            "category": category_name,
            "items": category_items
        })

    driver.quit()
    return restaurant_data

# Function to get restaurant coordinates asynchronously
async def get_restaurant_coordinates(url):
    print("Extracting the coordinates")
    driver = await setup_selenium(url)

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))

    # Extract coordinates
    h5 = driver.find_element(By.CSS_SELECTOR, 'h5.sc-1uh2q3e-0.cXEaB')
    parent = h5.find_element(By.XPATH, '..')
    links = parent.find_elements(By.TAG_NAME, 'a')
    coordinates_url = links[1].get_attribute('href')
    driver.quit()

    if coordinates_url:
        coordinates = coordinates_url.split("=")[-1]
        return coordinates
    
# Main function to scrape restaurant data and coordinates asynchronously
async def get_restaurant_details(base_url):
    order_url = f"{base_url}/order"
    restaurant_data = await scrape_restaurant_data(order_url)
    print("Restaurnt data extracted")
    print(json.dumps(restaurant_data, indent=2))
    coordinates = await get_restaurant_coordinates(base_url)
    restaurant_data["coordinates"] = coordinates
    
    print(json.dumps(restaurant_data, indent=2))
    # print(restaurant_data)

    return restaurant_data