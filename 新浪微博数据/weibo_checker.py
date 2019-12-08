# -*- coding: utf-8 -*-

import urllib.request
import json
#from pymongo import MongoClient
import pandas as pd

import json
import os.path
import sys
import urllib
import time
import numpy as np





id = '1761179351'
MONGO_HOST = 'mongodb://localhost:27017/weibo_database'  # mongodb host path

proxy_addr = "183.129.207.82:11031"
fakeList =[]
df1 = pd.DataFrame(columns=['id', 'name', 'profile_image_url','description','profile_url','verified','guanzhu','fensi','gender','urank','isAnomaly'])


def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header(
        "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return data


def get_containerid(url):
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type') == 'weibo'):
            containerid = data.get('containerid')
    return containerid

df1 = pd.DataFrame(
            columns=['id', 'name', 'profile_image_url', 'description', 'profile_url', 'verified', 'guanzhu', 'name',
                     'fensi', 'gender', 'urank','statusesCount','followersCount','followCount', 'isAnomaly'],index=np.arange(100000))
def get_userInfo(id,indexcount):
    global df1
    try:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        profile_image_url = content.get('userInfo').get('profile_image_url')
        description = content.get('userInfo').get('description')
        profile_url = content.get('userInfo').get('profile_url')
        verified = content.get('userInfo').get('verified')
        guanzhu = content.get('userInfo').get('follow_count')
        name = content.get('userInfo').get('screen_name')
        fensi = content.get('userInfo').get('followers_count')
        gender = content.get('userInfo').get('gender')
        urank = content.get('userInfo').get('urank')
        statusesCount = content.get('userInfo').get('statuses_count')
        followersCount = content.get('userInfo').get('followers_count')
        followCount = content.get('userInfo').get('follow_count')

        print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n" +
              "微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")
        df1.iloc[indexcount] = {'id':id,'name':name,'profile_image_url':profile_image_url, 'description':description, 'profile_url':profile_url, 'verified':verified, 'guanzhu':guanzhu, 'name':name,
                     'fensi':fensi, 'gender':gender, 'urank':urank,'statusesCount':statusesCount,'followersCount':followersCount,'followCount':followCount, 'isAnomaly':0}

       # a = [id, name, profile_url, description, profile_url, str(verified), str(guanzhu), str(fensi), str(gender), str(
       #      urank), str(0)]
       # df1.append(a)
    except :
        print(id +"，Fake")
        df1.iloc[indexcount] ={'id': id, 'isAnomaly':1}

       # a=[id, "", "", "", "", str(""), str(""), str(""),str(""), str(""), str(1)]
        #df1.append(a)
        fakeList.append(id)
    return df1


# 获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等

def get_weibo_store(id, file):
    i = 1
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
            id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data = use_proxy(weibo_url, proxy_addr)
            print(data)
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if(len(cards) > 0):

                for j in range(len(cards)):

                    card_type = cards[j].get('card_type')
                    if(card_type == 9):
                        mblog = cards[j].get('mblog')
                        attitudes_count = mblog.get('attitudes_count')
                        comments_count = mblog.get('comments_count')
                        created_at = mblog.get('created_at')
                        reposts_count = mblog.get('reposts_count')
                        scheme = cards[j].get('scheme')
                        text = mblog.get('text')
                        with open(file, 'a', encoding='utf-8') as fh:
                            fh.write("----第"+str(i)+"页，第" +
                                     str(j)+"条微博----"+"\n")
                            fh.write("微博地址："+str(scheme)+"\n"+"发布时间："+str(created_at)+"\n"+"微博内容："+text+"\n"+"点赞数："+str(
                                attitudes_count)+"\n"+"评论数："+str(comments_count)+"\n"+"转发数："+str(reposts_count)+"\n")

                client = MongoClient(MONGO_HOST)  # connect mongodb
                db = client.weibo_database  # create db
                data_json = json.loads(data)  # Decode the JSON from Twitter
                # insert the data into the mongodb into a collection
                db.chongbin_collection.insert(data_json)
                i += 1
            else:
                break
        except Exception as e:
            print(e)
            pass
def read_file(path):
    with open(path, "r",encoding='ISO-8859-1') as f:
        for line in f:
            yield line


def batch_url_extractor(input_path, output_path):

    #csv_data = pd.read_csv(input_path)

    f = read_file(input_path)
    for line_count, link in enumerate(f):
        if line_count== 0:
            continue
        if line_count == 100000:
            break
        if line_count % 1000 ==0:
            time.sleep(30)
        user_id = link.split(',')[0]
        print('当前用户:' + user_id)
        get_userInfo(user_id,line_count)
        time.sleep(3)
    df1.to_csv('./result_all_nodes2.csv',encoding='utf_8_sig')


#get_userInfo('1402869242')
#exit(0)
if __name__ == '__main__':
    print("start")
    #

    batch_url_extractor("./all_nodes.csv", "fake_users.txt")
    exit(0)
    a = ['1041514813', '1372391882', '1465128481', '1576229144', '1705145357', '1752629790', '1757645411', '1816532795',
     '1830577063', '1838436697', '1876464221', '1908062085', '2064748387', '2128884541', '2346769694', '2425320194',
     '2459502185', '2617986623', '2641042505', '2643768800', '2696382082', '2766467333', '2768946311', '2784654125',
     '2786535687', '2833621377', '2891854953', '2899097081', '2998850183', '3031805374', '3072569041', '3073160087',
     '3087243885', '3089819133', '3118752457', '3147297283', '3152303751', '3152783674', '3175664544', '3184028954',
     '3225497724', '3254093841', '3254927351', '3307709485', '3308159265', '3317338860', '3391721524', '3427028600',
     '3429995494', '3508559184', '3591311671', '3723075335', '3723075914', '3723357835', '3764369327', '3817099196',
     '3914156316', '3972850415', '3973480557', '3975927245', '3978461117', '3978521513', '3978629730', '3983687100',
     '5035125768', '5043577095', '5063358893', '5071097702', '5087718785', '5103613401', '5118722930', '5135642220',
     '5138811486', '5151182890', '5161194256', '5208835275', '5212384562', '5237121924', '5245379166', '5291696737',
     '5293544530', '5305021616', '5322066783', '5323263294', '5324797585', '5325912225', '5326477957', '5328854844',
     '5331917298', '5331950652', '5332084382', '5335242471', '5361261043', '5365515981', '5365519449']

    for item in a:
        time.sleep(3)
        get_userInfo(item)
    # if len(sys.argv) == 3:
    # batch_url_extractor(sys.argv[2], sys.argv[3], 0)
    # else:
    #     print "Error: Please enter 2 parameters"
    """
    if len(sys.argv) == 4:
        if sys.argv[1] == "facebook":
            batch_share_extractor(get_url_share_count, sys.argv[2], sys.argv[3], 3)
        elif sys.argv[1] == "twitter":
            batch_share_extractor(get_url_twitt_count, sys.argv[2], sys.argv[3], 3)
    else:
        print "Error: Please enter 3 parameters"
    """
    print("finished")
    print(fakeList)
    sys.exit(1)
