import requests
import pymysql
import re
import time
import random
import math
from lxml import html as HTML
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
import unicodedata

sqlLock = threading.Lock()
UA = [
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; ARM; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.33 Safari/535.11',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
]

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": 'http-pro.abuyun.com',
    "port": '',
    "user": '',
    "pass": '',
}
proxies = {'https': proxyMeta,
           'http': proxyMeta, }

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.cellartracker.com',
    'Referer': 'https://www.cellartracker.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA),
}

# finewest
sql1 = pymysql.connect(
    host='',
    port=,
    user='',
    password='',
    db=''
)
cursor1 = sql1.cursor()

# finewest_test
sql2 = pymysql.connect(
    host='',
    port=,
    user='',
    password='',
    db=''
)
cursor2 = sql2.cursor()


def getRules():
    # 所有的
    goodsrules = "SELECT `id` FROM `shopping_goodsrules`"
    sqlLock.acquire()
    cursor1.execute(goodsrules)
    sqlLock.release()
    rules_list = cursor1.fetchall()
    rulesid = [str(i[0]) for i in rules_list]
    # 已查询的
    testrules = "SELECT `classNameId` FROM `crawl` WHERE `from`='CT' and type=1 group by `classNameId`"
    sqlLock.acquire()
    cursor2.execute(testrules)
    sqlLock.release()
    cellarlist = cursor2.fetchall()
    cellar = [str(i[0]) for i in cellarlist]
    # 未查询的
    idlist = [id for id in rulesid if id not in cellar]
    return idlist


def tryUrl(url):
    while True:
        try:
            response = requests.get(url=url, headers=header, proxies=proxies)  # verify=False,.content.decode('utf-8')
            if response.status_code == 200:
                html = HTML.fromstring(response.content.decode('utf-8'))
                return html
            else:
                time.sleep(random.uniform(1, 2))
                continue
        except:
            # print('\r\n   解析失败，重试中')
            continue


def changUni(unic):
    change = unicodedata.normalize('NFKD', unic).encode('ascii', 'ignore').strip()  # 转换法语
    code = str(change, encoding='utf-8')
    return code


def getmess(url, xpathtree):
    while True:
        html = tryUrl(url)
        mess = html.xpath(xpathtree)
        if len(mess) > 0:
            return html, mess
        else:
            continue


def crawl(id):
    goodsrules = "SELECT `className` FROM `shopping_goodsrules` where id =" + str(id)
    sqlLock.acquire()
    cursor1.execute(goodsrules)
    sqlLock.release()
    old_rule = cursor1.fetchall()[0][0].replace('\xa0', ' ').strip()
    print('\r\n查找:', id, old_rule)
    time.sleep(10)
    newrule = changUni(old_rule).replace("(", "").replace(")", "").replace("（", "").replace("）", "").strip()
    url = "https://www.cellartracker.com/list.asp?fInStock=0&iUserOverride=0&Table=List&szSearch=" + str(
        newrule).replace(' ', '%20').replace("'", "%92").replace("&", "%26")
    resultsxpath = "string(//div[@id='narrow_results']/a[1]/span)"
    time.sleep(random.uniform(1, 3))
    results = getmess(url, resultsxpath)[1].replace(' Wines', '').replace(',', '').replace('+', '')
    if int(results) > 0:
        try:
            pagesResult = getmess(url, resultsxpath)[0].xpath('//form[@id="top_goto"]/a/text()')[0]
            pages = re.findall("of(.*)", pagesResult)[0].strip()
        except IndexError:
            perpage = getmess(url, resultsxpath)[0].xpath('//a[@id="top_paging"]/text()')[0]
            pages = math.ceil(int(results) / int(perpage))
        for page in range(int(pages)):
            spuurl = url + '&Page=' + str(page + 1)
            hrefxpath = "//table[@id='main_table']//tr/td[1]//@href"
            hrefs = getmess(spuurl, hrefxpath)[1]
            for href in hrefs:
                time.sleep(random.uniform(1, 3))
                wineurl = "https://www.cellartracker.com/" + str(href)
                namemessxpath = "string(//div[@id='wine_copy_inner']/h1)"
                winehtml = getmess(wineurl, namemessxpath)[0]
                namemess = getmess(wineurl, namemessxpath)[1]
                try:
                    score = winehtml.xpath('string(//div[@id="wine_copy_inner"]/div[1]/span[1])') + winehtml.xpath(
                        'string(//div[@id="wine_copy_inner"]/div[1]/span[2])')
                except:
                    score = ''
                try:
                    try:
                        vintage = re.findall('\\d{4}', namemess)[0]
                    except IndexError:
                        vintage = re.findall('NV', namemess)[0]
                except:
                    vintage = ''
                name = namemess.replace(vintage, '').strip() + ' ' + winehtml.xpath(
                    'string(//div[@id="wine_copy_inner"]/h2)').strip()
                regionlen = len(winehtml.xpath('//div[@id="wine_copy_inner"]/ul/li'))
                if regionlen == 0:
                    country, region, sub_region = '', '', ''
                elif regionlen == 1:
                    country = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[1]/a)')
                    region, sub_region = '', ''
                elif regionlen == 2:
                    country = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[1]/a)')
                    region = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[2]/a)')
                    sub_region = ''
                elif regionlen > 2:
                    country = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[1]/a)')
                    region = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[2]/a)')
                    sub_region = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[' + str(regionlen) + ']/a)')
                # print(str(('CT', '1',id,old_rule,changUni(name),vintage,changUni(country),changUni(region),changUni(sub_region),score)))
                mysql = "INSERT INTO `crawl` (`from`, `type`,`classNameId`,`className`,`wineName`,`vintage`,`country`,`region`,`sub_region`,`score`)" \
                        "VALUES" + (str(('CT', '1', id, old_rule, changUni(name), vintage, changUni(country),
                                         changUni(region), changUni(sub_region), score)))
                sqlLock.acquire()
                cursor2.execute(mysql)
                sql2.commit()
                sqlLock.release()
    else:
        # print(str(('CT', '1', id, old_rule)))
        mysql = "INSERT INTO `crawl` (`from`, `type`, `classNameId`, `className`) VALUES " + (
            str(('CT', '1', id, old_rule)))
        sqlLock.acquire()
        cursor2.execute(mysql)
        sql2.commit()
        sqlLock.release()


def main():
    concurrentpool = ThreadPoolExecutor(max_workers=20)
    # 线程数和线程名
    concurrentLists = []
    for id in getRules():
        g = concurrentpool.submit(crawl, id)
        concurrentLists.append(g)
    # concurrentpool.map(crawl, [33647,38489,38490,38485])
    wait(concurrentLists, return_when=FIRST_COMPLETED)
    for future in as_completed(concurrentLists):
        data = future.done()
        if data is True:
            future.cancel()


if __name__ == '__main__':
    try:
        main()
    finally:
        print('\r\nFinished')
