import requests
import json
import math
import time
import re
import heapq
import csv
import json
import urllib.request


cdn_data_url = ["https://assets.cbndata.org/2019-nCoV/0/data.json?timestamp=1581350147652",
"https://assets.cbndata.org/2019-nCoV/1/data.json?timestamp=1581350147652",
"https://assets.cbndata.org/2019-nCoV/2/data.json?timestamp=1581350147652",
"https://assets.cbndata.org/2019-nCoV/3/data.json?timestamp=1581350147652",
"https://assets.cbndata.org/2019-nCoV/4/data.json?timestamp=1581350147652",
"https://assets.cbndata.org/2019-nCoV/5/data.json?timestamp=1581350147652",]

hg_data_url = "https://fy.hiwangchong.com/index/index/api/aid/130.html"

list_person_number = []
def cal_dis(lat2,lon2):
    list_d = []
    for j in cdn_data_url:
        print(lat2)
        print(lon2)
        jea = requests.get(j).json()
        for i in jea['data']:
            try:
                lat1 = (math.pi / 180) * float(i['latitude'])
                lat2_z= (math.pi / 180) * float(lat2)
                lon1 = (math.pi / 180) * float(i['longitude'])
                lon2_z= (math.pi / 180) * float(lon2)
                R = 6378.137
                # d =  math.acos(math.sin(latitude1)*math.sin(latitude2)+ math.cos(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1))*R
                d = math.acos(math.sin(lat1) * math.sin(lat2_z) + math.cos(lat1) * math.cos(lat2_z) * math.cos(lon2_z - lon1)) * R
                d = round(d, 1)
                list_person_number.append(i)
                list_d.append(d)
            except :
                list_person_number.append(i)
                list_d.append(88888)

    return list_d,list_person_number
#
# def cal_dis(lat2,lon2):
#     for i in list()
#     try:
#
#         lat1 = (math.pi / 180) * float(i['latitude'])
#         lat2 = (math.pi / 180) * float(28.423941)
#         lon1 = (math.pi / 180) * float(i['longitude'])
#         lon2 = (math.pi / 180) * float(117.985321)
#         R = 6378.137
#         # d =  math.acos(math.sin(latitude1)*math.sin(latitude2)+ math.cos(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1))*R
#         d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)) * R
#         d = round(d, 1)
#         list_d.append(d)
#     except Exception as e:
#         print('数据错误')
#     return list_d
# cal_dis(28.423941,117.985321)
# print(len(list_d))
# re1 = map(list_d.index, heapq.nsmallest(5, list_d))  # 求最大的三个索引    nsmallest与nlargest相反，求最小
# re2 = heapq.nlargest(5, list_d)  # 求最大的三个元素
# print(list_d.index)
#
# print(list(re1)[0])

def smallest_people(list_d):
    smallest_index_list = []
    smallest_index_list_1 = []

    re1 = map(list_d.index, heapq.nsmallest(50, list_d))
    # print(type(re1))
    for m in list(re1):
        # print(m)
        smallest_index_list_1.append(m)

    smallest_index_list = list(set(smallest_index_list_1))
    smallest_index_list.sort(key=smallest_index_list_1.index)
# [1,7,8,5,4]
    return smallest_index_list

# print(smallest_index_list)
#
# # smallest_index_list = list(re1)
# print(smallest_index_list)
# print(type(smallest_index_list))
# print(len(smallest_index_list))# 因为re1由map()生成的不是list，直接print不出来，添加list()就行了


# for i in list
# def cal_dis(lat1,lon1,lat2,lon2):
#     lat1 = (math.pi/180)* float(lat1)
#     lat2 = (math.pi/180)* float(lat2)
#     lon1 = (math.pi/180)* float(lon1)
#     lon2= (math.pi/180)*  float(lon2)
#     #因此AB两点的球面距离为:{arccos[sinb*siny+cosb*cosy*cos(a-x)]}*R
#     #地球半径
#     R = 6378.137
#     #d =  math.acos(math.sin(latitude1)*math.sin(latitude2)+ math.cos(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1))*R
#     d =  math.acos(math.sin(lat1)*math.sin(lat2)+ math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))*R
#     d=round(d,1)
#     return d


