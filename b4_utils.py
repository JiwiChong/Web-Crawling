import requests
from urllib import *
import os
import re
import zipfile
from io import BytesIO
from bs4 import BeautifulSoup
from tqdm import tqdm


def main_url_extraction(sub_urls_items, categories, args):
    filtered_category_urls = []
    for url in sub_urls_items:
        for cat in categories:
            latter_url_part = url.split('/')[-1]
            if cat == latter_url_part:
                filtered_category_urls.append(url)

    dirname = os.path.dirname(filtered_category_urls[0])
    sub_response = requests.get(os.path.join(dirname, args.category)).text   # one category
    sub_soup = BeautifulSoup(sub_response, "html.parser")
    return sub_soup


def category_html_link_extraction(sub_soup):
    category_links = []
    for link in sub_soup.find_all('a',
                            attrs={'href': re.compile("^https://")}):
        # display the actual urls
        link_ = link.get('href')
        if link_.endswith('.html'):
            category_links.append(link_)
    category_links_ = list(set(category_links))
    return category_links_


def category_model_php_extraction(category_links_list):
    cat_phps = []
    for i in tqdm(range(len(category_links_list))):
        response = requests.get(category_links_list[i]).text
        soup_one = BeautifulSoup(response, "html.parser")
        cat_links = []
        for link in soup_one.find_all('a',
                                attrs={'href': re.compile("^https://")}):

            link_ = link.get('href')
            if '.php' in link_:
                cat_links.append(link_)
        cat_phps.append(cat_links[0])
    
    return cat_phps


def category_datafile_extraction(category_phps, dir_to_make):
    token_dict = {}
    for php in tqdm(category_phps):
        mini_response = requests.get(php)
        mini_soup = BeautifulSoup(mini_response.text, 'html.parser')
        mini_links = mini_soup.find_all('a')
        l_ = [mini_links[i]['href'] for i in range(len(mini_links))]

        res = [x for x in l_ if '?token_id' in x]
        http = l_[0]
        token_address = http + res[0]
        mini_response = requests.get(token_address)
        # print(mini_response)
        try:
            mini_zipfile= zipfile.ZipFile(BytesIO(mini_response.content))
            mini_zipfile.extractall(os.path.join(dir_to_make + '/'))
        except Exception as e:
            print(str(e))
            continue