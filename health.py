import requests
import json
import csv
from lxml import html
import concurrent.futures
import time
import os
import sys


res_p = []
res_l = []
res_p_2 = []
res_d = []
res_p_3 = []
for_l = []

def scrape_url():
    speciality = open('.txt').read().split('\n')
    state = open('.txt').read().split('\n')
    w = open('.csv', 'w', encoding='utf8', newline='')
    wr = csv.writer(w, delimiter=',')
    for s in state:
        for spec in speciality:
            print('Scraping_...please wait, at now ' + str(spec))
            for i in range(1, 2):
                main_url = 'https://www./usearch?what=' + spec + '&where='+ s +'&pt=40.71455%2C%20-74.007118&pageNum=1&city=' + s +'&source=Solr'
                try:
                    r = requests.get(main_url, timeout=5)
                except:
                    try:
                        r = requests.get(main_url, timeout=5)
                    except:
                        try:
                            r = requests.get(main_url, timeout=5)
                        except:
                                r = requests.get(main_url, timeout=5)
                tree = html.fromstring(r.text)
                req_ses = tree.xpath("//script")[12].text
                sessino_id = req_ses.split('"')[15]
                request_id = req_ses.split('"')[-18]
                numbers = req_ses.split('=')[-4].replace('&pageNum','').replace('+','%20')
                url = 'https://www./usearch?userLocalTime=16%3A47&what=' + spec + '&searchType=&spec=null&where=' + s + '&pt=' + numbers +'&sort.provider=bestmatch&category=provider&sessionId=' + str(sessino_id) +'&requestId=' + str(request_id) + '&pageSize.provider=500&pageNum='+ str(i) +'&isFirstRequest=true&debug=false&isAtlas=false'
                try:
                    req = requests.get(url, timeout=5)
                except:
                    try:
                        req = requests.get(url, timeout=5)
                    except:
                        try:
                            req = requests.get(url, timeout=5)
                        except:
                            req = requests.get(main_url, timeout=5)
                root = json.loads(req.text)
                for g in range(1, 500):
                    try:
                        heh = '' + root['search']['searchResults']['provider']['results'][int(g)]['providerUrl']
                        wr.writerow([heh])
                    except:
                        pass

