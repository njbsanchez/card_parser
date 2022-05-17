# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By


# options = Options()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')

# driver = webdriver.Chrome("/Users/nsanchez/Desktop/tools_build/chromedriver", options=options)

# import time

# driver.get("https://www.tripadvisor.com/Airline_Review-d8729157-Reviews-Spirit-Airlines#REVIEWS")
# more_buttons = driver.find_elements(By.CLASS_NAME, value="moreLink")
# for x in range(len(more_buttons)):
#   if more_buttons[x].is_displayed():
#       driver.execute_script("arguments[0].click();", more_buttons[x])
#       time.sleep(1)
      
# page_source = driver.page_source

# from bs4 import BeautifulSoup

# soup = BeautifulSoup(page_source, 'lxml')
# print(soup)
# # reviews = []
# # reviews_selector = soup.find_all('div', class_='reviewSelector')
# # for review_selector in reviews_selector:
# #     review_div = review_selector.find('div', class_='dyn_full_review')
# #     if review_div is None:
# #         review_div = review_selector.find('div', class_='basic_review')
# #     review = review_div.find('div', class_='entry').find('p').get_text()
# #     review = review.strip()
# #     reviews.append(review)
    
# # print(reviews)

from datetime import datetime

today = datetime.today()
print("Today's date:", today)