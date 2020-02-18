# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading
import re
import requests
from distance import Regex,cal_dis,smallest_people,cal_dis_2,text_inpt
from daily_news import news_put,NewYork_news_put
import datetime


import json
import math


import heapq


# 两个api接口，virus不稳定，故默认使用virus2接口，如果要改用virus接口的话需要对test.py做部分改动
import virus2 as virus
# import virus as virus


url = "https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia"

logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()
queue_recved_message_friendlist = Queue()


def on_message(message):
    queue_recved_message.put(message)
    queue_recved_message_friendlist.put(message)


def friendsList():
    idList = {'wxid_rpa8gzrbalz322':1, '7039690060@chatroom': 0, '2388359522@chatroom': 0}
    # , '7039690060@chatroom': 0, '2388359522@chatroom': 0
    # while not queue_recved_message_friendlist.empty():
    #     message = queue_recved_message_friendlist.get()
    #     print(message)
    #     # 遍历好友和群，用来推送新闻
    #     if 'friend::person' in message.get('type'):
    #         personId = message.get('data', {}).get('wx_id', '')
    #         # if personId != 'fmessage' and personId != 'floatbottle' and personId != 'newsapp' and personId != 'weixin' and personId != 'medianote':
    #         #     idList[personId] = 1
    #         if personId == 'wxid_rpa8gzrbalz322':
    #             print("检测到用户！：" + personId)
    #
    #         # elif personId == '7039690060@chatroom':
    #         #     chatroomid_1 =
    #         #     print("检测到群聊！：" + personId)
    #             idList = {'wxid_rpa8gzrbalz322':1,'7039690060@chatroom':0}

        # if 'friend::chatroom' in message.get('type'):
        #     chatroomId = message.get('data', {}).get('chatroom_id', '')
        #     idList[chatroomId] = 0
        #     print("检测到群聊！：" + chatroomId)


    return idList



# 消息处理示例 仅供参考

