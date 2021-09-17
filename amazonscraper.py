from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


mainlist = []

# instantiating the selenium class
browser = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe')
browser.maximize_window()
url = 'https://www.amazon.com/s?k=electronics&i=electronics-intl-ship&crid=387MZ2MH7S1C0&qid=1631770642&sprefix=elec%2Celectronics-accessories%2C382&ref=sr_pg_1'


# function to modify the url
def extractor(url):
    browser.get(url)

    browser.implicitly_wait(10)
    # Dycrypting the response --VERY IMPORTANT
    content = browser.page_source.encode('utf-8').strip()

    soup = BeautifulSoup(content, "html.parser")
    return soup


def load():
    df = pd.DataFrame(mainlist)
    df.to_csv("Amazon_Electronics.csv", index=False)


def transformer(soup):

    wrapper = soup.find_all(
        'div', {'class': 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'})

    for wraps in wrapper:
        # finding divs with product names
        divs = wraps.find_all(
            'div', {'class': 'a-section a-spacing-none a-spacing-top-small'})
    # looping through  to get h2 in divs with product names
        for header in divs:
            # get all the h2 tags in items
            h2 = header.find_all(
                'h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})

            # get all the spans that contain the name of the product in h2 tags
            for spanNames in h2:
                product = spanNames.find(
                    'span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
                Amazondata = {}
                Amazondata["product_Name"] = product

    # looping through  divs to get spans  that contain stars and rating
        for item in wrapper:
            try:
                stars = item.find('span', {'class': 'a-icon-alt'}).text
            except:
                stars = " "

            try:
                rates = item.find('span', {'class': 'a-size-base'}).text
            except:
                rates = " "
            Amazondata["stars"] = stars
            Amazondata["rating"] = rates
            # Getting  pricing
            items = soup.find_all(
                'div', {'class': 'a-row a-size-base a-color-base'})
        for item in items:
            a_tag = item.find_all(
                'a', {'class': 'a-size-base a-link-normal a-text-normal'})
            for span in a_tag:
                a = span.find('span', {'class': 'a-price'})
                try:
                    price = a.find('span', {'class': 'a-offscreen'}).text
                except:
                    price = " "
                b = span.find('span', {'class': 'a-price a-text-price'})
                try:
                    old_price = b.find('span', {'class': 'a-offscreen'}).text
                except:
                    old_price = " "
                Amazondata["price"] = price
                Amazondata["old_price"] = old_price
        mainlist.append(Amazondata)
    return mainlist


def getPagination(soup):
    pager = soup.find('ul', {'class': 'a-pagination'})
    if not pager.find('ul', {'class': 'a-disabled a-last'}):
        url = "https://www.amazon.com/" + \
            str(pager.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return


wrapper = extractor(
    'https://www.amazon.com/s?k=electronics&i=electronics-intl-ship&page=2&qid=1631836588&ref=sr_pg_2')
transformer(wrapper)
load()
print("Loading to csv...")
# print(mainlist)


browser.quit()
