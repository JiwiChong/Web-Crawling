import requests
from urllib import *
import os
from io import BytesIO
from bs4 import BeautifulSoup
import argparse
from b4_utils import main_url_extraction, category_html_link_extraction, category_model_php_extraction, category_datafile_extraction

# Command: 
# python b4_crawler.py --category 'animal' --save_dir /home/jiwi/Documents/Web_Crawling/crawled_data/b4/

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser to extract Open3DModels')
    parser.add_argument('--start_url', type=str, default='https://open3dmodel.com/3d-models/', help='The main URL of Open3DModel')
    parser.add_argument('--category', type=str, help='category of model you want to crawl')
    parser.add_argument('--save_dir', type=str, help='Directory to which you want to save the crawled data files')
    args = parser.parse_args()

    dir_to_make = os.path.join(args.save_dir, args.category)

    try:
        os.makedirs(dir_to_make)
    except FileExistsError:
        pass

    response = requests.get(args.start_url)
    soup = BeautifulSoup(response.content, "html.parser")


    soup_one = soup.select("a[href]")[3]
    sub_url_one = soup_one['href']

    sub_urls_items = [soup.select("a[href]")[i]['href'] for i in range(len(soup.select("a[href]")))]

    categories = ['architecture', 'interior', 'furniture','animal', 'character','electronic','nature','plant','aircraft','vehicle','weapon','anatomy','food','sport','misc']

    sub_soup = main_url_extraction(sub_urls_items, categories, args)
    category_links = category_html_link_extraction(sub_soup)
    category_phps = category_model_php_extraction(category_links)
    
    category_datafile_extraction(category_phps, dir_to_make)