# data = {'user': 'wxid_8jhin5q597qz12', 'type': 'msg::single', 'data': {'data_type': '48', 'is_recv': True, 'msgfromid': 'wxid_rpa8gzrbalz322', 'msgfrominfo': {'wx_id': 'wxid_rpa8gzrbalz322', 'wx_id_search': 'xiaki18186471485', 'wx_nickname': 'xiaki', 'remark_name': ''}, 'msgtoid': 'wxid_8jhin5q597qz12', 'msgtoinfo': None, 'sendid': 'wxid_rpa8gzrbalz322', 'sendinfo': {'wx_id': 'wxid_rpa8gzrbalz322', 'wx_id_search': 'xiaki18186471485', 'wx_nickname': 'xiaki', 'remark_name': ''}, 'msgcontent': '<?xml version="1.0"?>\n<msg>\n\t<location x="30.493591" y="114.946838" scale="16" label="黄州区红潭路" maptype="0" poiname="黄冈市黄州区路口小学(三环路30号)" poiid="" />\n</msg>\n'}}
# string ='<?xml version="1.0"?>\n<msg>\n\t<location x="30.493591" y="114.946838" scale="16" label="黄州区红潭路" maptype="0" poiname="黄冈市黄州区路口小学(三环路30号)" poiid="" />\n</msg>\n'

def Regex(message):
    pattern_X = r'.*?x="(.*?)"'
    pattern_Y= r'.*?y="(.*?)"'
    city_regex = r'.*?省(.*?)市'
    city_regex_2 = r'.*?l="(.*?)市'
    city_regex_3 = r'.*?l="(.*?)区'


    # print(re.findall(pattern_X, string))
    lat2 = float(re.findall(pattern_X, message)[0])
    lon2 = float(re.findall(pattern_Y, message)[0])
    city = re.findall(city_regex, message)
    city_1 = re.findall(city_regex_3, message)
    if len(city)==0:
        print("lalal")
        city = re.findall(city_regex_2, message)[0]
    else:
        city = city[0]
    print(lat2,lon2)

    return lat2 ,lon2,city,city_1

 # x="36.065220" y="120.312653"
# message="{'user': 'wxid_8jhin5q597qz12', 'type': 'msg::single', 'data': {'data_type': '48', 'is_recv': True, 'msgfromid': 'wxid_rpa8gzrbalz322', 'msgfrominfo': {'wx_id': 'wxid_rpa8gzrbalz322', 'wx_id_search': 'xiaki18186471485', 'wx_nickname': 'xiaki', 'remark_name': ''}, 'msgtoid': 'wxid_8jhin5q597qz12', 'msgtoinfo': None, 'sendid': 'wxid_rpa8gzrbalz322', 'sendinfo': {'wx_id': 'wxid_rpa8gzrbalz322', 'wx_id_search': 'xiaki18186471485', 'wx_nickname': 'xiaki', 'remark_name': ''}, 'msgcontent': '<?xml version="1.0"?>\n<msg>\n\t<location x="36.065220" y="120.312653" scale="16" label="山东省青岛市市南区泰安路2号" maptype="0" poiname="青岛站" poiid="qqmap_975564240653458324" />\n</msg>\n'}}"
# message = '<?xml version="1.0"?>\n<msg>\n\t<location x="36.065220" y="120.312653" scale="16" label="山东省青岛市市南区泰安路2号" maptype="0" poiname="青岛站" poiid="qqmap_975564240653458324" />\n</msg>\n'
# a = <?xml version="1.0"?>
# <msg>
# 	<location x="39.131073" y="117.362305" scale="16" label="天津市东丽区津汉公路" maptype="0" poiname="天津滨海国际机场" poiid="qqmap_14481560886654183831" />
# </msg>
# a = Regex(message)
# print(a[0])
# def get_distance_xy():
#
#     msg_content = message_global.get('data', {}).get('msgcontent', '')
#     re.compile(r'(^x="$").findall(msg_content)





## 没有地理位置信息 需要加进去
# 此处需要ak，ak申请地址：https://lbs.amap.com/dev/key/app


# encoding:utf-8

# 此处需要ak，ak申请地址：https://lbs.amap.com/dev/key/app
ak = "VIh9s8WGZFh4C4ex6Ie38IEXPDcqeS23"

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'https://restapi.amap.com/'
}


# 地理信息解析
# def amp_geocode(addr=None):
#     url = "http://api.map.baidu.com/geocoding/v3"
#     params = {"address": addr,
#               "ak": ak}
#     response = requests.get(url, params=params, headers=headers)
#     if response.status_code == 200:
#         # try:
#         loc_info = json.loads(response.text)
#
#         print(loc_info)
#         lng = loc_info.split(",")[0]
#         lat = loc_info.split(",")[1]
#         print(loc_info)
#         time.sleep(0.25)
#         return (lng, lat)
#         # except Exception as e:
#         #     print("Exception in amp_geocode",e)
#         #     time.sleep(5)
#         #     return None
#     else:
#         print("========>", response.status_code)
#         time.sleep(5)
#         return None
# a = amp_geocode("湖北省黄冈市黄州区南湖街道刘家湾")

