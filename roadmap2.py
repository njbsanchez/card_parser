from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome("/Users/nsanchez/Desktop/tools_build/chromedriver", options=options)

import time


url = 'https://www.atlassian.com/roadmap/cloud'

driver.get(url)
more_buttons = driver.find_elements(By.CLASS_NAME, value="moreLink")
for x in range(len(more_buttons)):
  if more_buttons[x].is_displayed():
      driver.execute_script("arguments[0].click();", more_buttons[x])
      time.sleep(1)
      
page_source = driver.page_source

from bs4 import BeautifulSoup

soup = BeautifulSoup(page_source, 'lxml')

# Import the required modules
import json


# Function will return a list of dictionaries
# each containing information of books.
def json_from_html_using_bs4(soup_base):

	soup = soup_base

	# soup.find_all finds the div's, all having the same
	# class "col-xs-6 col-sm-4 col-md-3 col-lg-3" that is
	# stored in books
	books = soup.find_all(
		'li', attrs={'class':
				'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

	# Initialise the required variables
	star = ['One', 'Two', 'Three', 'Four', 'Five']
	res, book_no = [], 1
	
	# Iterate books classand check for the given tags
	# to get the information of each books.
	for book in books:

		# Title of book in <img> tag with "alt" key.
		title = book.find('img')['alt']

		# Link of book in <a> tag with "href" key
		link = base_url[:37] + book.find('a')['href']

		# Rating of book from

<p> tag
		for index in range(5):
			find_stars = book.find(
			'p', attrs={'class': 'star-rating ' + star[index]})
			
			# Check which star-rating class is not
			# returning None and then break the loop
			if find_stars is not None:
				stars = star[index] + " out of 5"
				break

		# Price of book from

<p> tag in price_color class
		price = book.find('p', attrs={'class': 'price_color'
													}).text

		# Stock Status of book from

<p> tag in
		# instock availability class.
		instock = book.find('p', attrs={'class':
						'instock availability'}).text.strip()
		
		# Create a dictionary with the above book information
		data = {'book no': str(book_no), 'title': title,
			'rating': stars, 'price': price, 'link': link,
			'stock': instock}

		# Append the dictionary to the list
		res.append(data)
		book_no += 1
	return res


# Main Function
if __name__ == "__main__":

	# Enter the url of website
	base_url = "https://books.toscrape.com/catalogue/page-1.html"

	# Function will return a list of dictionaries
	res = json_from_html_using_bs4(base_url)

	# Convert the python objects into json object and export
	# it to books.json file.
	with open('books.json', 'w', encoding='latin-1') as f:
		json.dump(res, f, indent=8, ensure_ascii=False)
	print("Created Json File")
