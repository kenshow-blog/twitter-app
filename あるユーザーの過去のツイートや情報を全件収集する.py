# -*- coding: utf-8 -*-

import codecs  # これによってテキストファイルに落とし込んでくれる
import urllib.request
import subprocess
import time
from datetime import datetime
import os
import tweepy
import config
import sys
sys.path.append('../')


CK = config.CK
CS = config.CS
AT = config.AT
AS = config.AS

# 認証
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
# レートリミットを確認しながら取得処理を行う
api = tweepy.API(auth)

# 情報を取得したいユーザーのスクリーンネームを設定
screen_name = ''

# 保存先フォルダのパスを指定
SAVE_FILE_PATH = ''

# 保存するフォルダお名前
foldername = SAVE_FILE_PATH + '/image_{}'.format(screen_name)

# 保存するフォルダが存在していないのにあああい作成
if not os.path.exists(foldername):
    os.makedirs(foldername)

dt_now = datetime.now()
DT_NOW_STR = dt_now.strftime('%Y-%m-%d-%H-%M-%S')


# タイムラインから最新のツイート一件を取得する関数
def getTL():
    global req, timeline, content
    # count=1は固定する
    # count=1は固定する
    req = (api.user_timeline(screen_name=screen_name, count=1, tweet_mode='extended', include_entities=True,
                             exclude_replies=True, include_rts=False))  # 1件だけなのでcountは1

    try:
        timeline = req[0]
        content = timeline._json
    # ユーザがリプライを連続で行った場合、exclude_replies=True に設定した場合,
    # timelineがnull値になり、一件取得できない場合がある.
    # そのため、例外処理で6分まって、再度、タイムラインを取得するようにしている
    # 6ふんは任意に調整か
    except:
        print('waiting.....')
        time.sleep(360)
        getTL()

# タイムラインの最新の１件からツイートの内容を取得して保存する


def getContents():

    f = codecs.open(
        '{}/tweets[{}]_{}.txt'.format(SAVE_FILE_PATH, screen_name, DT_NOW_STR), 'a', 'utf-8')
    f.write('-'*30)
    f.write('¥n')
    f.write(content['created_at'])
    f.write('¥n')
    f.write(content['full_text'])
    f.write('¥n')

    # extended_entitiesがある→画像か動画付きツイート
    if 'extended_entities' in content:
        content_check = content['extended_entities']['media'][0]

        # 動画保存
        if 'video_info' in content_check:
            f.write('video')
            f.write('¥n')

            # 辞書型定義
            dic_video_info = {}

            for bitrate_check in content['extended_entities']['media'][0]['video_info']['variants']:
                if 'bitrate' in bitrate_check:
                    key = bitrate_check['bitrate']
                    value = bitrate_check['url']
                    dic_video_info.setdefault(key, value)
            # keyの値が最大になるvalue(url)をセット
            max_key = max(dic_video_info.items(), key=lambda x: x[0])[0]
            video_url = dic_video_info[max_key]
            f.write(str(max_key))
            f.write('¥n')
            f.write(video_url)
            f.write('¥n')
            filename = ''
            filename = (foldername + '/[' + str(content['user']['screen_name']) + ']_' +
                        str(content['created_at'].replace('+0000', '').replace(' ', '-').replace(':', '-')) + '.mp4')

            try:
                urllib.request.urlretrieve(video_url, filename)
            except:
                print('error')
                print('動画が保存されまされませんでした')
                f.write('動画が保存されませんでした')
                f.write('¥n')

        else:
            for i, photo in enumerate(content['extended_entities']['media']):
                filename = ""
                filename = (foldername + "/[" + str(content['user']['screen_name']) + "]_" +
                            content['id_str'] + "_" + str(i) + "_" +
                            str(content['created_at'].replace(" +0000", "").replace(" ", "-").replace(":", "-")))

                if ".jpg" in photo['media_url']:
                    image_url = photo['media_url'][:-4] + \
                        "?format=jpg&name=orig"
                    # 保存ファイル名
                    filename = filename + "_orig.jpg"
                elif ".png" in photo['media_url']:
                    image_url = photo['media_url'][:-4] + \
                        "?format=png&name=orig"
                    # 保存ファイル名
                    filename = filename + "_orig.png"
                else:
                    image_url = photo['media_url']
                    filename = filename
                f.write(image_url)
                f.write('¥n')
                try:
                    urllib.request.urlretrieve(image_url, filename)

                except:
                    print("error")
                    print("保存されませんでした")

    else:
        print("{}¥t画像または動画がツイートに存在しません".format(
            datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
    f.close()


    ###メイン処理####
first = 0
while True:
    try:
        if first == 0:
            getTL()
            getContents()
            oldTwID = req[0]._json['id']
            first += 1
        elif first == 1:
            getTL()
            newTwID = req[0]._json['id']
            if oldTwID != newTwID:
                print('{}¥t更新されました'.format(
                    datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
                first += 1
            elif oldTwID == newTwID:
                print('{}¥t更新されていません'.format(
                    datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
                first = 1
        elif first == 2:
            print('first==2')
            getContents()
            oldTwID = req[0]._json['id']
            first -= 1
        time.sleep(60)
    except:
        print('{}¥tエラーが起きました'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
        # subprocess.run([/xxxxxxxxxxx/xxxxxxxxxx.sh])
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])
        # 再起動（エラーが起きたら再起動)
        #os.execv(sys.executable, os.path.ebspath(__file__))
        sys.exit()
