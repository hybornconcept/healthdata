from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery
import os

# s = HTMLSession()
url = 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_unv_e_1_172665_4'
mainlist = []
big_data = []
# credentials_path = 'C:\Users\DELL PRECISION 5520\Documents\Helloworld\SELENIUM\Electronics\project-1-325909-ee6de54dff76.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
# table_id = 'project-1-325909.Market_Research.Category'
# client = bigquery.Client()

gsg = 'https://www.amazon.com/Best-Sellers-Electronics-3D-Viewing-Glasses/zgbs/electronics/3224438011/ref=zg_bs_nav_e_3_172532'


def extractor(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    container = soup.find('ul', id='zg_browseRoot')

    for lis in container.find_all('li')[2:]:

        product_name = lis.get_text()
        for a in lis.find_all('a', href=True):
            product_link = a['href']
            # list2.append(product_link)

            lister = {
                'product_name': product_name,
                'product_link': product_link,
            }
            mainlist.append(lister)
    return mainlist


catName, level1, level2, level3, level4 = ([] for i in range(5))
counter = 0
catName = extractor(url)

for item_cat in catName:
    # print(item_cat['product_name'], " ", item_cat['product_link'])
    category_name = item_cat['product_name']
    level1 = extractor(item_cat['product_link'])
    for item1 in level1:
        # print(item1['product_name'], " ", item1['product_link'])
        level1_name = item1['product_name']
        level2 = extractor(item1['product_link'])
        for item2 in level2:
            #  print(item2['product_name'], " ", item2['product_link'])
            level2_name = item2['product_name']
            level3 = extractor(item2['product_link'])
            for item3 in level3:
                n = 5
                # print(item3['product_name'], " ", item3['product_link'])
                while n > 0:
                    level3_name = item3['product_name']
                    level4 = extractor(item3['product_link'])
                    for item4 in level4:
                        if item4['product_link'] == gsg:
                            print('Element found')
                            break
                        else:
                         # print(item4['product_name'], " ", item4['product_link'])
                            level4_name = item4['product_name']
                            level4_link = item4['product_link']
                            level4_Id = (
                                [int(s) for s in level4_link.split("/") if s.isdigit()][0])
                            level_number = (
                                [s for s in level4_link.split("_")][-2])
                            # level4 = extractor(item3['product_link'])
                            collator = {
                                'CatID': level4_Id,
                                'CatName': category_name,
                                'CatLevel1': level1_name,
                                'CatLevel2': level2_name,
                                'CatLevel3': level3_name,
                                'CatLevel4': level4_name,
                                'Level': level_number,
                                'CatUrl': level4_link,
                            }
                            print(collator)
                            big_data.append(collator)


# num = "https://www.amazon.com/Best-Sellers-Electronics-Photo-Printers-Scanners/zgbs/electronics/499328/ref=zg_bs_nav_e_2_502394/145-5257390-0013855"
# print([int(s) for s in num.split("/") if s.isdigit()][0])
