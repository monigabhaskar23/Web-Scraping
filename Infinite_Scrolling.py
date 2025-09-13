from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Path to your downloaded driver
service = Service("E:\DATA_SCIENCE\chromedriver-win64\chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.nike.com/ca/w/sale-shoes-3yaepzy7ok")

last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height
    
#Imports the HTML of the webpage into python  
soup = BeautifulSoup(driver.page_source, 'lxml')
#print(soup)

#grabs the HTML of each product
product_card = soup.find_all('div', class_ = 'product-card__body')
#print(product_card)

data = []
for product in product_card:
    try:
        link_tag = product.find('a', class_='product-card__link-overlay')
        link = 'https://www.nike.com' + link_tag['href'] if link_tag else ''

        name_tag = product.find('div', class_='product-card__title')
        name = name_tag.text.strip() if name_tag else ''

        subtitle_tag = product.find('div', class_='product-card__subtitle')
        subtitle = subtitle_tag.text.strip() if subtitle_tag else ''

        # Use more general selectors for prices
        full_price_tag = product.find('div', class_=lambda x: x and 'is--striked-out' in x)
        sale_price_tag = product.find('div', class_=lambda x: x and 'is--current-price' in x)
        full_price = full_price_tag.text.strip() if full_price_tag else ''
        sale_price = sale_price_tag.text.strip() if sale_price_tag else ''

        data.append({
            'Link': link,
            'Name': name,
            'Subtitle': subtitle,
            'Price': full_price,
            'Sale Price': sale_price
        })
    except Exception as e:
        print("Skipped product:", e)
        continue

df = pd.DataFrame(data)

df.to_csv(r'E:\DATA_SCIENCE\scalar\nike_data.csv')