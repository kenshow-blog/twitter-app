import tweepy
import config
import sys
sys.path.append('../')

# TweepyAPI KEY
CK = config.CK
CS = config.CS
AT = config.AT
AS = config.AS

# tweepyの設定
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# twitter_idは大きければ大きいほど最新のものとなる
# since_idは指定したIDより最近のツイート
# max_idは指定したIDおよび指定したIDよりも古いツイート

screen_name = ''

for result in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended', since_id=100000).items(100):
    print('ツイートID : ', result.created_at)
    print(result.full_text)