def thread_handle_message(wx_inst):



    while True:
        # schedule.run_pending()  # 运行所有可运行的任务
        # wx_inst.update_frinds()
        time.sleep(0.1)
        message = queue_recved_message.get()
        global returnmsg
        returnmsg = "0"

        message_global = message
        msgflag = 0
        if 'msg' in message.get('type'):
            print(message)
            time.sleep(1)

            # 这里是判断收到的是消息 不是别的响应
            msg_content = message.get('data', {}).get('msgcontent', '')    # 收到的消息
            if message.get('data', {}).get('msgfromid', ''):
                chatroom_wxid = message.get('data', {}).get('msgfromid', '')
            elif message.get('data', {}).get('from_wxid', ''):
                wx_id = message.get('data', {}).get('from_wxid', '')
                msgflag = 1

            send_or_recv = message.get('data', {}).get('is_recv', '')
            send_or_recv_1 = message.get('data', {}).get('data_type', '')
            print(send_or_recv)
            print('******************')
            # try:
            # 读取api数据
            f = open('APIDATA.txt', 'r')
            r_read = f.read()
            r = eval(r_read)
            f.close()
            # time.sleep(10)
            # print(send_or_recv)
            # print(send_or_recv['data']['data_type'])
            if send_or_recv == True and send_or_recv_1 =='1':

                print(msg_content)

                # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
                if "/virusall" in msg_content:
                    print(msg_content)
                    msglist = re.compile(r'(?<=/virusall ).*').findall(msg_content)
                    if msglist != []:
                        msg = ''.join(msglist)
                        returnmsg = virus.provinceall(r, msg)

                        if msgflag == 0:
                            wx_inst.send_text(chatroom_wxid, returnmsg)
                            print('aa')
                        else:
                            wx_inst.send_text(to_user=wx_id, msg=returnmsg)
                            print('bb')
                        time.sleep(1)


                elif "/virus" in msg_content :
                    print('msg')
                    msglist = re.compile(r'(?<=/virus ).*').findall(msg_content)
                    if msglist != []:
                        print('hello a ')
                        msg = ''.join(msglist)
                        area, confirmedCount, suspectedCount, curedCount, deadCount, updateTime = virus.area(r, msg)
                        if (area == "未查询到数据"):
                            print('cc')
                            returnmsg = area
                        else:
                            print('hello a ')
                            returnmsg = str(area) + ":\n" + "确诊人数：" + str(confirmedCount) + "\n" +\
                                        "治愈人数：" + str(curedCount) + "\n" + "死亡人数：" +\
                                        str(deadCount) + "\n" + "数据最后更新时间：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))
                            # wx_inst.send_text(chatroom_wxid, returnmsg)
                    else:
                        print('hello c ')
                        confirmedCount, suspectedCount, curedCount, deadCount, updateTime = virus.overall(r)
                        returnmsg = "截至" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime))) + \
                                    ":\n" + "确诊人数：" + str(confirmedCount) + "\n" + "疑似感染人数：" +\
                                    str(suspectedCount) + "\n" + "治愈人数：" + str(curedCount) + "\n" + "死亡人数：" + \
                                    str(deadCount)

                    # 在这里设置回复内容
                    if msgflag == 0:
                        print('fff')
                        wx_inst.send_text(chatroom_wxid, returnmsg)
                    else:
                        print('ddd')
                        wx_inst.send_text(to_user=wx_id, msg=returnmsg)
                    time.sleep(1)




                # 机器人发言的位置
                elif "/virusall" not in msg_content and "/virus" not in msg_content and '[Escape:at' in msg_content and "/纽约时报" not in msg_content:
                    pattern_regex = r'(?<=]).*'
                    at_mesg = re.findall(pattern_regex, msg_content)[0]
                    print(at_mesg)


                    returnmsg = text_inpt(at_mesg)







                    # 在这里设置回复内容
                    if msgflag == 0:
                        wx_inst.send_text(chatroom_wxid, returnmsg)
                    else:
                        wx_inst.send_text(to_user=wx_id, msg=returnmsg)
                    time.sleep(1)

                elif "/纽约时报" in msg_content:
                    pattern_regex = r'(?<=纽约时报).*'
                    at_mesg = re.findall(pattern_regex, msg_content)
                    try:
                        if at_mesg[0] == '':
                            q = 0
                            returnmsg = NewYork_news_put(q)
                        else:
                            try:
                                q = int(at_mesg[0])
                                returnmsg = NewYork_news_put(q)
                            except:
                                returnmsg = '网络请求错误'
                    except:

                        returnmsg = '网络请求错误'
                    if msgflag == 0:
                        wx_inst.send_text(chatroom_wxid, returnmsg)
                    else:
                        wx_inst.send_text(to_user=wx_id, msg=returnmsg)
                    time.sleep(1)
                else:
                    print('没走通')
            elif send_or_recv == True and send_or_recv_1 =='48':
                #
                print(msg_content)
                print('地图判定')
                dentist_city = Regex(msg_content)
                print(dentist_city[2])
                if dentist_city[2] == '黄冈' or dentist_city[3] =='黄州':
                    lat = dentist_city[0]
                    lon = dentist_city[1]
                    a = cal_dis_2(lat2=lat, lon2=lon)
                    print(a[0])
                    smallest_distance = smallest_people(a[0])
                    print(smallest_distance)
                    tt0 = smallest_distance[0]
                    tt1 = smallest_distance[1]
                    tt2 = smallest_distance[2]
                    returnmsg = "*"*35+"\n"+\
                                "根据当前位置信息判断："+"\n" +\
                                "*"*35+"\n" +"离你最近的3位患者分别是" +":\n"+ \
                                "1:  "+str(a[1][tt0]['beizhu']) +"\n"+"地址为："+str(a[1][tt0]['address'])+"\n"+ "确诊于:"+str(a[1][tt0]['date'])+"\n"+"(" + "距您"+str(a[0][tt0]) + "km)" + "\n"+\
                                "2:  "+str(a[1][tt1]['beizhu']) +"\n"+"地址为："+str(a[1][tt1]['address'])+"\n"+ "确诊于:"+str(a[1][tt1]['date'])+"\n"+"(" + "距您"+str(a[0][tt1]) + "km)" + "\n" +\
                                "3:  "+str(a[1][tt2]['beizhu']) +"\n"+"地址为："+str(a[1][tt2]['address'])+"\n"+ "确诊于:"+str(a[1][tt2]['date'])+"\n"+"(" + "距您"+str(a[0][tt2]) + "km)" + "\n" +"谢哥提醒你：勤洗手，戴口罩！ 不带你试试，试试就逝世！"



                # print(dentist_city)
                print(dentist_city[0])
                print(dentist_city[1])
                lat = dentist_city[0]
                lon = dentist_city[1]
                a = cal_dis(lat2=lat,lon2=lon)
                print(a[0])
                # a = cal_dis(Regex(msg_content)[0], Regex(msg_content)[1])
                if dentist_city[2] != '黄冈' and dentist_city[3] != '黄州':

                    city_single = []
                    smallest_distance = smallest_people(a[0])
                    print(smallest_distance)
                    tt0 = smallest_distance[0]
                    tt1 = smallest_distance[1]
                    tt2 = smallest_distance[2]
                    returnmsg = "*"*35+"\n"+\
                                "根据当前位置信息判断："+"\n" +\
                                "*"*35+"\n" +"离你最近的患者分别是" +":\n"+ \
                                "1:  "+"地址为："+str(a[1][tt0]['address'])+"\n"+ "确诊病例共计:"+str(a[1][tt0]['count'])+"位"+"(" + "距您"+str(a[0][tt0]) + "km)" + ":\n"+\
                                "2:  "+"地址为："+str(a[1][tt1]['address'])+"\n"+ "确诊病例共计:"+str(a[1][tt1]['count'])+"位"+"(" + "距您"+str(a[0][tt1]) + "km)" + ":\n"+\
                                "3:  "+"地址为："+str(a[1][tt2]['address'])+"\n"+ "确诊病例共计:"+str(a[1][tt2]['count'])+"位"+"(" + "距您"+str(a[0][tt2]) + "km)" + ":\n"+"其他患者信息未公开" ":\n" +"谢哥提醒你：勤洗手，戴口罩！ 不带你试试，试试就逝世！"

                    #             # print(returnmsg)
                    #             repeat =0
                    #             if message.get('data', {}).get('msgfromid', ''):
                    #                 chatroom_wxid = message.get('data', {}).get('msgfromid', '')
                    # print(a[1][0]['province'])

                    # for i in a[1]:
                    #     # print(i)
                    #     # print(dentist_city[2])
                    #     if i['province'] == dentist_city[2]+'市':
                    #         # print(i)
                    #         if 'longitude' in i.keys():
                    #             # print("nihaoa")
                    #             smallest_distance = smallest_people(a[0])
                    #             # print(smallest_distance)
                    #             # print(smallest_distance[0])
                    #             # print(a[0])
                    #             tt0 = smallest_distance[0]
                    #             tt1 = smallest_distance[1]
                    #             tt2 = smallest_distance[2]
                    #             # print('*'*50)
                    #             # print(a[1])
                    #             # print(a[1][tt0])
                    #
                    #             returnmsg = "附近的疫情小区离你最近的前三个分别为"+":\n"+"地址是"+str(a[1][tt0])+"("+str(a[0][tt0])+"km)"+":\n"+"地址是"+str(a[1][tt1])+"("+str(a[0][tt1])+"km)"+":\n"+"地址是"+str(a[1][tt2])+"("+str(a[0][tt2])+"km)"
                    #             # print(returnmsg)
                    #             repeat =0
                    #             if message.get('data', {}).get('msgfromid', ''):
                    #                 chatroom_wxid = message.get('data', {}).get('msgfromid', '')
                # 在这里设置回复内容
                if msgflag == 0:
                    wx_inst.send_text(chatroom_wxid, returnmsg)
                else:
                    wx_inst.send_text(to_user=wx_id, msg=returnmsg)
                time.sleep(1)



                        # elif i.has_key('city') and i['city']==dentist_city[2]:
                        #     returnnmsg = "当前" + dentist_city[2] + ":\n" + "数据未完全公布或不完整谢哥无能为力，总患病人数为" + \
                        #                  a[i][0]['count'] + "\n" + "数据最后更新时间：" + str(
                        #         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))
                            # print(returnnmsg)

                            # i.append(city_single)

                    # for i in city_single:
                    #     returnnmsg = "当前"+city_single[0]['city']+":\n"+"数据未完全公布或不完整谢哥无能为力，总患病人数为"+city_single[0]['count'] + "\n" + "数据最后更新时间：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))
                    #     # print(returnnmsg)
                    # else:
                    #     returnnmsg = "当前"+city_single[0]['city']+":\n"+"数据未完全公布或不完整谢哥无能为力，总患病人数为"+city_single[0]['count'] + "\n" + "数据最后更新时间：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))

                        # pass
                        # returnmessage = city_
                        # str(area) + ":\n" + "确诊人数：" + str(confirmedCount) + "\n" +\
                        #                 "治愈人数：" + str(curedCount) + "\n" + "死亡人数：" +\

                        #                 str(deadCount) + "\n" + "数据最后更新时间：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updateTime)))
                        # if msgflag == 0:
                        #     print("abababa")
                        #     print(returnnmsg)
                        #     wx_inst.send_text(chatroom_wxid, returnnmsg)
                        # else:
                        #     wx_inst.send_text(to_user=wx_id, msg=returnnmsg)
                        #     print("cdcdcdc")
                        # time.sleep(1)

            else:
                print('等式不成立')
            # except:
            #     if msgflag == 0:
            #         wx_inst.send_text(chatroom_wxid, "数据更新中，稍后再试")
            #     else:
            #         wx_inst.send_text(to_user=wx_id, msg="数据库更新中，稍后再试")
            #     time.sleep(1)



