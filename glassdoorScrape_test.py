from selenium import webdriver
#from bs4 import BeautifulSoup # For HTML parsing
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
from selenium.webdriver.common import action_chains, keys
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import sys
import re


# call the helper

from helperP3 import load_obj, save_obj, init_driver, searchJobs, text_cleaner, get_pause, \
string_from_text
	
# 1- Load existing dictionary. Check for initial dictionary. 
# If empty initialize
		
try:               
	jobDict = load_obj('glassDoorDict')
	link =    load_obj('glassDoorlink')
except:
	save_obj([], 'glassDoorlink')
	save_obj({}, 'glassDoorDict')
	
	jobDict = load_obj('glassDoorDict')
	link =    load_obj('glassDoorlink')    

print('len(jobDict) = '+str(len(jobDict))+ ', len(link) = '+str(len(link)))

# 2- Choose what you want to do: 
#    get_link => Scraping for links and brief data, 
#    get_data => Scraping for detailed data.


get_link = True ####&&&&
#get_link = False


get_data = (not get_link) # either get_link or get_data

if get_link or get_data:
	
# 3- initialize website
	
	website = "https://www.glassdoor.com/index.htm"
	
	# Initialize the webdriver
	
	browser = init_driver()  
	#browser = webdriver.Chrome()

# 4- Scrape for links and brief data


if get_link:

	browser.get(website)

	# Initialize cities and jobs

	#jobName_lst = ['Data Scientist', 'Data Analyst','Data Engineer']
	#jobName = np.random.choice(jobName_lst)
	jobName = 'Data Scientist' ####&&&&

	#city_lst = ['San Jose','New York','San Francisco','Detroit','Washington','Austin','Boston','Seattle','Chicago','Los Angeles',' ']
	#city = np.random.choice(city_lst)  
	city = 'New York'  ####&&&&

	print('jobName = '+jobName+ ', city = '+city)    
		
	# search for jobs (short description) 
	try:    
		# jobDict structure {'job_id':['rating','position','company','salary']}
		update_jobDict, update_link = searchJobs(browser, jobName, city, jobDict, link)
		sleep(get_pause())
	except Exception as e:
		print(type(e),e)
		sys.exit("Error message")
		#pass
		
		
	print('len(update_jobDict) = '+str(len(update_jobDict))+ ', len(update_link) = '+str(len(update_link)))
	
	# save dictionary and link     

	save_obj(update_jobDict, 'glassDoorDict')
	save_obj(update_link, 'glassDoorlink')
	
 # 5- Scrape the job description, for every link
				
if get_data:        
	
	print('len(link) = '+str(len(link)))
	while len(link) > 50: # originally 0, a hard coded solution for when only bad links are left.
	#for i in range(10): # debugging	
		 
		try:
			rnd_job = np.random.choice(range(len(link)))
			#print(rnd_job)
			ids = link[rnd_job][0]
			page = link[rnd_job][1]
			#print(ids)
			#print(page)
			
			browser.get(page)     
			#print(browser)            
			sleep(3)
			
			# Extract text   
			desc_list = browser.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div[1]').text
			#print('desc_list '+ str(type(desc_list)))
			description = text_cleaner(desc_list)
			#description = desc_list
			#print('description '+ str(type(description)))
			
			# jobDict structure {'job_id':['rating','position','company','salary','descr']}
			jobDict[ids].append(description)    
			
			
			#Additional information about company (size, revenue, industry)
			sleep(2)
			try:
				browser.find_element_by_xpath('//*[@id="JobContent"]//header/ul/li[2]/span').click()
				tmp_txt = browser.find_element_by_id('EmpBasicInfo').text
					
				hq_city = string_from_text('Headquarters', tmp_txt).split(',')[0]
				#print('hq_city = ',hq_city)
				jobDict[ids].append(hq_city)
				#print(' 1 = ',)
				hq_state_code = string_from_text('Headquarters', tmp_txt).split(',')[1]
				#print('hq_state_code = ',hq_state_code)
				jobDict[ids].append(hq_state_code)
				#print(' 2 = ',)
				#size_low = int(re.findall('\d+',string_from_text('Size',tmp_txt))[0])
				size = re.findall('\d+',string_from_text('Size',tmp_txt))
				#print('size = ', size)
				#size_high = int(re.findall('\d+',string_from_text('Size',tmp_txt))[1])
				#print(' = ',)
				jobDict[ids].append(size)
				#print(' 3 = ',)
				#jobDict[ids].append(size_low)
				#jobDict[ids].append(size_high)
				industry = string_from_text('Industry',tmp_txt)
				#print('industry = ',industry)

				jobDict[ids].append(industry)
				#print(' 4 = ',)
				#jobDict[ids].append(revenue)

				#size = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]//[@class=div[1]/div[1]/div[3]/span').text
				#size = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[3]/span').text
				#industry = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[6]/span').text
				#revenue = browser.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[1]/div[7]/span').text
			except Exception as e:
				print(type(e),e)

			#remove links already used
			           
			dummy=link.pop(rnd_job) 

			# if everything is fine, save
			#print("Going to save data!!")
			save_obj(jobDict, 'glassDoorDict')
			save_obj(link, 'glassDoorlink')
											
			print('Scraped successfully ' + ids)
			
			sleep(get_pause())
		except:   
			print( ids + ' is not working! Sleep for 6 seconds and retry')
			print( 'Still missing ' + str(len(link)) + ' links' )
			sleep(6)
	print('Done for now!! len(link) = '+str(len(link)))		
	browser.close()
 