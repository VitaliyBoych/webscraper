from selenium import webdriver
import time
import csv
import json
import requests
import concurrent.futures
import logging
from selenium.webdriver.chrome.options import Options


timestr = time.strftime("%Y.%m.%d--%H.%M.%S")
w = open('Result-' + timestr + '.csv', 'w', encoding='utf8', newline='')
wr = csv.writer(w, delimiter=',')
wr.writerow(['PID', 'Product title', 'Brand', 'Unit Price', 'Quantity', 'Price', 'Price Before Discount', 'Measuring Unit', 'Category', 'Type', 'Description', 'URL', 'Image'])
LOG_FILENAME = 'Log-' + timestr + '.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def download(url):
    r = requests.get(url)
    filename = url.split('/')[-1]
    with open('imgs/{}'.format(filename), 'wb') as q:
        q.write(r.content)
    print(filename, 'downloaded....')
    return filename


def load_url(u):
    urle = u.split(',')[0]
    category = u.split(',')[1]
    product_url = u.split(',')[2]
    r = requests.get(urle)
    root = json.loads(r.text)
    try:
        product_title = root['Product']['Description'].replace('<br>', '').strip()
    except:
        product_title = ''
    try:
        price = root['Product']['Price']
    except:
        price = ''
    try:
        price_before_discount = root['Product']['WasPrice']
    except:
        price_before_discount = ''
    try:
        unit_price = root['Product']['CupString'].replace('0.00 / 0', '').replace('$', '')
        measuring_unit = root['Product']['CupMeasure']
    except:
        unit_price = ''
        measuring_unit = ''
    descr = root['Product']['RichDescription']
    try:
        description = 'Product Details: ' + descr.replace('</br>', '').replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('<i>', '').replace('</i>', '').replace('</strong>', '')
    except:
        description = ''
    try:
        ingred = 'Ingredients: ' + root['AdditionalAttributes']['ingredients']
    except:
        ingred = ''
    description = description + ' / ' + ingred
    if descr == '':
        description = ingred
    elif descr == 'null':
        description = ingred
    elif ingred == 'null':
        description = description.replace(' / ', '').replace('null', '').replace('/', '')
    elif ingred == '':
        description = description.replace(' / ', '').replace('null', '').replace('/', '')
    tags = root['AdditionalAttributes']['piessubcategorynamesjson'].split('"')[-2]
    src = root['DetailsImagePaths'][0]
    filename = download(src)
    pid = filename.replace('.jpg', '').replace('.tif', '').replace('_1','')
    if int(price) == int(price_before_discount):
        price_before_discount = root['Product']['CentreTag']['TagContent']
        if str(price_before_discount) == 'null':
            price_before_discount = ''
        else:
            try:
                price_before_discount = price_before_discount.replace('00"','00').split('"')[-2]
            except:
                pass
    if '.' not in str(price_before_discount):
        price_before_discount = ''
    elif str(measuring_unit) == '0':
        measuring_unit = ''
    brand = ''
    quantity = ''
    wr.writerow([pid, product_title, brand, unit_price, quantity, price, price_before_discount, measuring_unit, category, tags, description, product_url, filename])
    print(price_before_discount, len(price_before_discount))


domain_file = 'url.txt'
URLS = [url.strip() for url in open(domain_file)]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = {executor.submit(load_url, url): url for url in URLS}
    start = time.time()
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
    print(start - time.time())



