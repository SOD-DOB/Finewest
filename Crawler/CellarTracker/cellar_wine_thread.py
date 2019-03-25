import requests
import numpy as np
import pymysql
import re,time
import random
import math
from lxml import html as HTML
import threading
import queue
import unicodedata
threadLock = threading.Lock ()
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
    "port": '9010',
    "user": 'H6B8WY3O4988764P',
    "pass": 'B44BC8FAD71691A4',
}
proxies = {'https': proxyMeta,
           'http': proxyMeta, }

header = {
    # 'Cookie':'_ga=GA1.2.1187845717.1550540407; GS%5FPopularWinesTab=1; __gads=ID=15d96058cc8a7466:T=1550540408:S=ALNI_Ma5WaBFuQug8dhbZ4pI9OHmMhFSew; d7s_uid=jsb3q4urphkbbl; LastTable=AllWines; _gid=GA1.2.485643615.1552269672; SPSI=29aea109848dbe973296c75617848525; sbtsck=jav3yw6FeLLEvftpz/+3tjEMuBDZ9/lCt7lI9nJFh7Eg5I=; UTGv2=h49bda5211e3865cd658b47569987f804241; GS%5FPageRecords=100; spcsrf=45536df2faa689b9bfd39bce361e304f; sp_lit=oX6CyF7Z6R+Yo+EhtF252Q==; PRLST=Za; _gat=1; adOtr=aF91A9a8084',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Host': 'www.cellartracker.com',
    'Referer':'https://www.cellartracker.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA),
}

# finewest
sql1 = pymysql.connect (
    host='rm-2zehi2ns25kee8568o.mysql.rds.aliyuncs.com',
    port=3306,
    user='fwread',
    password='Finewest1127',
    db='finewest'
)
cursor1 = sql1.cursor ()

# finewest_test
sql2 = pymysql.connect (
    host='rm-2zehi2ns25kee8568o.mysql.rds.aliyuncs.com',
    port=3306,
    user='fwtest',
    password='Finewest2018',
    db='fwtest'
)
cursor2 = sql2.cursor ()

def getRules():
    # 所有的
    goodsrules = "SELECT `id` FROM `shopping_goodsrules`"
    threadLock.acquire()
    cursor1.execute (goodsrules)
    threadLock.release()
    rules_list = cursor1.fetchall ()
    rulesid = [str(i[0]) for i in rules_list]
    # 已查询的
    testrules = "SELECT `classNameId` FROM `crawl_cellar` group by `classNameId`"
    threadLock.acquire()
    cursor2.execute(testrules)
    threadLock.release()
    cellarlist = cursor2.fetchall ()
    cellar = [str(i[0]) for i in cellarlist]
    # 未查询的
    idlist = list(id for id in rulesid if id not in cellar)
    id_queue = queue.Queue ()
    for id in idlist:
        id_queue.put(str(id))
    return id_queue

def re_name(x):
    try:
        a = "".join (re.compile (r'[^\u4E00-\u9FA5]').findall (x))
        b = re.findall (r'[(](.*?)[)]', str (a))[0]
        name = a.replace ('(' + b + ')', '').strip ()
    except:
        name = "".join (re.compile (r'[^\u4E00-\u9FA5]').findall (x))
    return name # 非中文

def tryUrl(url):
    while True:
        try:
            response = requests.get (url=url, headers=header, proxies=proxies)#verify=False,.content.decode('utf-8')
            time.sleep(2)
            html = HTML.fromstring(response.content)
            return html
        except:
            # print('\r\n   解析失败，重试中')
            time.sleep(random.uniform(3,8))
            continue

def changUni(unic):
    change = unicodedata.normalize ('NFKD', unic).encode ('ascii', 'ignore').strip () # 转换法语
    code = str (change, encoding='utf-8')
    return code

def getmess(url,xpathtree):
    while True:
        html = tryUrl(url)
        mess = html.xpath(xpathtree)
        if len(mess)>0:
            return html,mess
        else:
            continue

