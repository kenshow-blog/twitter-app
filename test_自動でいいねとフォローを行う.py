# -*- coding: utf-8 -*-

import codecs  # これによってテキストファイルに落とし込んでくれる
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import pandas as pd
import os
import tweepy
import config
import sys
sys.path.append('../')


def main():
    # tweetidの取得方法はその人のツイート画面にいって上にstatusの次に出てくる数字の羅列を持ってくれば良い
    # def auth():
    CK = config.CK
    CS = config.CS
    AT = config.AT
    AS = config.AS
    # 認証
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    # レートリミットを確認しながら取得処理を行う
    api = tweepy.API(auth)

    # リストから１件ずつ検索キーワードを取り出し、それぞれのキーワードで順次,検索を実行する
    q_list = ['#駆け出しエンジニアと繋がりたい', '#プログラミング初心者', '#今日の積み上げ', '#英語']
    # q_list = ['#新卒', '#22卒']

    # 取得する件数
    count = 30
    for q in q_list:
        results = api.search(q=q, count=count)
        for result in results:
            # 検索結果のツイートIDをセット
            tweet_id = result.id
            # 検索結果のツイートを行ったユーザーのidを取得
            user_id = result.user._json['id']
            try:
                # いいねする

                api.create_favorite(tweet_id)
                print('いいねしました')
                # 下記の実装が自動フォローをする
                # api.create_friendship(user_id)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
# def display_ps():
#     main()

# scheduler = BlockingScheduler()

# #スケジュールにジョブを設定
# scheduler.add_job(
#     main, 'interval', minutes=2
# )
# #スケジュール開始
# try:
#     scheduler.start()
# except KeyboardInterrupt:
#     pass


# 上記のように定義することで他のファイルでこのファイルをimportとしたと同時に上の関数が実行されるのを防ぐことができる。