def apidata(wx_inst):
    # global timer1
    try:
        r = requests.get(url).json()
        f = open('APIDATA.txt', 'w')
        f.write(str(r))
        f.close()
        print("API数据刷新成功")
    except:
        print("API异常")


def virusnews(wx_inst):
    # global timer2
    try:
        # 读取API数据
        f = open('APIDATA.txt', 'r')
        r_read = f.read()
        r = eval(r_read)
        f.close()

        idList = friendsList()
        time.sleep(5)

        newslist = virus.news(r)
        if(newslist!=[]):
            print("检测到新新闻\n--------------------")
            returnmsg = ""
            for x in newslist:
                returnmsg = returnmsg + x['title'] + '\n' + x['sourceUrl'] + '\n\n'

            print(returnmsg)

            # 读取群和好友列表


            for x in idList:
                time.sleep(3)
                if idList[x] == 0:
                    wx_inst.send_text(x, returnmsg)
                if idList[x] == 1:
                    wx_inst.send_text(to_user=x, msg=returnmsg)

            # wx_inst.send_text('31848182176@chatroom', returnmsg)
            # wx_inst.send_text('1030099185@chatroom', returnmsg)
    except:
        print("API异常")

def spider_daily_news(wx_inst):

    a = news_put()

    idList =friendsList()
    for x in idList:
        time.sleep(3)

        if idList[x] == 0:
            print('ttt')
            wx_inst.send_text(x, a)
        if idList[x] == 1:
            print('tttt')
            wx_inst.send_text(to_user=x, msg=a)



