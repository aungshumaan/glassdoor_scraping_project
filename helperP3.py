
"""
Based on code created by Diego De Lazzari
Modified for Python 3 by Aungshuman Zaman

"""
from selenium import webdriver
#from bs4 import BeautifulSoup # For HTML parsing
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
from selenium.webdriver.common import action_chains, keys
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import pickle
import re
import csv

def init_driver():
    ''' Initialize chrome driver'''
    
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    #browser = webdriver.Chrome(driver, chrome_options=chrome_options)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #browser = webdriver.Chrome()

    return browser

##############################################################################

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
############################################################################### 
        
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)     
###############################################################################

def get_pause():
    return np.random.choice(range(4,6)) 

###############################################################################
#utility function to get csv file from pickle.
def get_csv(pickle_obj):
    my_dict = load_obj(pickle_obj)
    csv_filename = 'mycsvfile.csv'
    with open(csv_filename, 'w') as f:  # Just use 'w' mode in 3.x
        writer = csv.writer(f)

        for k,v in my_dict.items():
            if len(v) == 6:
                new_dict = {}
                new_dict['job_id'] = k
                new_dict['rating'] = v[0] 
                new_dict['position'] = v[1]
                new_dict['company_name'] = v[2]
                new_dict['salary'] = v[3]
                new_dict['link'] = v[4]
                new_dict['description'] = v[5]
                writer.writerow(new_dict.values())
    

###############################################################################

def searchJobs(browser, jobName, city=None, jobDict = None, link=None):
    '''Scrape for job listing'''

    
    q = input('Shall we scrape? (y/n)\n') #q = raw_input('Shall we scrape? (y/n)')
    
    if q=='y':
        
        job = browser.find_element_by_id("KeywordSearch")  #job title, keywords, or company
        location = browser.find_element_by_id("LocationSearch") #location search
        sleep(3)
        job.send_keys(jobName)  #type in job name in search
        sleep(2)
        #location form is already populated. 
        location.clear() 
        # can also execute JavaScript to clear it
        #browser.execute_script("arguments[0].value = ''", location) 
        location.send_keys(city) #type in location name in search
        
        sleep(2)
        #deal with pop-up
        browser.find_element_by_class_name('gd-btn-mkt').click()
        
        sleep(5)

        # Set up starting page 
        #initial_url = browser.current_url
    
        
        # Find brief description
        
        
        for i in range(25): #25
            try:
                # Extract useful classes
                jobPosting =browser.find_elements_by_class_name('jl')
                sleep(get_pause())
                
                # Create a job Dictionary. Every job in glassDoor has a unique data-id.
                # data-id should be used as key for the dictionary
                #create a map of 2-tuple. 2-tuple => data-id and selenium webElement.
                jobTuple = map(lambda a: (a.get_attribute('data-id'), a), jobPosting) 
                
                # Filter picks out only those data-ids that are not in jobDict.keys()  
                newPost = list(filter(lambda b: b[0] not in jobDict.keys(),jobTuple) ) #list of 2-tuple
                            
                #If there are new posts, update job dict and link list
                if newPost != []:
    
                    # process the tuple
                    #jobData = list(map(lambda a: (a[0],a[1].text.encode("utf8")./
                        #split('\n')[0:4]),newPost))
                    jobData = list(map(lambda a: (a[0],a[1].text.split('\n')[0:4]),newPost))
                    # Update job dictionary   
                    tmp = dict((a[0],a[1]) for a in jobData)
                    jobDict.update(tmp)
                    # finally find the links: 
                    link_lst = list(map(lambda c: (c[0],c[1].find_element_by_tag_name('a').\
                        get_attribute('href')), newPost))
                    #add the link to job dict
                    tmp = [jobDict[c[0]].append(c[1]) for c in link_lst]
                    # update link list. This will be used in get_data part.
                    link += link_lst

                
                browser.find_element_by_class_name('next').click()
                try:
                    browser.find_element_by_class_name('xBtn').click()
                except:
                    pass
                    
            except Exception as e:
                #pass
                print(type(e),e)
            
    return jobDict, link
    
###############################################################################    

def text_cleaner(text):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    #print('starting text_cleaner')
    stopws = set(stopwords.words("english"))
    #print('initialized stopws')
    
    lines = (line.strip() for line in text.splitlines()) # break into lines
    #lines = [line.strip() for line in text.splitlines()]
        
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    #chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out  
        
    #print('Going for text!')
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
    
        
    # Now clean out all of the unicode junk (this line works great!!!)
    #print('cleaning out unicode junc from text!')    
    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore') # Need this as some websites aren't formatted
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception
       
    #print('getting rid of non-words from text!')        
    text = re.sub(b"[^a-zA-Z.+3]",b" ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
                                                # Also include + for C++
        
    #print('make text lower case!')       
    text = text.lower()  # Go to lower case
    
    #print('split text!')       
    text = text.split()  #  and split them apart
    
    #print('removing stop words!')       
    text = [w for w in text if not w in stopws]
        
        
    #print('set of text')       
    text = list(set(text)) # Last, just get the set of these. Ignore counts 
                           # we are just looking at whether a term existed or not on the website
 
    #print("We are done! Let's return it!")    
    return text 
    
    
##############################################################################
    