i = '湖北省黄冈市黄州区南湖街道刘家湾'
url_1= 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak=VIh9s8WGZFh4C4ex6Ie38IEXPDcqeS23'.format(i)
def lng_lat_get(url, headers):
    a =requests.get(url=url,headers=headers)
    result = json.loads(a.text)
    # print(result)
    lng = dict(result)['result']['location']['lng']
    lat = dict(result)['result']['location']['lat']
    # print(lng)
    return lat,lng
# lng_lat_get(url_1,headers)
#
# def travel_list():
#     for i in range

# 爬取黄冈网站上的疫情数据存入data2中
hg_data_url_1 = "https://fy.hiwangchong.com/index/index/api/aid/130.html"
i = '湖北省黄冈市黄州区南湖街道刘家湾'
url_1= 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak=VIh9s8WGZFh4C4ex6Ie38IEXPDcqeS23'.format(i)

def get_data_huanggang_txt(hg_data_url_1):
    new_list = []
    response = requests.get(hg_data_url_1)
    illness_table = str(response.text)
    a = illness_table.lstrip('initMap(')
    b = a.rstrip(');')
    m = eval(b)
    print(len(m))
    count = 0
    for i in m:
        try:

            address_u = i['address']
            url_1 = 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak=VIh9s8WGZFh4C4ex6Ie38IEXPDcqeS23'.format(address_u)
            lat_lng = lng_lat_get(url_1,headers)
            i.setdefault('latitude', lat_lng[0])
            i.setdefault('longitude',lat_lng[1])
            count +=1
            new_list.append(i)
            time.sleep(0.1)
            print(count)





        except:

            print('速度太快')
    print(new_list)
    with open('data_2.txt', 'w',encoding='utf-8') as f:
        f.write(str(m))
#


def cal_dis_2(lat2,lon2):
    list_hg_d = []
    list_hg_person_number = []
    f = open('data_2.txt','r', encoding ='utf - 8')  # ‘r’可以省略，因为默认值就是r
    content = f.read()
    list_real = eval(content)


    for i in list_real:
        try:
            lat1 = (math.pi / 180) * float(i['latitude'])
            # print("*" * 100)
            # print(i['latitude'])
            # print("+" * 150)
            # print(lat1)
            lat2_z= (math.pi / 180) * float(lat2)
            # print("*" * 100)
            # print(lat2_z)
            # print("+" * 150)
            # print(lat2)
            lon1 = (math.pi / 180) * float(i['longitude'])
            # print(lon1)
            lon2_z= (math.pi / 180) * float(lon2)
            # print(lon2)
            R = 6378.137
            # d =  math.acos(math.sin(latitude1)*math.sin(latitude2)+ math.cos(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1))*R
            d = math.acos(math.sin(lat1) * math.sin(lat2_z) + math.cos(lat1) * math.cos(lat2_z) * math.cos(lon2_z - lon1)) * R
            d = round(d, 5)
            # print(d)
            list_hg_person_number.append(i)
            list_hg_d.append(d)
            # print(list_d)
            # print(d)
        except :
            list_hg_person_number.append(i)
            list_hg_d.append(88888)
            # print('数据错误')
    # print("*"*100)
    # print("列表长度")
    # print(len(list_d))
    # print(len(list_person_number))
    # print(list_d)
    # print(lat2_z)
    # print(lon2_z)
    # print(list_person_number)
    # print("*" * 100)
    return list_hg_d,list_hg_person_number

#机器人api

def text_inpt(your_question):
    urls = 'http://openapi.tuling123.com/openapi/api/v2'  # 请求地址
    datainput = your_question
    data_dic = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": datainput
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "信息路"
                }
            }
        },
        "userInfo": {
            "apiKey": "37349261b1f74fa9a2d6d34fe8548c4a",
            "userId": "demo"
        }
    }

    data_json = json.dumps(data_dic).encode('utf8')
    a = requests.post(urls, data_json)  # 使用post请求
    content = (a._content).decode('utf-8')  # 获取返回结果_content属性，解码
    res = json.loads(content)  # 反序列化
    print(res['results'][0]['values']['text'])
    answer = res['results'][0]['values']['text']
    return answer


