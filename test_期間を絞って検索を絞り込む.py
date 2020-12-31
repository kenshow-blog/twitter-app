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

#検索用文字列(リツイートは除外する)
s = 'python'
searchStr = s + ' exclude:retweets'

#過去1週間分のツイートしか取得できない
since = '2020-10-27_00:00:00_JST'
until = '2020-10-27_23:59:59_JST'

#この日付以降のツイートを取得する
sinceDate = since
#この日付以前のツイートを取得する
untilDate = until

tweets = tweepy.Cursor(api.search, q = searchStr,
                        include_entities = True,
                        tweet_mode = 'extended',
                        since = sinceDate,
                        until = untilDate,
                        lang = 'ja').items()
# print(tweets)

for tweet in tweets:
    print('-'*30)
    # print('aaa')
    print('ツイートID : ',tweet.id)
    print('スクリーンネーム : ',tweet.user.screen_name)
    print('ツイートID : ',tweet.created_at)
    print(tweet.full_text)
    print('いいねの数 : ',tweet.favorite_count)
    print('リツイート数 : ',tweet.retweet_count)
