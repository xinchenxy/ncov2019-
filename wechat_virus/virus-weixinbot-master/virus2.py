# -*- coding: utf-8 -*-
import requests
import time
import urllib
import difflib
import re
import sqlite3


def overall(r):
    # url = "https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia"
    # r = requests.get(url).json()
    # 获取返回的json数据

    # 确诊人数
    confirmedCount = r['data']['statistics']['confirmedCount']
    # 疑似感染人数
    suspectedCount = r['data']['statistics']['suspectedCount']
    # 治愈人数
    curedCount	 = r['data']['statistics']['curedCount']
    # 死亡人数
    deadCount = r['data']['statistics']['deadCount']
    # 数据最后变动时间
    updateTime = int(r['data']['statistics']['modifyTime'])/1000

    return confirmedCount, suspectedCount, curedCount, deadCount, updateTime
    # print(confirmedCount)
    # print(suspectedCount)
    # print(curedCount)
    # print(deadCount)
    # print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(updateTime)))

def area(r, areaname):
    # 分割省份地区
    arealist = re.split(r'[;,\s]\s*', areaname)
    provincename = arealist[0]
    if len(arealist)>1:
        cityname = arealist[1]

    # 获取省份名称模糊匹配
    # url = "https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia"
    # r = requests.get(url).json()
    # url = "https://lab.isaaclin.cn/nCoV/api/provinceName"
    provincenameList = []
    countrylist =[]
    for x in r['data']['listByCountry']:
        provincenameList.append(x['provinceName'])
    for x in r['data']['listByOther']:
        countrylist.append(x['name'])



    # print(provincenameList)

    # 匹配省份国家
    flag = 0
    province = ''.join(difflib.get_close_matches(provincename, provincenameList, 1, cutoff=0.1))
    if province == '':
        province = ''.join(difflib.get_close_matches(provincename, countrylist, 1, cutoff=0.1))
        if province == '':
            return "未查询到数据", 0 , 0, 0, 0, 0
        flag = 1
    # url2 = "https://lab.isaaclin.cn/nCoV/api/area?province=" + urllib.parse.quote(provice)
    # provicemsg = requests.get(url2).json()
    # print(provicemsg)

    if len(arealist)==1:
        if flag == 0:
            for x in r['data']['listByCountry']:
                if province == x['provinceName']:
                    # 确诊人数
                    confirmedCount = x['confirmed']
                    # 疑似感染人数
                    suspectedCount = x['suspected']
                    # 治愈人数
                    curedCount = x['cured']
                    # 死亡人数
                    deadCount = x['dead']
                    # 数据最后变动时间
                    updateTime = int(x['modifyTime']) / 1000

                    return province, confirmedCount, suspectedCount, curedCount, deadCount, updateTime

        if flag == 1:
            for x in r['data']['listByOther']:
                if province == x['name']:
                    # 确诊人数
                    confirmedCount = x['confirmed']
                    # 疑似感染人数
                    suspectedCount = x['suspected']
                    # 治愈人数
                    curedCount = x['cured']
                    # 死亡人数
                    deadCount = x['dead']
                    # 数据最后变动时间
                    updateTime = int(x['modifyTime']) / 1000
                    return province, confirmedCount, suspectedCount, curedCount, deadCount, updateTime


    # 如果检测到城市
    if len(arealist) > 1:
        # 遍历城市列表近似匹配城市
        citylist = []
        for x in r['data']['listByArea']:
            if province == x['provinceName']:
                for y in x['cities']:
                    citylist.append(y['cityName'])

                city = ''.join(difflib.get_close_matches(cityname, citylist, 1, cutoff=0.1))
                for y in x['cities']:
                    if(y['cityName']==city):
                        # 确诊人数
                        confirmedCount = y['confirmed']
                        # 疑似感染人数
                        suspectedCount = y['suspected']
                        # 治愈人数
                        curedCount = y['cured']
                        # 死亡人数
                        deadCount = y['dead']
                        # 数据最后变动时间
                        updateTime = int(r['data']['statistics']['modifyTime']) / 1000

                        return city, confirmedCount, suspectedCount, curedCount, deadCount, updateTime

        return "未查询到数据", 0, 0, 0, 0, 0
    else:
        return "未查询到数据", 0, 0, 0, 0, 0


