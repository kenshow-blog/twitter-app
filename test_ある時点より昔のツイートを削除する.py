# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
import config
import tweepy
import os
import random

import pandas as pd

import urllib.request

import codecs#これによってテキストファイルに落とし込んでくれる
from datetime import datetime
import time

import json

#tweetidの取得方法はその人のツイート画面にいって上にstatusの次に出てくる数字の羅列を持ってくれば良い
# def auth():
CK = config.CK
CS = config.CS
AT = config.AT
AS = config.AS
#認証
auth = tweepy.OAuthHandler(CK,CS)
auth.set_access_token(AT,AS)
#レートリミットを確認しながら取得処理を行う
api = tweepy.API(auth)



#Twitterには過去のデータをダウンロードできる場所があるからそこからデータを抜き取って削除命令をするアルゴリズムを実装する
with open('twitterデータからダウンロードしたjsファイル',encoding='utf_8') as f:
    data = f.read()
tw = json.loads(data[data.find('['):])

for i, t in enumerate(tw,start=1):
    print(str(i))
    print(t['tweet']['id_str'])
# これで過去のツイートが読み込まれたことが確認できる

j=0
for i, t in enumerate(tw,start=1):
    #2018年4月1日以前のツイートを消したい場合
    if datetime.timestamp(datetime(2018, 4, 1, 0, 0, 0)) > ((int(t['tweet']['id'] >> 22) + 1288834974657)/1000):
        try:
            api.destroy_status(int(t['tweet']['id']))
            print(int(t['tweet']['id']))
            j = j + 1
        except:
            pass
print('全ツイート数:' + str(i))
print('削除対象ツイート数:' + str(j))
            



