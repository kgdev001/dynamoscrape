import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
import json
import config2 as config2


# a list of dictionaries to hold the scraped data
news_catalog = []#{}

# Set up fake user-agent to avoid being blocked
def get_headers():
    ua = UserAgent()
    return {'User-Agent': ua.random}

# Fetch the web page content
def fetch_page_content(url):
    headers = get_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve content. Status code: {response.status_code}")
    
# Login to the portal

# handle request throttling

# Handle paggination

#iterate over each qrticle in the catalog to extract the required info
def catalog(catalog):
    article_ele_type = config2.article_element_type
    article_ele_class = config2.article_element_class
    title_ele_type = config2.title_element_type
    title_ele_class = config2.title_element_class
    posted_date_ele_type = config2.posted_date_element_type
    posted_date_ele_class = config2.posted_date_element_class
    link_ele_type = config2.article_link_element
    link_ele_class = config2.article_link_class
          
    for ix, article in enumerate(catalog.find_all(article_ele_type, class_=article_ele_class)):
        #define attributes to be captured

        title = article.find(title_ele_type, class_= title_ele_class).get_text().strip() # dynamic 

        posted_day = article.find(posted_date_ele_type, class_=posted_date_ele_class).get_text().strip() # dynamic 

        article_url = article.find(link_ele_type, class_= link_ele_class).get("href") # dynamic 
        
        news_catalog.append({"index":ix,"title": title, "url": article_url, "posted_day": posted_day})
        #news_catalog[ix] = {"index":ix,"title": title, "url": article_url, "posted_day": posted_day}

    return news_catalog

# Parse HTML and extract the iterable from the landing page
def parse_article_data(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    # find the article parent through a parameterised input. The parameter will tell which element to iterated over
    
    # dynamic
    parent_ele_type = config2.parent_element_type
    parent_ele_class = config2.parent_element_class
    parent_ele_id = config2.parent_element_id

    #parent_element = {"element_type":"div", "element_calss":"epn_result_list epn_4_column"}
    all_articles_element = soup.find(parent_ele_type, class_= parent_ele_class, id = parent_ele_id )
    
    # Call function to extract data from catalog
    article_listing = catalog(all_articles_element)
    #return catalog(all_articles_element)
    return article_listing

# Dump to CSV
def write_to_csv (data):
    filename = config2.output_file_name
    with open(filename, 'w', newline='') as csv_file:
        # Create a writer object
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
    
        # Write the header
        writer.writeheader()
    
        # Write the rows
        writer.writerows(data)

    print(f'Data has been written to {filename}')

source_url = config2.url

content = fetch_page_content(config2.url) #dynamic

article_catalog = parse_article_data (content)

write_to_csv (article_catalog)

### Step 1: Get the raw HTML
### Step 2: Parse it
### Step 3: Based on the configuration, get the data and store it in a JSON
###     This will involve iterating over list of article, going inside the articles, login, captcha maybe  
###step 3.1: First capture the landing page data with url - Done
### step 4: Go inside each url where bot needs to go and append the extracted data to the original data

###This script does not handle pagination, login, inner content, error handling, retry logic, data cleaning, keyword matching

'''
Things to make dynamic:
- Base url of the source
- where to find the article title
- where to find the article author
- where to find the inner content
- pagination
    - Through url query strings
    - Dynamic rendering
    - Infinite scrolling
- login
'''
