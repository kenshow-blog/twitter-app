import sys
sys.path.append('../')
import config
import tweepy

# TweepyAPI KEY
CK = config.CK
CS = config.CS
AT = config.AT
AS = config.AS

#tweepyの設定
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

#フォローしているアカウント
friends = api.friends_ids()

#2020年9月20日以降ツイートしていないのを使われていないと判断する
#ユーザーオブジェクトには最新ツイートが入る
i = 0
for friend in reversed(friends):
    info = api.get_user(user_id=friend)
    info_json = info._json
    #ツイートされている場合,statusキーが存在する
    if 'status' in info_json.keys():
        tweet_id = info_json['status']['id']
        created_at = info_json['status']['created_at']

    else:#そもそもツイートしていないstatusは飛ばす実装
        continue

    #例 Fri Feb 21 01:41:37 +0000 2020 みたいな形で空白が間に入って日時の情報が入っている状態
    date = created_at.split(' ')
    if int(date[5]) <= 2020 and int(date[2]) <= 20 and date[1] == 'Sep':
        print(info_json['screen_name'])
        api.destroy_friendship(screen_name=info_json['screen_name'])
    i += 1
    if i >= 100:
        break
