# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:12:45 2020

@author: HP
"""

import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

os.chdir(r'F:/TEC/')
url1 = 'http://pds-geosciences.wustl.edu/mex/mex-m-marsis-5-ddr-ss-tec-v1/mexmds_2001/data/'
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text, 'html.parser')
for j in range(1,len(soup1.findAll('a'))):
    tag1 = soup1.findAll('a')[j]
    link1 = tag1['href']
    url = 'http://pds-geosciences.wustl.edu/'+ link1
#    print(url)
#   url = 'http://pds-geosciences.wustl.edu/mex/mex-m-marsis-5-ddr-ss-tec-ext1-v1/mexmds_2002/data/ddr299x/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in range(2,len(soup.findAll('a')),2):
        one_a_tag = soup.findAll('a')[i]
        link = one_a_tag['href']
        download_url = 'http://pds-geosciences.wustl.edu/'+ link
        urllib.request.urlretrieve(download_url, './'+link[link.find('/frm_tec_ddr_')+1:])
        time.sleep(1)