from requests_html import HTMLSession
from bs4 import BeautifulSoup


s = HTMLSession()

url = 'https://www.amazon.com/s?k=electronics&qid=1632069494&ref=sr_pg_1'


# Extractor method
def extractor(url):
    s = HTMLSession()

    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')

    dataframe = []
    container_div = soup.find_all(
        'div', class_='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20')

    for item in container_div:
        try:

            product_image = item.find('img', class_='s-image').attrs['src']
        except:
            ""
        try:
            product_name = item.find(
                'a', class_='a-link-normal a-text-normal').span.text.strip()
        except:
            ""
        try:
            stars = item.find(
                'span', class_='a-icon-alt').text
        except:
            ""
        try:
            votes = item.find(
                'div', class_='a-row a-size-small').find(
                'span', class_='a-size-base').text
        except:

            ""
        try:
            current_price = item.find(
                'span', class_='a-offscreen').text
        except:
            ""

        try:
            old_price = ""
            price = item.find(
                'span', class_='a-price-whole').text

            fraction = item.find(
                'span', class_='a-price-fraction').text
            old_price += "$" + price + fraction
        except:
            ""

        product = {
            'product_name': product_name,
            'product_image_link': product_image,
            'product_rating': stars,
            'product_votes': votes,
            'product_price': current_price,
            'product_old_price': old_price,
        }
        dataframe.append(product)

    print(dataframe)

# Url Generator  method


def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

# Url Generator  method


def getnextpage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.com/' + \
            str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return


url_keep = []
while True:
    data = getdata(url)
    url = getnextpage(data)
    if not url:
        break
    url_keep.append(url)

print("Extracting data from all pages...")
for url in url_keep:
    extractor(url)
