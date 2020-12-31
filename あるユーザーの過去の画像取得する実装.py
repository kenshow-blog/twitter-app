# -*- coding: utf-8 -*-
import pandas as pd
import xlrd
import time
import datetime
import codecs
import urllib.request
import os
import tweepy
import config
import sys
sys.path.append('../')
# jvhW ody0 4CKD q5ye c8tu c2yi

# API KEY
CK = config.CK
CS = config.CS
AT = config.AT
AS = config.AS

# tweepy setting
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

# レートリミット設定
api = tweepy.API(auth, wait_on_rate_limit=True)

# 取得するスクリーンネームを指定する（@不要）
screen_name = ""

# 指定したツイートIDより新しいツイートを取得する
since_id = ""
if since_id != "":
    try:
        since_id = int(since_id) + 1
    except:
        since_id = 1

# 保存先フォルダ
foldername = "attach"

# 保存先フォルダが存在しない場合は作成する
if not os.path.exists(foldername):
    os.makedirs(foldername)

dt_now = datetime.datetime.now()
DT_NOW_STR = dt_now.strftime('%Y-%m-%d-%H-%M-%S')


if since_id != "":
    search_results = (tweepy.Cursor(api.user_timeline,
                                    screen_name=screen_name,
                                    since_id=since_id,
                                    tweet_mode="extended",
                                    include_entities=True,
                                    exclude_replies=True,
                                    include_rts=False).items())
else:
    search_results = (tweepy.Cursor(api.user_timeline,
                                    screen_name=screen_name,
                                    tweet_mode="extended",
                                    include_entities=True,
                                    exclude_replies=True,
                                    include_rts=False).items())


list_df = (pd.DataFrame(columns=['id_str',
                                 'created_at',
                                 'full_text',
                                 'user_screen_name',
                                 'retweet_count',
                                 'favorite_count'
                                 ]))

attach_df = (pd.DataFrame(columns=['id_str',
                                   'image_url_1',
                                   'image_file_1',
                                   'image_url_2',
                                   'image_file_2',
                                   'image_url_3',
                                   'image_file_3',
                                   'image_url_4',
                                   'image_file_4',
                                   'video_url',
                                   'video_file'
                                   ]))

totalcount = ""

for i, result in enumerate(search_results):

    # JSON形式のデータをcontentに入れる
    content = result._json

    totalcount = i

    tmp_se = (pd.Series([content['id_str'],
                         content['created_at'],
                         content['full_text'],
                         content['user']['screen_name'],
                         content['retweet_count'],
                         content['favorite_count']
                         ], index=list_df.columns))

    list_df = list_df.append(tmp_se, ignore_index=True)

    # 画像または動画を保存

    content['image_url_1'] = ""
    content['image_file_1'] = ""
    content['image_url_2'] = ""
    content['image_file_2'] = ""
    content['image_url_3'] = ""
    content['image_file_3'] = ""
    content['image_url_4'] = ""
    content['image_file_4'] = ""
    content['video_url'] = ""
    content['video_file'] = ""

    if "extended_entities" in content:
        content_check = content["extended_entities"]["media"][0]
        # 動画保存
        if "video_info" in content_check:
            # 辞書型定義
            dic_video_info = {}

            for bitrate_check in content['extended_entities']['media'][0]['video_info']['variants']:
                if "bitrate" in bitrate_check:

                    # 辞書型に加えて、降順にソート
                    key = bitrate_check['bitrate']
                    value = bitrate_check['url']
                    dic_video_info.setdefault(key, value)

            # keyの値が最大になるvalue（url）をセット
            max_key = max(dic_video_info.items(), key=lambda x: x[0])[0]
            video_url = dic_video_info[max_key]

            filename = ""
            filename = (foldername + "/[" + str(content['user']['screen_name']) + "]_" + content['id_str'] + "_" +
                        str(content['created_at'].replace(" +0000", "").replace(" ", "-").replace(":", "-")) + ".mp4")

            # 動画保存処理
            try:
                # video_urlの動画をfilenameという名前で保存
                urllib.request.urlretrieve(video_url, filename)
                ret1 = "video"
                ret2 = video_url
                ret3 = filename
                content['video_url'] = ret2
                content['video_file'] = ret3
            except:
                print("error")
                print("保存されませんでした")
                ret1 = "error"
                ret2 = "error"
                ret3 = "保存されませんでした"
        else:
            # 最大4枚画像を取り出す
            for i, photo in enumerate(content['extended_entities']['media']):
                #image_url_data = []
                #filename_data = []
                filename = ""
                filename = (foldername + "/[" + str(content['user']['screen_name']) + "]_" +
                            content['id_str'] + "_" + str(i) + "_" +
                            str(content['created_at'].replace(" +0000", "").replace(" ", "-").replace(":", "-")))

                if ".jpg" in photo['media_url']:
                    # 画像のurlを取得
                    image_url = photo['media_url'][:-4] + \
                        "?format=jpg&name=orig"
                    print(image_url)
                    # 保存ファイル名
                    filename = filename + "_orig.jpg"

                elif ".png" in photo['media_url']:
                    # 画像のurlを取得
                    image_url = photo['media_url'][:-4] + \
                        "?format=png&name=orig"
                    # print(image_url)
                    # 保存ファイル名
                    filename = filename + "_orig.png"

                else:
                    # 画像のurlを取得
                    image_url = photo['media_url']
                    # print(image_url)
                    # 保存ファイル名
                    filename = filename

                # print(image_url)
                # image_url_data.append(image_url)
                # filename_data.append(filename)

                # 画像保存処理
                try:
                    # image_urlの画像をfilenameという名前で保存
                    urllib.request.urlretrieve(image_url, filename)
                    # print("image")
                    # print(image_url)
                    # print(filename_data)
                    ret1 = "image"
                    ret2 = image_url
                    ret3 = filename
                    if i == 0:
                        content['image_url_1'] = ret2
                    elif i == 1:
                        content['image_url_2'] = ret2
                    elif i == 2:
                        content['image_url_3'] = ret2
                    elif i == 3:
                        content['image_url_4'] = ret2

                    if i == 0:
                        content['image_file_1'] = ret3
                    elif i == 1:
                        content['image_file_2'] = ret3
                    elif i == 2:
                        content['image_file_3'] = ret3
                    elif i == 3:
                        content['image_file_4'] = ret3
                except:
                    print("error")
                    print("保存されませんでした")
                    ret1 = "error"
                    ret2 = "error"
                    ret3 = "保存されませんでした"
    else:
        # print("画像または動画がツイートに存在しません")
        ret1 = "nofile"
        ret2 = "nofile"
        ret3 = "画像または動画がツイートに存在しません"

    tmp_se2 = (pd.Series([content['id_str'],
                          content['image_url_1'],
                          content['image_file_1'],
                          content['image_url_2'],
                          content['image_file_2'],
                          content['image_url_3'],
                          content['image_file_3'],
                          content['image_url_4'],
                          content['image_file_4'],
                          content['video_url'],
                          content['video_file']
                          ], index=attach_df.columns))

    attach_df = attach_df.append(tmp_se2, ignore_index=True)

dframe = pd.merge(list_df, attach_df, on='id_str', how='left')
# Excel形式で保存
export_file_name = "{}_{}.xlsx".format(screen_name, DT_NOW_STR)
dframe.to_excel(export_file_name, sheet_name='tweetlist')
# CSVで保存する場合
# export_file_name = "{}_{}.csv".format(screen_name, DT_NOW_STR)
# dframe.to_csv(export_file_name)