class myThread (threading.Thread):
    def __init__(self, name, id_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.id_queue = id_queue

    def run(self):
        while not self.id_queue.empty():
            try:
                crawl (self.name, self.id_queue)
            except:
                break
        # print ("Exiting " + self.name)

def crawl(threadName,Queue):
    id = Queue.get()
    goodsrules = "SELECT `className` FROM `shopping_goodsrules` where id =" + str (id)
    threadLock.acquire ()
    cursor1.execute (goodsrules)
    threadLock.release ()
    old_rule = cursor1.fetchall ()[0][0].strip()
    print ('\r\n',threadName,': 查找:',id, old_rule)
    newrule = changUni (re_name (old_rule)).strip()
    url = "https://www.cellartracker.com/list.asp?fInStock=0&iUserOverride=0&Table=List&szSearch="+str(newrule).replace(' ','%20')
    resultsxpath = "string(//div[@id='narrow_results']/a[1]/span)"
    time.sleep (random.uniform (1, 3))
    results = getmess(url,resultsxpath)[1].replace(' Wines','').replace(' ','')
    if int(results)>0:
        perpage = getmess(url,resultsxpath)[0].xpath('//a[@id="top_paging"]/text()')[0]
        pages = math.ceil (int (results) / int(perpage))
        for page in range(pages):
            spuurl = url+'&Page='+str(page+1)
            hrefxpath = "//table[@id='main_table']//tr/td[1]//@href"
            hrefs = getmess(spuurl,hrefxpath)[1]
            for href in hrefs:
                time.sleep (random.uniform (1, 3))
                wineurl = "https://www.cellartracker.com/"+str(href)
                namemessxpath = "string(//div[@id='wine_copy_inner']/h1)"
                winehtml = getmess(wineurl,namemessxpath)[0]
                namemess = getmess(wineurl,namemessxpath)[1]
                try:
                    score = winehtml.xpath('string(//div[@id="wine_copy_inner"]/div[1]/span[1])')+winehtml.xpath('string(//div[@id="wine_copy_inner"]/div[1]/span[2])')
                except:
                    score = ''
                try:
                    try:
                        vintage = re.findall('\\d{4}',namemess)[0]
                    except IndexError:
                        vintage = re.findall('NV',namemess)[0]
                except:
                    vintage = ''
                name = namemess.replace(vintage,'').strip()+' '+winehtml.xpath('string(//div[@id="wine_copy_inner"]/h2)').strip()
                regionlen = len(winehtml.xpath('//div[@id="wine_copy_inner"]/ul/li'))
                if regionlen == 0:
                    country,region,sub_region = '','',''
                elif regionlen == 1:
                    country = winehtml.xpath('string(//div[@id="wine_copy_inner"]/ul/li[1]/a)')
                    region, sub_region = '', ''
                elif regionlen == 2:
                    country = winehtml.xpath ('string(//div[@id="wine_copy_inner"]/ul/li[1]/a)')
                    region = winehtml.xpath ('string(//div[@id="wine_copy_inner"]/ul/li[2]/a)')
                    sub_region = ''
                elif regionlen >2:
                    country = winehtml.xpath ('string(//div[@id="wine_copy_inner"]/ul/li[1]/a)')
                    region = winehtml.xpath ('string(//div[@id="wine_copy_inner"]/ul/li[2]/a)')
                    sub_region = winehtml.xpath ('string(//div[@id="wine_copy_inner"]/ul/li['+str(regionlen)+']/a)')
                print(str(('0',id,old_rule,changUni(name),vintage,changUni(country),changUni(region),changUni(sub_region),score)))
                mysql = "INSERT INTO `crawl_cellar` (`type`,`classNameId`,`className`,`wineName`,`vintage`,`country`,`region`,`sub_region`,`score`)" \
                        "VALUES"+(str(('0',id,old_rule,changUni(name),vintage,changUni(country),changUni(region),changUni(sub_region),score)))
                threadLock.acquire()
                cursor2.execute(mysql)
                threadLock.release()
                sql2.commit()
    else:
        print(str(('0',id,old_rule)))
        mysql = "INSERT INTO `crawl_cellar` (`type`,`classNameId`,`className`)VALUES" + (str (('0', id, old_rule)))
        threadLock.acquire()
        cursor2.execute(mysql)
        threadLock.release()
        sql2.commit()

def main():
    # 线程数和线程名
    threadLists = []
    for i in range (1, 5):
        threadName = 'Thread-' + str (i)
        threadLists.append (threadName)
    # 创建新线程
    threads = []
    for threadName in threadLists:
        thread = myThread (threadName,getRules())
        thread.start ()
        threads.append (thread)
    for thread in threads:
        thread.join ()
    print ('finished')

if __name__ == '__main__':
    main()
