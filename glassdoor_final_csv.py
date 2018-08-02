from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import csv
import re

from helperP3 import init_glassdoor

# driver = webdriver.Chrome(r'path\to\where\you\download\the\chromedriver.exe')
driver = init_glassdoor()  
#driver = webdriver.Chrome()
driver.get("https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm")
# Click review button to go to the review section


csv_file = open('gd_reviews.csv', 'a')
writer = csv.writer(csv_file)
jobs =  driver.find_elements_by_xpath('//*[@id="MainCol"]/div/ul//div[2]/div[1]/div[1]/a')
#jobs = driver.find_elements_by_xpath('//li[@data-normalize-job-title="data scientist"]')


print(len(jobs))
index = 0
errorCount = 0
for job in jobs: #debugging  [10:13]
	index = index+1
	print(' job #{num}'.format(num=index))
	review_dict = {}

	job.click()
	time.sleep(2)
	try:
		driver.find_element_by_xpath('//*[@id="JAModal"]//div[@class="xBtn"]').click()
	except WebDriverException:
		#print('nothing to cross out')
		pass

	try:
		driver.find_element_by_xpath('//div[1]/div[2]/header/ul/li[2]').click()
		text2 = driver.find_element_by_xpath('//*[@id="CompanyContainer"]').text


		driver.find_element_by_xpath('//div[1]/div[2]/header/ul/li[1]').click()
		text1 = driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]').text


		driver.find_element_by_xpath('//div[1]/div[2]/header/ul/li[3]/span').click()
		text3 = driver.find_element_by_xpath('//*[@id="RatingContainer"]').text
	
	
		el4  = driver.find_element_by_xpath('//div[1]/div[2]/header/ul/li[4]/span')
		driver.execute_script("arguments[0].click();", el4)
		text4 = driver.find_element_by_xpath('//*[@id="ReviewsContainer"]').text  #need to separate individual reviews
	
		review_dict['Job_decr']= text1
		review_dict['company']= text2
		review_dict['rating']= text3 
		review_dict['review']= text4
	
	
		writer.writerow(review_dict.values())
	except:
		#pass
		errorCount +=1


print(errorCount)

#review_button.click()

'''

# Windows users need to open the file using 'wb'
# csv_file = open('reviews.csv', 'wb')
csv_file = open('reviews.csv', 'w')
writer = csv.writer(csv_file)
# Page index used to keep track of where we are.
index = 1
while index <=2:  ###while True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the reviews on the page
		wait_review = WebDriverWait(driver, 10)
		reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
									'//div[@itemprop="review"]')))
		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			# Use relative xpath to locate the title, text, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			title = review.find_element_by_xpath('.//div[@itemprop="headline"]').text
			text = review.find_element_by_xpath('.//span[@itemprop="reviewBody"]').text
			username = review.find_element_by_xpath('.//span[@itemprop="author"]').text
			date_published = review.find_element_by_xpath('.//meta[@itemprop="datePublished"]').get_attribute('content')
			rating = review.find_element_by_xpath('.//span[@itemprop="ratingValue"]').text

			review_dict['title'] = title
			review_dict['content'] = text
			review_dict['username'] = username
			review_dict['date_published'] = date_published
			review_dict['rating'] = rating
			writer.writerow(review_dict.values())

		# Locate the next button on the page.
		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//li[@class="nextClick displayInlineBlock padLeft5 "]')))
		next_button.click()
	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break
'''
