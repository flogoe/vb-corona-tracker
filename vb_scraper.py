#!/usr/bin/env python3

import requests
import re
import string
import datetime
from bs4 import BeautifulSoup
from git import Repo


# PATH and FILENAMES
PATH = '/home/alfiron/Workspace/vb_scraper/data/'
# PATH = '/home/flg/vb_scraper/vb_scraper/data/'

KA_PREMIUM = "vb_data_ka_premium"
KA_LIFESTYLE = "vb_data_ka_lifestyle"
FRANKENTHAL = "vb_data_frankenthal"
KETSCH = "vb_data_ketsch"


PATH_OF_GIT_REPO = '/home/flg/vb_scraper/vb_scraper'
COMMIT_MESSAGE = 'Update data files'

# URLS 
URL_KA_PREMIUM = 'https://www.venicebeach-fitness.de/clubs/premium-fitness/karlsruhe-postgalerie/'
URL_KA_LIFESTYLE = 'https://www.venicebeach-fitness.de/clubs/lifestyle-fitness-plus/karlsruhe/'
URL_FRANKENTHAL = 'https://www.venicebeach-fitness.de/clubs/lifestyle-fitness-plus/frankenthal.html'
URL_KETSCH = 'https://www.venicebeach-fitness.de/clubs/premium-fitness/ketsch.html'

# MAXIMAL CAPACITY
MAX_CAPACITY_KA_PREMIUM = 0
MAX_CAPACITY_KA_LIFESTYLE = 0
MAX_CAPACITY_FRANKENTHAL = 0
MAX_CAPACITY_KETSCH = 0


# TIME / DATE
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TIME = datetime.datetime.now().strftime("%H:%M")


def get_free_spots_from_url(url, filename, capacity):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    spots_html_element = soup.findAll('strong', text = re.compile('Plätze'))[0]

    free_spots = ''.join(filter(lambda x: x.isdigit(), str(spots_html_element)))
    visitors = capacity - int(free_spots)
    

    if(TIME =='00:00'):
        column_title = "date;visitors;capacity\n"
        write_visitors_to_file(column_title, filename)
    
    output = str(TIMESTAMP) + ";" + str(visitors) + ";" + str(capacity) +"\n"

    write_visitors_to_file(output, filename)


def write_visitors_to_file(result, filename):
    with open(PATH + filename + '_' + DATE + '.csv', "a") as myfile:
        myfile.write(result)


def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(A=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code') 

get_free_spots_from_url(URL_KA_PREMIUM, KA_PREMIUM, MAX_CAPACITY_KA_PREMIUM)
get_free_spots_from_url(URL_KA_LIFESTYLE, KA_LIFESTYLE, MAX_CAPACITY_KA_LIFESTYLE)
get_free_spots_from_url(URL_FRANKENTHAL, FRANKENTHAL, MAX_CAPACITY_FRANKENTHAL)
get_free_spots_from_url(URL_KETSCH, KETSCH, MAX_CAPACITY_KETSCH)



if TIME == '00:00' or TIME == '12:00':
    git_push()