def clear_urls():
    file_p = open('.csv', 'w')
    with open('.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            name = row[0]
            if name not in for_links:
                for_links.append(name)
                file_p.write(';'.join(row) + '\n')
    print('>Unique url<')
    os.remove('.csv')


scrape_url()
clear_urls()


st_code = open('.txt').read()
domain_file = '.csv'
URLS = [url.strip() for url in open(domain_file)]
pract = open('.csv', 'w', encoding='utf8', newline='')
pr = csv.writer(pract, delimiter=',')
locat = open('.csv', 'w', encoding='utf8', newline='')
l_i = csv.writer(locat, delimiter=',')
doct = open('.csv', 'w', encoding='utf8', newline='')
doc_id = csv.writer(doct, delimiter=',')

def load_url(url):
    r = requests.get(url, timeout=3)
    tree = html.fromstring(r.text)
    try:
        dr = tree.xpath("//img/@alt")[0].split('.')[0]
    except:
        dr = ''
    if str(dr) != 'Dr':
        dr = ''
    n = tree.xpath("//img/@alt")[0].replace('Dr. ', '').split(',')[0]
    print(url)
    full_n = tree.xpath("//img/@alt")[0]
    tit = tree.xpath("//img/@alt")[0].split(',')[-1]
    gen = tree.xpath("//span[@data-qa-target='ProviderDisplayGender']/text()")[0]
    lan = '@@' + '@@'.join(tree.xpath('//section[@data-qa-target="learn-languages-section"]/div[@class="subsection-info-list is-mobile-toggle"]/div[@class="subsection-details no-read-more"]/ul//li/text()'))
    tre = tree.xpath("//ul[@id='insurance-payor-list']/li")
    ins = ''
    for tr in tre:
        ins += '@@' + '@'.join(tr.xpath(".//div[contains(@class,'insurance')]/text()"))
    if str(ins) == '@@':
        ins = ''
    bre = tree.xpath("//section[@data-qa-target='learn-certifications-section']//li")
    board_s = ''
    for br in bre:
        board_s += '@@' + br.xpath(".//div[not(@class)]/text()")[0].replace('@@@@@','@@')
        board_s += '@' + '@'.join(br.xpath(".//div[@class='subsection-info-list-subtext']/text()")[:-1]).replace('@@@@@','@@')
    if str(board_s) == '@@':
        board_s = ''
    spe = '@@' + '@@'.join(tree.xpath('//section[@data-qa-target="learn-specialties-section"]/div/div/ul//li/text()')).replace('@@@@@','@@')
    if str(spe) == '@@':
        spe = ''
    try:
        cond = '@@' + '@@'.join(tree.xpath('//section[@data-qa-target="learn-conditions-section"]/div/div/ul//li/text()')).replace('@@@@@','@@')
    except:
        cond = ''
    if str(cond) == '@@':
        cond = ''
    try:
        pro1 = '@@' + '@@'.join(tree.xpath('//section[@data-qa-target="learn-procedures-section"]/div/div/ul/li/a/text()')) + '@@'
    except:
        pro1 = '@@'
    try:
        pro2 = '@@'.join(tree.xpath('//section[@data-qa-target="learn-procedures-section"]/div/div/ul/li/text()'))
    except:
        pro2 = ''
    pro = pro1 + pro2
    if str(pro) == '@@@@':
        pro = ''
    edu = ''
    ete = tree.xpath("//section[@data-qa-target='learn-education-section']//li")
    for et in ete:
        edu += '@@' + et.xpath(".//div[not(@class)]/text()")[0]
        edu += '@' + '@'.join(et.xpath(".//div[@class='subsection-info-list-subtext']/text()")).replace(' | ', '@')
    if str(edu) == '@@':
        edu = ''
    try:
        m = tree.xpath("//section[@data-qa-target='learn-background-section']/div/div/div/h5/span/text()")[0]
        s = tree.xpath("//section[@data-qa-target='learn-background-section']/div/div/div/h5/span/text()")[1]
        board_a = tree.xpath("//section[@data-qa-target='learn-background-section']/div/div/div/h5/span/text()")[2]
    except:
        m = '0'
        s = '0'
        board_a = '0'
    aw = '@@' + '@@'.join(tree.xpath('//section[@data-qa-target="learn-awards-section"]/div/div/ul/li/text()')).replace('@@@@', '@@').replace(', ', '@')
    if str(aw) == '@@':
        aw = ''
    med = ''
    mre = tree.xpath('//section[@data-qa-target="learn-awards-section"]/div/div[@class="subsection-details no-read-more"]')
    for tr in mre:
        media += '@@' + '@'.join(tr.xpath(".//ul/li/a/text()")).replace('\r\n', '@').replace(', ', '@')
    if str(media) == '@@':
        media = ''
    aw = aw.replace('@@@@', '@@')
    try:
        acc_c = tree.xpath("//div[@class='accepting-text']/text()")[0]
        if str(accepting_c) != '':
            acc_c = 'Yes'
    except:
        acc_c = ''
    tr = tree.xpath("//nav[@class='visiting-loa-cards']/ul/li")
    adress_d = '/ '.join(tree.xpath('//a[@data-qa-target="qa-practice-link"]//div[@itemprop="streetAddress"]/text()'))
    for t in tr:
        try:
             pr_n = t.xpath(".//div[@class='practice-name']/text()")[0].replace(';', ',')
        except:
            pr_n = '@@' + full_name
        add = t.xpath(".//div[@itemprop='Ad']/text()")[0]
        c = t.xpath(".//span[@itemprop='adsL']/text()")[0].strip().replace(', ','')
        s = t.xpath(".//span[@itemprop='aRen']/text()")[0]
        po = t.xpath(".//span[@itemprop='pC']/text()")[0]
        try:
            te = t.xpath(".//a[@class='hg-track new']/@href")[0].replace('tel:', '')
        except:
            te = ''
        try:
            a_n = t.xpath(".//div[@class='a-n']/text()")[0]
        except:
            a_n = ''
        p2 = ''
        try:
            f = t.xpath(".//span[@class='action-label numeric-label']/text()")[0].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        except:
            f = ''
        if str(state) != str(st_code):
            pass
        else:
            pr.writerow([])
            l_i.writerow([])
            doc_id.writerow([])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = {executor.submit(load_url, url): url for url in URLS}
    start = time.time()
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
    print(start - time.time())

def p_():
    file_p = open('.csv', 'w')
    with open('.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            name = row[1]
            if name not in res_p:
                res_p.append(name)
                file_p.write(';'.join(row) + '\n')
    print('Script is still working, pls wait...')
	
def l_():
    file_l = open('.csv', 'w')
    with open('.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            address = row[2]
            if address not in res_l:
                res_l.append(address)
                file_l.write(';'.join(row) + '\n')

def dr():
    file_p_3 = open('.csv', 'w')
    with open('.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            name = row[1]
            if name not in res_p_3:
                res_p_3.append(name)
                file_p_3.write(';'.join(row) + '\n')
def dn():
    doc = open('.csv').read().split('\n')
    res_loc = open('.csv', 'w')
    for l in doc:
        loc = l.split(';')[-1]
        if '/' not in str(loc):
            loc = ''
        res_loc.write(l + ';' + loc + '\n')

def d_():
    try:
        loa = open('.csv').read().split('\n')
        doa = open('.csv').read().split('\n')
        res_doc = open('.csv', 'w')
        for d in doa:
            pr_adress = d.split(';')[-2]
            i = 0
            for p in loa:
                if p.find(pr_adress) != -1:
                    break
                i += 1
            try:
                p_id = loa[i].split(';')[0]
                l_id = loa[i].split(';')[1]
                res_doc.write(d + ';' + p_id + ';' + l_id + '\n')
            except:
                pass
    except:
        pass
def doas_2():
    loa = open('.csv').read().split('\n')
    doa = open('.csv').read().split('\n')
    res_doc = open('.csv', 'w')
    for d in doa:
        pr_adress = d.split(';')[-3]
        i = 0
        for p in loa:
            if p.find(pr_adress) != -1:
                break
            i += 1
        try:
            p_id = loa[i].split(';')[0]
            l_id = loa[i].split(';')[1]
        except:
            p_id = ''
            l_id = ''
        res_doc.write(d + ';' + p_id + ';' + l_id + '\n')
def final():
    print('Almost done')
    try:
        j = 1
        fin_l = open('.csv', encoding='utf8').read().split('\n')
        fin_d = open('.csv', encoding='utf8').read().split('\n')
        res = open('.csv', 'w', encoding='utf8')
        for d in fin_d:
            adr = d.split(';')[-3]
            ids = d.split(';')[-1]
            if adr != '':
                ids = []
                for l in fin_l:
                    if adr == l.split(';')[-1]:
                        ids.append(l.split(';')[1])
                ids = ', '.join(ids)

            if ids == '':
               ids = d.split(';')[-1]
            g = d.split(';')
            g = ';'.join(g[:-1]) + ';' + ids
            res.write(str(j) + ';' + g + '\n')
            j+=1
    except:
        pass

def djson():
    f = open('', 'rU')
    reader = csv.DictReader(f, fieldnames=(), delimiter=';')
    out = json.dumps([row for row in reader])
    print("JSON parsed!")
    f = open('.json', 'w')
    f.write(out)
    print("JSON  saved!")

def ljson():
    f = open('.csv', 'rU')
    reader = csv.DictReader(f, fieldnames=(), delimiter=';')
    out = json.dumps([row for row in reader])
    print("JSON  parsed!")
    f = open('.json', 'w')
    f.write(out)
    print("JSON saved!")

def pjson():
    f = open('.csv', 'rU')
    reader = csv.DictReader(f, fieldnames=(), delimiter=';')
    out = json.dumps([row for row in reader])
    print("JSON  parsed!")
    f = open('.json', 'w')
    f.write(out)
    print("JSON  saved!")

print('>>>>FINISHED<<<<')