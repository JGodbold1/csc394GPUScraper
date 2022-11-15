import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# this file was authored by Dave P.


def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    # add term query to url
    url = template.format(search_term)

    # add page query placeholder
    url += '&page={}'

    return url


def extract_record(item):
    """ Extract and return data from single record"""

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    # price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    # Review and rating
    try:
        rating = item.i.text
        review_count = item.find('span', {
                                 'class': 'a-size-base puis-light-weight-text s-link-centralized-style'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, price, rating, review_count, url)
    return result


def runSearch(search_term, path):
    """Run main program routine"""
    # URL: https://chromedriver.chromium.org/
    # Debug: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
    # options.binary_location = r"your\path\chrome"

    # Startup the chrome webdriver
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.page_load_strategy = 'normal'
    options.add_experimental_option(
        "excludeSwitches", ["ignore-certificate-errors"])
    service = Service(
        executable_path="C:/Users/Kyurre/AppData/Local/Programs/Python/Python310/chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)

    records = []
    url = get_url(search_term)
    #url = 'https://www.amazon.com/s?k=gpu&ref=nb_sb_noss_1'

    # Go through max of 20 pages on amazon and parse information
    for page in range(1, 10):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all(
            'div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:                                         # Only add to the list of a record of an item exists
                records.append(record)
    uniq_records = set(records)
    driver.close()

    # print(records)

   

    # save data to csv file
    try:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
            writer.writerows(uniq_records) #ls added unique record 11/15/2022
    except FileNotFoundError:
        print("Couldn't find file in specified path")


#runSearch('gpu', 'gpu.csv')
