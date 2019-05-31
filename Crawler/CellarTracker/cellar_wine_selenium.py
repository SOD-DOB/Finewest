import re
import pymysql
import string
import time
import random
import zipfile
import math
import unicodedata
import numpy as np
import selenium.webdriver.support.ui as ui
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def create_proxy_auth_extension(proxy_host, proxy_port,
                                proxy_username, proxy_password,
                                scheme='http', plugin_path=None):
    if plugin_path is None:
        plugin_path = r'./{}_{}@http-pro.abuyun.com_9010.zip'.format(proxy_username, proxy_password)
    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Abuyun Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_path

def getRules():
    # 所有的
    goodsrules = "SELECT `id` FROM `shopping_goodsrules`"
    cursor1.execute (goodsrules)
    rules_list = cursor1.fetchall ()
    rulesid = [str(i[0]) for i in rules_list]
    # 已查询的
    testrules = "SELECT `classNameId` FROM `crawl_cellar` group by `classNameId`"
    cursor2.execute(testrules)
    cellarlist = cursor2.fetchall ()
    cellar = [str(i[0]) for i in cellarlist]
    # 未查询的
    idlist = list(id for id in rulesid if id not in cellar)
    return idlist

def re_name(x):
    try:
        a = "".join (re.compile (r'[^\u4E00-\u9FA5]').findall (x))
        b = re.findall (r'[(](.*?)[)]', str (a))[0]
        name = a.replace ('(' + b + ')', '').strip ()
    except:
        name = "".join (re.compile (r'[^\u4E00-\u9FA5]').findall (x))
    return name # 非中文

def changUni(unic):
    change = unicodedata.normalize ('NFKD', unic).encode ('ascii', 'ignore').strip () # 转换法语
    code = str (change, encoding='utf-8')
    return code

def getMess(id):
    goodsrules = "SELECT `className` FROM `shopping_goodsrules` where id =" + str (id)
    cursor1.execute (goodsrules)
    old_rule = cursor1.fetchall ()[0][0].strip ()
    print ('\r\n 查找:', id, old_rule)
    newrule = changUni (re_name (old_rule)).strip ()
    url = "https://www.cellartracker.com/search.asp?QTable=AllWines&S=" + str (newrule).replace (' ','%20') + "&SaveSearch=True"
    # url = "https://www.cellartracker.com/list.asp?fInStock=0&iUserOverride=0&Table=List&szSearch=" + str (newrule).replace (' ', '%20')
    driver.implicitly_wait (60)
    driver.get(url)
    time.sleep(2)
    results = driver.find_element_by_xpath("//div[@id='narrow_results']/a[1]/span").text.replace(' Wines','').replace(',','')
    if int(results)>0:
        perpage = driver.find_element_by_xpath('//a[@id="top_paging"]').text
        pages = math.ceil (int (results) / int(perpage))
        for page in range(pages):
            spuurl = url+'&Page='+str(page+1)
            driver.get(spuurl)
            hrefs = len(driver.find_element_by_xpath("//table[@id='main_table']//tr/td[1]//a"))
            for href in range(hrefs):
                js = 'document.getElementsByClassName("more")[' + str (href+1) + '].click();'
                driver.execute_script (js)
                handle = driver.window_handles  # 获取句柄
                driver.switch_to.window (handle[-1])

                time.sleep (random.uniform (2, 5))
                namemess = driver.find_element_by_xpath("string(//div[@id='wine_copy_inner']/h1)")
                try:
                    score = driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/div[1]/span[1]').text+\
                            driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/div[1]/span[2]').text
                except:
                    score = ''
                try:
                    try:
                        vintage = re.findall('\\d{4}',namemess)[0]
                    except IndexError:
                        vintage = re.findall('NV',namemess)[0]
                except:
                    vintage = ''
                name = namemess.replace(vintage,'').strip()+' '+driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/h2').text.strip()
                regionlen = len(driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/ul/li'))
                if regionlen == 0:
                    country,region,sub_region = '','',''
                elif regionlen == 1:
                    country = driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/ul/li[1]/a').text
                    region, sub_region = '', ''
                elif regionlen == 2:
                    country = driver.find_element_by_xpath ('//div[@id="wine_copy_inner"]/ul/li[1]/a').text
                    region = driver.find_element_by_xpath ('//div[@id="wine_copy_inner"]/ul/li[2]/a').text
                    sub_region = ''
                elif regionlen >2:
                    country = driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/ul/li[1]/a').text
                    region = driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/ul/li[2]/a').text
                    sub_region = driver.find_element_by_xpath('//div[@id="wine_copy_inner"]/ul/li['+str(regionlen)+']/a').text
                print(str(('0',id,old_rule,changUni(name),vintage,changUni(country),changUni(region),changUni(sub_region),score)))
                mysql = "INSERT INTO `crawl_cellar` (`type`,`classNameId`,`className`,`wineName`,`vintage`,`country`,`region`,`sub_region`,`score`)" \
                        "VALUES"+(str(('0',id,old_rule,changUni(name),vintage,changUni(country),changUni(region),changUni(sub_region),score)))
                # cursor2.execute(mysql)
                # sql2.commit()
                driver.close ()
                driver.switch_to.window (handle[0])
    else:
        print(str(('0',id,old_rule)))
        # mysql = "INSERT INTO `crawl_cellar` (`type`,`classNameId`,`className`)VALUES" + (str (('0', id, old_rule)))
        # cursor2.execute(mysql)
        # sql2.commit()

if __name__ == '__main__':
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

    # finewest
    sql1 = pymysql.connect (
        host='',
        port=,
        user='',
        password='',
        db=''
    )
    cursor1 = sql1.cursor ()

    # finewest_test
    sql2 = pymysql.connect (
        host='',
        port=,
        user='',
        password='',
        db=''
    )
    cursor2 = sql2.cursor ()

    # 代理IP
    proxyHost = "http-pro.abuyun.com"
    proxyPort = ""
    proxyUser = ""
    proxyPass = ""
    proxy_auth_plugin_path = create_proxy_auth_extension (
        proxy_host=proxyHost,
        proxy_port=proxyPort,
        proxy_username=proxyUser,
        proxy_password=proxyPass)
    options = webdriver.ChromeOptions ()
    options.add_argument ('disable-infobars')  # 隐藏"Chrome正在受到自动软件的控制"
    options.add_argument ("--start-maximized")
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument ('user-agent='+random.choice(UA))
    # options.add_argument ('--headless')  # 使用无头谷歌浏览器模式
    options.add_argument ('--disable-gpu')
    options.add_argument ('blink-settings=imagesEnabled=false')  # 不加载图片
    options.add_extension (proxy_auth_plugin_path)
    driver = webdriver.Chrome (executable_path='D:/Programs/Python/Python37/Scripts/chromedriver/chromedriver.exe',
                               chrome_options=options)


    # driver.get("http://www.fynas.com/ua/view")
    for i in getRules()[100:]:
        getMess (i)

    time.sleep (5)
    driver.close ()
    driver.quit()
