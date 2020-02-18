import requests
import sxtwl
import datetime
from datetime import date
import lxml
from lxml import etree
# 日历中文索引
ymc = [u"十一", u"十二", u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十"]
rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十", \
       u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九", \
       u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]

# 日历库实例化
lunar = sxtwl.Lunar()



# 2.阳历转阴历


def china_lunar():
    today = str(date.today())

    today_list = today.split('-')  # ['2019', '08', '08']
    lunar_day = lunar.getDayBySolar((int)(datetime.datetime.now().year), (int)(datetime.datetime.now().month), (int)(datetime.datetime.now().day))  # 输入年月日
    # 判断是否为润年
    if (lunar_day.Lleap):
        china_day = "农历:{0}月{1}".format(ymc[lunar_day.Lmc], rmc[lunar_day.Ldi])
    else:
        china_day ="农历:{0}月{1}".format(ymc[lunar_day.Lmc], rmc[lunar_day.Ldi])
    return today,china_day


import json
def morning_news():
    news_api = 'http://api.tianapi.com/bulletin/index?key=7d407997897033ce7f6e86a51e3284d2'
    response = requests.get(news_api)
    print(dict(response.json()))
    news_list = dict(response.json())
    news = ''
    m = 1
    news_q=''
    for i in news_list['newslist']:
        img_url=''
        if i['url'] == '':
            img_url = i['imgsrc']
        news = str(str(m)+":"+i['title']+"\n"+i['url']+img_url+"\n")
        news_q += str(news)
        m += 1

    return news_q

def news_put():
    news_spider_message = '【早间新闻】 '+china_lunar()[0]+" "+china_lunar()[1]+"\n"+morning_news()
    return news_spider_message


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

def NewYork_news(page=1):
    society = 'https://cn.nytimes.com/society/{}/'.format(page)
    response = requests.get(url=society,headers =headers )
    mytree = lxml.etree.HTML(response.text)
    title = mytree.xpath('//*[@id="sectionWrapper"]/div[1]/div/div/ul//h3/a')

    news = mytree.xpath('//*[@id="sectionWrapper"]/div[1]/div/div/ul//p')
    url = mytree.xpath('//*[@id="sectionWrapper"]/div[1]/div/div/ul//h3/a/@href')
    # print(mytree.xpath('//*[@id="sectionWrapper"]/div[1]/div[2]/div/ul//h3/a')[1].text)  #这个是标题
    # print(mytree.xpath('//*[@id="sectionWrapper"]/div[1]/div[2]/div/ul//p')[1].text)  # 这个是简介
    #
    # print(mytree.xpath('//*[@id="sectionWrapper"]/div[1]/div[2]/div/ul//h3/a/@href')[1])  # 这个是链接
    newss_1 = ''
    number = 1
    for t in title:

        newss = str(number)+":"+str_list(t.text) +'。'+'\n'+'    概要：'+str_list(news[title.index(t)].text)+'。'+'\n'+'    详情：'+'\n'+'\n'
        newss_1 +=newss
        number += 1

    return newss_1



def NewYork_news_put(page=0):
    news_spider_message = '【纽约时报中文网】'+china_lunar()[0]+" "+china_lunar()[1]+"\n"+NewYork_news(page)

    return news_spider_message

def str_list(t):
    m=''
    for i in list(t):
        if i == '中':
            china = 'Z'
            m += china +'_'
        else:

            m += i + '_'


    return m