def news(news):
    conn = sqlite3.connect('virusnews.db')
    cur = conn.cursor()
    # url = "https://lab.isaaclin.cn/nCoV/api/news"
    # url = "https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia"
    #
    # news = requests.get(url).json()
    newslist=[]
    print("--------------------\n执行新闻刷新任务\n")
    for x in news['data']['timeline']:
        if re.findall('(确诊)|(例)|(新增)|(治愈)|(出院)|(累计)|(药)|(钟南山)|(辟谣)|(谣言)|(疫情)|(病毒)|(专家)|(新疆)|(风险)|(世卫组织)|(传播)|(聚集性)', x['title'])==[]:
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

    if newslist==[]:
        print("无新新闻\n--------------------")

    return newslist


def provinceall(r, provincename):

    # 获取省份名称模糊匹配
    # url = "https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia"
    # r = requests.get(url).json()
    # url = "https://lab.isaaclin.cn/nCoV/api/provinceName"
    provincenameList = []
    countrylist =[]
    for x in r['data']['listByCountry']:
        provincenameList.append(x['provinceName'])
    for x in r['data']['listByOther']:
        countrylist.append(x['name'])

    # print(provincenameList)

    # 匹配省份国家
    flag = 0
    province = ''.join(difflib.get_close_matches(provincename, provincenameList, 1, cutoff=0.1))
    if province == '':
        province = ''.join(difflib.get_close_matches(provincename, countrylist, 1, cutoff=0.1))
        if province == '':
            return "未查询到数据"
        flag = 1
    # url2 = "https://lab.isaaclin.cn/nCoV/api/area?province=" + urllib.parse.quote(provice)
    # provicemsg = requests.get(url2).json()
    # print(provicemsg)

    if flag == 0:
        provincemsg = province + ":\n"
        for x in r['data']['listByArea']:
            if province == x['provinceName']:
                for y in x['cities']:
                    provincemsg = provincemsg + str(y['cityName']) + "：确诊" + str(y['confirmed']) + ",治愈" + str(y['cured']) + ",死亡" + str(y['dead']) + "\n"

                updateTime = int(r['data']['statistics']['modifyTime']) / 1000
                provincemsg = provincemsg + "数据最后更新时间：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))
                return provincemsg

    if flag == 1:
        for x in r['data']['listByOther']:
            if province == x['name']:
                # 确诊人数
                confirmedCount = x['confirmed']
                # 疑似感染人数
                suspectedCount = x['suspected']
                # 治愈人数
                curedCount = x['cured']
                # 死亡人数
                deadCount = x['dead']
                # 数据最后变动时间
                updateTime = int(x['modifyTime']) / 1000

                returnmsg = str(province) + ":\n" + "确诊人数：" + str(confirmedCount) + "\n" + \
                            "治愈人数：" + str(curedCount) + "\n" + "死亡人数：" + \
                            str(deadCount) + "\n" + "数据最后更新时间：" +\
                            str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))
                return returnmsg


if __name__ == '__main__':
    url = "https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia"
    r = requests.get(url).json()

    # returnmsg = provinceall(r, '库尔勒')
    # print(returnmsg)




    newslist = news(r)
    print(newslist)


    # overall
    # confirmedCount, suspectedCount, curedCount, deadCount, updateTime = overall(r)
    # print("截至", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)), "：")
    # print("全国确诊人数：", confirmedCount)
    # print("疑似感染人数：", suspectedCount)
    # print("治愈人数：", curedCount)
    # print("死亡人数：", deadCount)

    # area
    # area, confirmedCount, suspectedCount, curedCount, deadCount, updateTime = area(r, '新疆 吐鲁番')
    # if(area == "未查询到数据"):
    #     print(area)
    # else:
    #     print(area, ":")
    #     print("确诊人数：", confirmedCount)
    #     print("疑似感染人数：", suspectedCount)
    #     print("治愈人数：", curedCount)
    #     print("死亡人数：", deadCount)
    #     print("数据最后变动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))






