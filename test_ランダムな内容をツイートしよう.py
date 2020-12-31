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
import datetime
import time


CK = config.CK
CS = config.CS
AT = config.AT
AS = config.AS
#認証
auth = tweepy.OAuthHandler(CK,CS)
auth.set_access_token(AT,AS)
#レートリミットを確認しながら取得処理を行う
api = tweepy.API(auth)


dframe = pd.read_excel('読み込みたいエクセル.xlsx', index_col=0)
# index_colで指定した数字の行を無視する（ただし0だったら一行目が無視されることとなる

r_list = range(1,101)


i = random.randint(0,len(r_list))
#iは行数指定
status = (dframe['指定した列名1'][i] + ' ' + dframe['指定した列名2'][i] + ' ' + dframe['指定した列名3'][i] + '¥n' +
            dframe['指定した列名4'][i] + ' ' + dframe['指定した列名5'][i] + '¥n')
#Twitterに投稿
api.update_status(status=status)