from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

from bs4 import BeautifulSoup
import json



options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome("/Users/nsanchez/Desktop/tools_build/chromedriver", options=options)



# url = 'https://author.marketing.internal.atlassian.com/wac/roadmap/data-center?mgnlVersion=1.23'

# driver.get(url)
# more_buttons = driver.find_elements(By.CLASS_NAME, value="moreLink")
# for x in range(len(more_buttons)):
#   if more_buttons[x].is_displayed():
#       driver.execute_script("arguments[0].click();", more_buttons[x])
#       time.sleep(1)
      
# page_source = driver.page_source

with open("v_12_16.html", "r", encoding='utf-8') as f:
    text= f.read()

page_source = text

soup = BeautifulSoup(page_source, 'lxml')

  
content = soup.find_all(class_='inner')  
    
    
cards_dictionary = {}


for i,card in enumerate(content,start=1):
    
    title = str(card.h4.string)
    print('*************')
    print(title)
    desc = 'N/A' if card.find(class_="description").p is None else str(((card.find(class_="description")).p.contents)[0])
    status = str(card.find(class_="custom-category").contents[0])
    try:
        category = str(card.find(class_="custom-category2").contents[0])
    except:
        category = str("none")
    try:
        date = str(card.find(class_="custom-field-1").contents[0])
    except:
        date = str("none")
    products = []
    try:
        for product in card.find(class_="custom-product").contents:
            products.append(str(product.string))
    except:
        products = card.find(class_="custom-field-2").contents[0]
            

    cards_dictionary[i]={'title':title,
             'description':desc,
             'status':status,
             'category':category,
             'date':date,
             'products':products
             }


from datetime import date

today = date.today()
# print("Today's date:", today)

file_name = f'cloud_cards_{today}'

with open(f'json_outputs/{file_name}.json', 'w') as outfile:
    json.dump(cards_dictionary, outfile)
    
    
y=json.dumps(cards_dictionary)

print(y)

  


df = (pd.DataFrame.from_dict(cards_dictionary)).T

file = f'csv_outputs/{file_name}.csv'
df.to_csv (file, index = True, header=True)
    
    

