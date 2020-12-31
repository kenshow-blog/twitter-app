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

screen_name = 'kenshow_study'

#NGワードがあればフォローしない
#フォロワーのアカウントデータを取得
follower_list = api.followers(screen_name=screen_name,count=250)

for follower in follower_list:
    des = follower.description
    if 'ネットビジネス' or '副業' or '100万' or '金儲け' in des:
        api.destroy_friendship(follower.id)
        pass
    else:
        follower_id = follower.id
        api.create_friendship(follower.id)
follower_list = api.followers(screen_name=screen_name,count=50)


#okワードがあればフォローする場合
for follower in follower_list:
    des = follower.description
    if '相互フォロー' or 'フォロバ100%' or '相互アカ' in des:
        follower_id = follower.id
        api.create_friendship(follower.id)
    else:
        pass
