# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
import config
import tweepy
import os

import pandas as pd

import urllib.request

import codecs#これによってテキストファイルに落とし込んでくれる
import datetime
import time


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

#フォローする人数
limit = 30

screen_name = 'フォロワーのID'

#フォロワーのIDをfollowers_idsに格納
followers_ids = api.followers_ids(screen_name=screen_name)

follow_cnt = 0

#フォロワーリストを変数に格納
for followers_id in followers_ids:
    followers = api.get_user(followers_id)

    #フォロワーのフォロワー数が、100を超えてて、かつフォロワーのフレンドの数が、１００を超えた場合,ユーザをフォローする
    #フォロワーのフォロワー数 followers.followers_count
    #フォロワーのフレンド数 followwers.friends_count フォロー数

    if followers.followers_count > 100 and followers.friends_count > 100:
        follow_cnt += 1
        api.create_friendship(followers.id)
        print('フォローした数:' + str(follow_cnt))
    if follow_cnt == limit:
        break