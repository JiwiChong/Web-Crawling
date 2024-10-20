# Web-Crawling

Web Crawling is a technique used to scrape essential or targeted information from certain websites 
that would be used for research work or other objectives. In this repository, web crawling tools 
that extract 3D models for 3D Computer Vision research works, are provided. 
The tools used in this repository are Selenium and BeautifulSoup. The website from which the
3D models are extracted from is: https://open3dmodel.com/

![img1](https://github.com/user-attachments/assets/180c76e1-c693-4a9c-84ac-fa268c666d4c)

The website is severely plagued with Ads that pop from several sides of the site and this can
be very disturbing to download the models manually. Hence, it is convenient to utilize the web crawling
method to extract the models automatically given the category of the model one desires to get.
The categories are not limited to "Vehicle", "Architecture", "Weaponds", etc. 



# Commands
### For Web Crawling using Selenium:<br />
python selenium_crawler.py --category (category of object of interest) --save_dir (directory where to save models)

### For Web Crawling using BeautifulSoup:<br />
python b4_crawler.py --category (category of object of interest) --save_dir (directory where to save models)
