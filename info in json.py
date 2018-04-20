import requests
from lxml import html, etree
import json
import dicttoxml
from io import BytesIO


def g(url):
    table = []
    ths = []
    data = {}
    url_id = url[url.rfind('/') + 1:]
    r = requests.get('https://www' + url_id)
    tree = html.fromstring(r.text)
    th = tree.xpath("//th")
    for t in th[:-1]:
        ths.append(t.text_content().strip())
    table.append(ths)
    tr = tree.xpath(".//*[@id='contractListTable']/tbody/tr")
    for t in tr[:-1]:
        td = t.xpath(".//td")
        tds = []
        for d in td:
            tds.append(' '.join(d.text_content().split()))
        table.append(tds)
    r = requests.get(url)
    tree = html.fromstring(r.text)
    name = tree.xpath("//div[@class='row']/div/h3/text()")[0].strip()
    info = {'status': tree.xpath("//span[@class='SPMarketStatus']/text()")[0].strip(),
            'Market Type': tree.xpath("//div[@class='row']/div[2]/p/a/text()")[0].strip(),
            'End Date': tree.xpath("//div[@class='row']/div[2]/p[2]/text()")[0].strip()}
    rules = tree.xpath("//div[@class='tab-c']/p/text()")[0].strip()
    dates = ['24H', '7D', '30D', '90D']
    for d in dates:
        r = requests.get(
            'https://www' + url_id + '&timespan=' + d)
        
        x = dicttoxml.dicttoxml(json.loads(r.text), attr_type=False)
        tree = etree.parse(BytesIO(x))
        var = []
        for item in tree.xpath("//item"):
            try:
                var.append({'ContractName': item.xpath(".//ContractName/text()")[0],
                            'Date': item.xpath(".//DateString/text()")[0],
                            'OpenSharePrice': item.xpath(".//OpenSharePrice/text()")[0],
                            'HighSharePrice': item.xpath(".//HighSharePrice/text()")[0],
                            'LowSharePrice': item.xpath(".//LowSharePrice/text()")[0],
                            'Volume': item.xpath(".//TradeVolume/text()")[0]})
            except:
                pass
        print(str(var))
        if d.find('24H') != -1:
            data.update({'24H': var})
        elif d.find('7D') != -1:
            data.update({'7D': var})
        elif d.find('30D') != -1:
            data.update({'30D': var})
        elif d.find('90D') != -1:
            data.update({'90D': var})
    output = {'Data': data}
    return output


urls = ['https://www']
for url in urls:
    g(url)
