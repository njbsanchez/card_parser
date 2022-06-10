from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import date

from bs4 import BeautifulSoup
import json

def get_page_source(url):
    """
    takes in url of page, returns page source
    """
    
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    driver.get(url)
    more_buttons = driver.find_elements(By.CLASS_NAME, value="moreLink")
    for x in range(len(more_buttons)):
        if more_buttons[x].is_displayed():
            driver.execute_script("arguments[0].click();", more_buttons[x])
            time.sleep(1)
        
    page_source = driver.page_source
    
    return page_source

def get_page_taxonomy(page_source):
    """
    takes in page source, returns content taxonomy
    """
    soup = BeautifulSoup(page_source, 'lxml')
    content = soup.find_all(class_='inner')  
    
    return content
     
def create_card_dict(url):
    """
    takes in taxonomy, returns card_dictionary
    """
    
    page_source = get_page_source(url)
    content = get_page_taxonomy(page_source)
    
    cards_dictionary = {}

    for i,card in enumerate(content,start=1):
    
        title = str(card.h4.string)
        # print('*************')
        # print(title)
        desc = 'N/A' if card.find(class_="description").p is None else str(((card.find(class_="description")).p.contents)[0])
        try:
            status = str(card.find(class_="custom-category").contents[0])
        except:
            category = str("missing")
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
        try:
            for a in card.find_all('a', href=True):
                link = str(a['href'])
        except:
            link = str('none')

        cards_dictionary[i]={'title':title,
                'description':desc,
                'status':status,
                'category':category,
                'date':date,
                'products':products,
                'link':link
                }
    
    return cards_dictionary

def create_cloud_reports(cards_dictionary):
    
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
    
def create_dc_reports(cards_dictionary):
    
    today = date.today()
    # print("Today's date:", today)

    file_name = f'dc_cards_{today}'
    with open(f'json_outputs/{file_name}.json', 'w') as outfile:
        json.dump(cards_dictionary, outfile)
    
    y=json.dumps(cards_dictionary)
    print(y)
    
    df = (pd.DataFrame.from_dict(cards_dictionary)).T
    file = f'csv_outputs/{file_name}.csv'
    df.to_csv (file, index = True, header=True)
  
def parse_cloud(cloud_url):
    cloud_dictionary = create_card_dict(cloud_url)
    create_cloud_reports(cloud_dictionary)
    
def parse_dc(dc_url):
    dc_dictionary = create_card_dict(dc_url)
    create_dc_reports(dc_dictionary)


if __name__ == "__main__":
    
    # cloud_url = 'https://www.atlassian.com/roadmap/cloud'
    dc_url = 'https://www.atlassian.com/roadmap/data-center'

    # parse_cloud(cloud_url)
    parse_dc(dc_url)
    

