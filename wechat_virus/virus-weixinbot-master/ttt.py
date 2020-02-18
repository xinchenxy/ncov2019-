# import re
import requests
import json
# string = "山东省青岛市市南区泰安路2号"
# city_regex = r'.*?省(.*?)市'
# print(re.findall(city_regex, string)[0])
# import heapq
# lisy_1 = [1,5,8,3,4,9,7,2,3,0,5]
#
# smallest_index_list = []
#
# re1 = map(lisy_1.index, heapq.nsmallest(3, lisy_1))
# # print(type(re1))
# for m in list(re1):
#     # print(m)
#     smallest_index_list.append(m)
# print(smallest_index_list)
# import math
# lat1 = (math.pi / 180) * float(25.013399)
# lat2 = (math.pi / 180) * float(30.493612)
# lon1 = (math.pi / 180) * float(102.701859)
# lon2 = (math.pi / 180) * float(114.946823)
# R = 6378.137
# # d =  math.acos(math.sin(latitude1)*math.sin(latitude2)+ math.cos(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1))*R
# d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)) * R
# d = round(d, 1)
# print(d)
hg_data_url_1 = "https://fy.hiwangchong.com/index/index/api/aid/130.html"
# i = '湖北省黄冈市黄州区南湖街道刘家湾'
# url_1= 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak=VIh9s8WGZFh4C4ex6Ie38IEXPDcqeS23'.format(i)
#
# def get_data_huanggang_txt(hg_data_url_1):
#     new_list = []
#     response = requests.get(hg_data_url_1)
#     illness_table = str(response.text)
#     a = illness_table.lstrip('initMap(')
#     b = a.rstrip(');')
#     m = eval(b)
#     print(len(m))
# get_data_huanggang_txt(hg_data_url_1)
#
# get_data_huanggang_txt(hg_data_url_1)
#
#
# def text_inpt(your_question):
#     urls = 'http://openapi.tuling123.com/openapi/api/v2'  # 请求地址
#     datainput = your_question
#     data_dic = {
#         "reqType": 0,
#         "perception": {
#             "inputText": {
#                 "text": datainput
#             },
#             "inputImage": {
#                 "url": "imageUrl"
#             },
#             "selfInfo": {
#                 "location": {
#                     "city": "北京",
#                     "province": "北京",
#                     "street": "信息路"
#                 }
#             }
#         },
#         "userInfo": {
#             "apiKey": "37349261b1f74fa9a2d6d34fe8548c4a",
#             "userId": "demo"
#         }
#     }
#
#     data_json = json.dumps(data_dic).encode('utf8')
#     a = requests.post(urls, data_json)  # 使用post请求
#     content = (a._content).decode('utf-8')  # 获取返回结果_content属性，解码
#     res = json.loads(content)  # 反序列化
#     print(res['results'][0]['values']['text'])
# import re
# tt = '[Escape:at,nickname=Bot by xy,wxid=wxid_8jhin5q597qz12] 测试2'
# pattern_regex = r'(?<=]).*'
# at_mesg = re.findall(pattern_regex, tt)
# print(at_mesg)
# import datetime
# print(int(datetime.datetime.now().second))
# import re
# tt = '纽约时报100'
# pattern_regex = r'(?<=纽约时报).*'
# at_mesg = re.findall(pattern_regex, tt)
# if at_mesg[0] == '':
#     print(0)
# try:
#     print(int(at_mesg[0]))
# except:
#     print('cuowu')

# a = '公众号：碎念'
# b = '土堆'
# str_list = list(a)
# str_list.insert(4, b)
# a_b = ''.join(str_list)
t = '概要：新冠病毒的致死率据估最低可能与流感差不多，但公众对两者的反应却形成巨大反差。对新冠疫情感到恐惧并非不理智的表现，但说明了人们在风险评估方面存在的缺陷。。'

def str_list(t):
    m=''
    for i in list(t):
        m += i +'.'
    print(m)
    return m
