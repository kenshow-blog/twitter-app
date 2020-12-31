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



# あるユーザと相互フォロワーでない場合のアカウントをフォロー解除する
SC_NAME = '検索したユーザー'

#フォロワーとフレンドのIDを取得
followers = api.followers_ids(screen_name=SC_NAME,count=10)
friends = api.friends_ids(screen_name=SC_NAME,count=10)

#フォローを解除する

#フォロ解除数
unfollow_cnt = 0
for friend_id in friends:
    #フレンドがフォロワーにいない(相互フォローではない)
    if friend_id not in followers:
        if unfollow_cnt <= 100:
            api.destroy_friendship(friend_id)
            print('フォローを解除したユーザ： {}'.format(api.get_user(friend_id).screen_name))
            time.sleep(2)
            unfollow_cnt += 1
        else:
            print('フォロー解除数が100人を超えたため　処理停止')
            break

# あるキーワードで検索したユーザを指定の件数フォローする

keyword = 'webエンジニア'

#検索結果取得件数
s_count = 3
follow_cnt = 0
results = api.search(q=keyword, count=s_count)

for result in results:
    #フォロー数が検索結果取得件数以下の場合にフォローする
    if follow_cnt <= s_count:
        #検索結果で取得したツイートをしたユーザのスクリーンネームをセットし、フォローする
        screen_name = result.user._json['screen_name']
        api.create_friendship(screen_name)
        print('フォローしたユーザ: {}'.format(screen_name))
        time.sleep(2)
        follow_cnt += 1
    else:
        print('フォローした数が3人を超えた為処理停止')
        break



