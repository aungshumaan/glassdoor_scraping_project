from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import csv
import re


driver = webdriver.Chrome()
driver.get("https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm")


csv_file = open('gd_reviews.csv', 'a')
writer = csv.writer(csv_file)
jobs =  driver.find_elements_by_xpath('//*[@id="MainCol"]/div/ul//div[2]/div[1]/div[1]/a')
#jobs = driver.find_elements_by_xpath('//li[@data-normalize-job-title="data scientist"]')


print(len(jobs))
index = 0
errorCount = 0
for job in jobs[1:4]: #debugging  [10:13]
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
	except Exception as e:
		#pass
		print(type(e),e)
		errorCount +=1


print(errorCount)
