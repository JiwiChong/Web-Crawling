from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import zipfile
from io import BytesIO
import argparse
from tqdm import tqdm
import os

#Command:
# python selenium_crawler.py --category 'architecture' --save_dir /home/jiwi/Documents/Web_Crawling/crawled_data/selenium/


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser to extract Open3DModels')
    parser.add_argument('--start_url', type=str, default='https://open3dmodel.com/3d-models/', help='The main URL of Open3DModel')
    parser.add_argument('--category', type=str, help='category of model you want to crawl')
    parser.add_argument('--save_dir', type=str, help='Directory to which you want to save the crawled data files')
    args = parser.parse_args()

    driver = webdriver.Chrome()
    # Navigate to the webpage
    driver.get(args.start_url)
    bodies = driver.find_elements(By.XPATH, "/html/body/div/div[2]/div/ul/li/a")
    category_links = [bodies[i].get_attribute('href') for i in range(len(bodies))]
    category_dict = {os.path.basename(link):i for i, link in enumerate(category_links)}

    dir_to_make = os.path.join(args.save_dir, os.path.basename(category_links[category_dict[args.category]]))

    try:
        os.makedirs(dir_to_make)
    except FileExistsError:
        pass

    driver.get(category_links[category_dict[args.category]])

    # length of 42 
    category_one_sites = driver.find_elements(By.CSS_SELECTOR, '[id*="%s"]' % 'site-')
    category_one_site_html = [category_one_sites[i].find_element(By.TAG_NAME, "a").get_attribute("href") for i in range(len(category_one_sites))]

    for html in tqdm(category_one_site_html):
        driver.get(html)
        cat_one_model_php = driver.find_elements(By.XPATH, "//div[@class='downloadlink']")[0].find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
        driver.get(cat_one_model_php)

        cat_one_model_one_token = driver.find_elements(By.XPATH, "/html/body/div[3]/div[7]/div/div/div[6]/a")
        cat_one_model_one_token_addr = cat_one_model_one_token[0].get_attribute('href')
        mini_response = requests.get(cat_one_model_one_token_addr)
        # print(mini_response)
        try:
            mini_zipfile= zipfile.ZipFile(BytesIO(mini_response.content))
            mini_zipfile.extractall(dir_to_make+'/')
        except Exception as e:
            print(str(e))
            continue