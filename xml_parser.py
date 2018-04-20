import requests
from lxml import etree, html
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time


all_urls = ['',
            '',
            '',
            '']
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('')
pr = sh.get_worksheet(0)
ser = sh.get_worksheet(1)


def parse_pr_fin(urls):
    dates = list(filter(None, pr.col_values(4)[6:]))
    start = 7 + len(dates)
    for url in urls:
        req = requests.get(url)
        fin_tree = etree.fromstring(req.content)
        fin_title = fin_tree.xpath("//headline/text()")[0]
        fin_date = fin_tree.xpath("//published/@date")[0].split()[0]
        info_tree = html.fromstring(fin_tree.xpath("//main/text()")[0])
        fin_info = '\n'.join(info_tree.xpath("//text()"))
        if fin_date not in dates:
            cell_list = [pr.acell('B{}'.format(start)), pr.acell('D{}'.format(start)), pr.acell('F{}'.format(start))]
            out = [fin_title, fin_date, fin_info]
            for c, o in zip(cell_list, out):
                c.value = o
            pr.update_cells(cell_list)
            start += 1


def parse_pr_en(urls):
    dates = list(filter(None, pr.col_values(4)[6:]))
    start = 7 + len(dates)
    for url in urls:
        req = requests.get(url)
        en_tree = etree.fromstring(req.content)
        en_title = en_tree.xpath("//headline/text()")[0]
        en_date = en_tree.xpath("//published/@date")[0].split()[0]
        info_tree = html.fromstring(en_tree.xpath("//main/text()")[0])
        en_info = '\n'.join(info_tree.xpath("//text()"))
        out = [en_title, en_date, en_info]
        if en_date in dates:
            index = 7 + dates.index(en_date)
            check = pr.acell('A{}'.format(index)).value
            if check == '':
                cell_list = [pr.acell('A{}'.format(index)), pr.acell('C{}'.format(index)),
                             pr.acell('E{}'.format(index))]
                for c, o in zip(cell_list, out):
                    c.value = o
                pr.update_cells(cell_list)
        else:
            cell_list = [pr.acell('A{}'.format(start)), pr.acell('C{}'.format(start)), pr.acell('E{}'.format(start))]
            start += 1
            for c, o in zip(cell_list, out):
                c.value = o
            pr.update_cells(cell_list)


def parse_ser_fin(urls):
    dates = list(filter(None, ser.col_values(4)[6:]))
    start = 7 + len(dates)
    for url in urls:
        req = requests.get(url)
        fin_tree = etree.fromstring(req.content)
        fin_title = fin_tree.xpath("//headline/text()")[0]
        fin_date = fin_tree.xpath("//published/@date")[0].split()[0]
        info_tree = html.fromstring(fin_tree.xpath("//main/text()")[0])
        fin_info = '\n'.join(info_tree.xpath("//text()"))
        if fin_date not in dates:
            cell_list = [ser.acell('B{}'.format(start)), ser.acell('D{}'.format(start)), ser.acell('F{}'.format(start))]
            start += 1
            out = [fin_title, fin_date, fin_info]
            for c, o in zip(cell_list, out):
                c.value = o
            ser.update_cells(cell_list)


def parse_ser_en(urls):
    dates = list(filter(None, ser.col_values(4)[6:]))
    start = 7 + len(dates)
    for url in urls:
        req = requests.get(url)
        en_tree = etree.fromstring(req.content)
        en_title = en_tree.xpath("//headline/text()")[0]
        en_date = en_tree.xpath("//published/@date")[0].split()[0]
        info_tree = html.fromstring(en_tree.xpath("//main/text()")[0])
        en_info = '\n'.join(info_tree.xpath("//text()"))
        out = [en_title, en_date, en_info]
        if en_date in dates:
            index = 7 + dates.index(en_date)
            check = ser.acell('A{}'.format(index)).value
            if check == '':
                cell_list = [ser.acell('A{}'.format(index)), ser.acell('C{}'.format(index)),
                             ser.acell('E{}'.format(index))]
                for c, o in zip(cell_list, out):
                    c.value = o
                ser.update_cells(cell_list)
        else:
            cell_list = [ser.acell('A{}'.format(start)), ser.acell('C{}'.format(start)), ser.acell('E{}'.format(start))]
            start += 1
            for c, o in zip(cell_list, out):
                c.value = o
            ser.update_cells(cell_list)


def parse(url):
    r = requests.get(url)
    tree = etree.fromstring(r.content)
    urls = tree.xpath("//guid/text()")
    if url.find('_pr') != -1:
        if url.find('_5_') != -1:
            parse_pr_en(urls)
        else:
            parse_pr_fin(urls)
    else:
        if url.find('_5_') != -1:
            parse_ser_en(urls)
        else:
            parse_ser_fin(urls)


def main():
    for a in all_urls:
        parse(a)


schedule.every(15).minutes.do(main)


while True:
    schedule.run_pending()
    time.sleep(1)


