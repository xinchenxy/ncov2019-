# -*- coding: utf-8 -*-
import requests
import time
import urllib
import difflib
import re
import sqlite3


def overall():
    url = "https://lab.isaaclin.cn/nCoV/api/overall"
    r = requests.get(url).json()
    # 获取返回的json数据

    # 确诊人数
    confirmedCount = r['results'][0]['confirmedCount']
    # 疑似感染人数
    suspectedCount = r['results'][0]['suspectedCount']
    # 治愈人数
    curedCount	 = r['results'][0]['curedCount']
    # 死亡人数
    deadCount = r['results'][0]['deadCount']
    # 数据最后变动时间
    updateTime = int(r['results'][0]['updateTime'])/1000

    return confirmedCount, suspectedCount, curedCount, deadCount, updateTime
    # print(confirmedCount)
    # print(suspectedCount)
    # print(curedCount)
    # print(deadCount)
    # print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(updateTime)))

def area(areaname):
    # 分割省份地区
    arealist = re.split(r'[;,\s]\s*', areaname)
    provincename = arealist[0]
    if len(arealist)>1:
        cityname = arealist[1]

    # 获取省份名称模糊匹配
    url = "https://lab.isaaclin.cn/nCoV/api/provinceName"
    provincenameList = requests.get(url).json()['results']
    # print(provincenameList)

    # 匹配省份
    provice = ''.join(difflib.get_close_matches(provincename, provincenameList, 1, cutoff=0.1))
    if provice == '':
        return "未查询到数据", 0 , 0, 0, 0, 0
    url2 = "https://lab.isaaclin.cn/nCoV/api/area?province=" + urllib.parse.quote(provice)
    provicemsg = requests.get(url2).json()
    # print(provicemsg)

    if len(arealist)==1:
        # 确诊人数
        confirmedCount = provicemsg['results'][0]['confirmedCount']
        # 疑似感染人数
        suspectedCount = provicemsg['results'][0]['suspectedCount']
        # 治愈人数
        curedCount = provicemsg['results'][0]['curedCount']
        # 死亡人数
        deadCount = provicemsg['results'][0]['deadCount']
        # 数据最后变动时间
        updateTime = int(provicemsg['results'][0]['updateTime']) / 1000

        return provice, confirmedCount, suspectedCount, curedCount, deadCount, updateTime
    # 如果检测到城市
    if len(arealist) > 1:
        # 遍历城市列表近似匹配城市
        citylist = []
        for x in provicemsg['results'][0]['cities']:
            citylist.append(x['cityName'])

        city = ''.join(difflib.get_close_matches(cityname, citylist, 1, cutoff=0.1))
        for x in provicemsg['results'][0]['cities']:
            if(x['cityName']==city):
                # 确诊人数
                confirmedCount = x['confirmedCount']
                # 疑似感染人数
                suspectedCount = x['suspectedCount']
                # 治愈人数
                curedCount = x['curedCount']
                # 死亡人数
                deadCount = x['deadCount']
                # 数据最后变动时间
                updateTime = int(provicemsg['results'][0]['updateTime']) / 1000

                return city, confirmedCount, suspectedCount, curedCount, deadCount, updateTime

        return "未查询到数据", 0, 0, 0, 0, 0
    else:
        return "未查询到数据", 0, 0, 0, 0, 0


def news():
    conn = sqlite3.connect('virusnews.db')
    cur = conn.cursor()
    url = "https://lab.isaaclin.cn/nCoV/api/news"
    news = requests.get(url).json()
    newslist=[]
    print(news)
    for x in news['results']:
        if re.findall('(确诊)|(首例)|(新增)|(治愈)|(出院)|(累计)', x['title'])==[]:
            continue
        else:
            try:
                cursor = conn.execute("SELECT site from news WHERE site = ?", [x['sourceUrl']])
                sites = cursor.fetchall()

                if len(sites) != 0:
                    continue
                # 数据库中没有 属于新新闻，加入数据库并返回
                # id = int(x['provinceId'])
                # sites = x['sourceUrl']
                # conn.execute("INSERT INTO news VALUES ('id','sites')")
                cur = conn.cursor()
                cur.execute("INSERT INTO news VALUES (?,?)", [int(x['provinceId']), x['sourceUrl']])
                newslist.append(x)

                # if results==None:
                #     print("未找到结果")
            except:
                # 数据库中没有 属于新新闻，加入数据库并返回
                # id = int(x['provinceId'])
                # sites = x['sourceUrl']
                # cur.execute("INSERT INTO news VALUES ('id','sites')")

                conn.execute("INSERT INTO news VALUES (?,?)", [int(x['provinceId']), x['sourceUrl']])
                newslist.append(x)

    conn.commit()
    cur.close()
    conn.close()
    return newslist


if __name__ == '__main__':

    newslist = news()
    print(newslist)


    # # overall
    # confirmedCount, suspectedCount, curedCount, deadCount, updateTime = overall()
    # print("截至", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)), "：")
    # print("全国确诊人数：", confirmedCount)
    # print("疑似感染人数：", suspectedCount)
    # print("治愈人数：", curedCount)
    # print("死亡人数：", deadCount)

    # # area
    # area, confirmedCount, suspectedCount, curedCount, deadCount, updateTime = area('新疆 吐鲁番')
    # if(area == "未查询到数据"):
    #     print(area)
    # else:
    #     print(area, ":")
    #     print("确诊人数：", confirmedCount)
    #     print("疑似感染人数：", suspectedCount)
    #     print("治愈人数：", curedCount)
    #     print("死亡人数：", deadCount)
    #     print("数据最后变动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))