def main():
    global have_sended
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print(wx_inst.get_myself())
    apidata(wx_inst)

    # 获取id
    # wx_inst.update_frinds()


    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()

    wx_inst.send_text(to_user='filehelper', msg='777888999')

    while True:
        apidata(wx_inst)


        # 开启自动新闻播报可能会导致帐号被封，谨慎开启
        wx_inst.update_frinds()

        if int(datetime.datetime.now().hour) == 8 and int(datetime.datetime.now().minute) == 30 :
            print('41')

            spider_daily_news(wx_inst)
            time.sleep(600)

        elif 10<int(datetime.datetime.now().hour)<14:
            apidata(wx_inst)
            virusnews(wx_inst)

            time.sleep(600)
        time.sleep(5)




    #
    # wx_inst.send_link_card(
    #     to_user='filehelper',
    #     title='博客',
    #     desc='我的博客，红领巾技术分享网站',
    #     target_url='http://www.honglingjin.online/',
    #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # )
    # time.sleep(1)
    #
    # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # time.sleep(1)
    #
    # wx_inst.send_file(to_user='filehelper', file_abspath=r'C:\Users\Leon\Desktop\1.txt')
    # time.sleep(1)
    #
    # wx_inst.send_gif(to_user='filehelper', gif_abspath=r'C:\Users\Leon\Desktop\08.gif')
    # time.sleep(1)
    #
    # wx_inst.send_card(to_user='filehelper', wx_id='gh_6ced1cafca19')

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
    # wx_inst.get_member_of_chatroom('22941059407@chatroom')

    # 新增@群里的某人的功能
    # wx_inst.send_text(to_user='22941059407@chatroom', msg='test for at someone', at_someone='wxid_6ij99jtd6s4722')

    # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的回调返回
    # wx_inst.update_frinds()


if __name__ == '__main__':
    main()
