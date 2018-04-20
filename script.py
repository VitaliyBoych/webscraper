# coding=utf-8
import requests
import time
from threading import Thread
from queue import Queue
from lxml import html, etree
import dicttoxml
import json
from io import BytesIO
import sys
import csv
import json

domain_file = 'result_links.txt'
theard_count = 5
out = []
q = open('Result.csv', 'w', encoding='utf8')
wr = csv.writer(q, delimiter=',', lineterminator='\n')
data = {}
data['results'] = []
w = open('black.txt', 'w')

def scrape(host):

    spec = []
    d = {}
    r = requests.get(host)
    tree = html.fromstring(r.text)
    tr = tree.xpath("//div[@class='col-xs-12 col-sm-6']//tr[./td]")
    name = tree.xpath("//h1[@class='product-name margin-top-md']/text()")[1].strip()
    try:
        name = tree.xpath("//h1[@class='product-name margin-top-md']/text()")[1].strip()
    except:
        pass
    try:
        top_category = tree.xpath("//ol[@class='breadcrumb categorycrumb padding-x-off pull-left hidden-print hidden-xs']/li/div/a/span/text()")[1].replace('›', '').strip()
    except:
        top_category = ''
    try:
        category = tree.xpath("//ol[@class='breadcrumb categorycrumb padding-x-off pull-left hidden-print hidden-xs']/li/div/a/span/text()")[2].replace('›', '').strip()
    except:
        category = ''
    try:
        sub_category = tree.xpath("//ol[@class='breadcrumb categorycrumb padding-x-off pull-left hidden-print hidden-xs']/li/div/a/span/text()")[3].replace('›', '').strip()
    except:
        sub_category = ''
    try:
        sub_sub_category = tree.xpath("//ol[@class='breadcrumb categorycrumb padding-x-off pull-left hidden-print hidden-xs']/li/div/a/span/text()")[4].replace('›', '').strip()
    except:
        sub_sub_category = ''
    try:
        images_all = ','.join(tree.xpath("//div[@class='slider']/div/@style")).replace('background-image: url(//', '').replace('); background-repeat: no-repeat', '').replace('60/50', '960/720')
    except:
        images_all = ''
    try:
        description = tree.xpath("//div[@id='description']")[0].text_content().strip().replace('\r','').replace('\n','').replace('                            ','').replace('Produktinformation','')
    except:
        description = ''
    try:
        price = tree.xpath("//span[@class='price']/text()")[0].strip()
    except:
        pass
    try:
        product_id = tree.xpath("//ul[@class='list-inline h4 product-identifiers']/li/text()")[1].strip()
    except:
        pass
    try:
        manufacter = tree.xpath("//ul[@class='list-inline h4 product-identifiers']/li/text()")[3].strip()
    except:
        pass
    try:
        manufacter_no = tree.xpath("//ul[@class='list-inline h4 product-identifiers']/li/text()")[5].strip()
    except:
        pass
    try:
        product_details = tree.xpath("//div[@id='eolOriginal']/h4/text()")[0].strip()
    except:
        product_details = ''
    try:
        for t in tr:
            key = t.xpath("./td[@width='50%']/text()")[0]
            value = t.xpath("./td[not(@width)]/text()")[0]
            d[key] = value
    except:
        d = ''
    data['results'].append({
        'name': name,
        'spec': d,
        'description': description,
        'top_category': top_category,
        'category': category,
        'sub_category': sub_category,
        'product_id': product_id,
        'manufacter_number': manufacter_no,
        'manufacter': manufacter,
        'images': images_all,
        'price': price,
        'url': host})
    print(name)
    with open('dustin_fi.txt', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile)



def check_url(host):
    try:
        scrape(host)
    except Exception as ex:
        w.write(host + '\n')
        print(ex)


def run(queue):
    while not queue.empty():
        host = queue.get_nowait()
        check_url(host)
        queue.task_done()


def main(domain_file):
    start_time = time.time()
    queue = Queue()
    with open(domain_file) as f:
        for line in f:
            queue.put(line.strip())
    for i in range(theard_count):
        thread = Thread(target=run, args=(queue,))
        thread.daemon = True
        thread.start()
    queue.join()
    print(time.time() - start_time)


main(domain_file)
