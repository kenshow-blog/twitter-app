これは python のライブラリである「Tweepy」を使った twitter 運用を自動化させてくれるためのアプリケーションです。

使い方：
config.py に TwitterAPI で発行した、
自分の
・API キー
・API シークレットキー
・アクセストークン
・アクセストークンシークレット

を入力してください。

注意：）
画像保存をするためのスクリプトを実装するために
ディレクトリ直下に「attach」フォルダを作成してください。


あとは、適当な python スクリプトを実行するとそのファイルの名前に書かれていることが実装されます。

例：
「test\_自動でいいねとフォローを行う.py」の
中身を自分の都合に合わせて一部情報を変更してから実装することで
自動でいいねとフォローをすることができる
