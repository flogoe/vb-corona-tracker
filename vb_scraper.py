#!/usr/bin/env python3

import requests
import re
import string
import datetime
from bs4 import BeautifulSoup

# PATH and FILENAMES
PATH = '/home/flg/vb_scraper/data/'
KA_PREMIUM = "vb_data_ka_premium.txt"
KA_LIFESTYLE = "vb_data_ka_lifestyle.txt"
FRANKENTHAL = "vb_data_frankenthal.txt"

# URLS 
URL_KA_PREMIUM = 'https://www.venicebeach-fitness.de/clubs/premium-fitness/karlsruhe-postgalerie/'
URL_KA_LIFESTYLE = 'https://www.venicebeach-fitness.de/clubs/lifestyle-fitness-plus/karlsruhe/'
URL_FRANKENTHAL = 'https://www.venicebeach-fitness.de/clubs/lifestyle-fitness-plus/frankenthal.html'

def get_free_spots_from_url(url, filename):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    spots_html_element = soup.findAll('strong', text = re.compile('Plätze'))[0]

    free_spots = ''.join(filter(lambda x: x.isdigit(), str(spots_html_element)))
    timestamp = datetime.datetime.now()

    output = str(timestamp) + " | " + free_spots + ";\n"

    write_free_spots_to_file(output, filename)



def write_free_spots_to_file(result, filename):
    with open(PATH + filename, "a") as myfile:
        myfile.write(result)

get_free_spots_from_url(URL_KA_PREMIUM, KA_PREMIUM)
get_free_spots_from_url(URL_KA_LIFESTYLE, KA_LIFESTYLE)
get_free_spots_from_url(URL_FRANKENTHAL, FRANKENTHAL)
