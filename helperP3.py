# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 21:12:30 2016

@author: Diego
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

def init_glassdoor():
    ''' Initialize chrome driver'''
    
    chrome_options = webdriver.ChromeOptions()
    
    #driver = '/Users/Diego/Documents/NYCDSA/Project 3/chromedriver'
    
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    return browser

##############################################################################

