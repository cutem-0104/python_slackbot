# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import urllib.request
import json

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#
#                           文字列中に':'はいらない
default_reply_count = 0
def_word = 'デフォルトの返事です'


@default_reply()
def default_func(message):
    global default_reply_count
    default_reply_count += 1
    message.reply('%d 回目のデフォルトの返事です' % default_reply_count)

    text = message.body['text']     # メッセージを取り出す
    # 送信メッセージを作る。改行やトリプルバッククォートで囲む表現も可能
    msg = 'あなたの送ったメッセージは\n```' + text + '```'
    message.reply(msg)      # メンション
    message.reply(def_word)


@respond_to('メンション')
def mention_func(message):
    message.reply('で？')


@respond_to('がんばれ')
def mention_func(message):
    message.reply('わかった')
    message.react('+1')


@respond_to(r'^ping\s+\d+\.\d+\.\d+\.\d+\s*$')
def ping_func(message):
    message.reply('それはpingのコマンドですね。実行できませんが')   # メンション


@respond_to(r'^set\s+\S.*')
def set_default_func(message):
    text = message.body['text']     # メッセージを取り出す
    temp, word = text.split(None, 1)    # 設定する言葉を取り出す。tempには'set'が入る
    global def_word     # 外で定義した変数の値を変えられるようにする
    def_word = word     # デフォルトの返事を上書きする
    msg = 'デフォルトの返事を以下のように変更しました。\n```' + word + '```'
    message.reply(msg)


@listen_to('リッスン')
def listen_func(message):
    message.send('リッスンだってさ')
    message.reply('おまえか')


@respond_to('天気')
def get_weather(message):
    message.send('りょうかい〜')
    citycode = "130010"
    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city={}".format(citycode)
    response = urllib.request.urlopen(url)

    data = response.read()
    resp = json.loads(data.decode())

    title = resp['title']
    text = resp['description']['text']

    for f in resp['forecasts']:
        label = f['dateLabel']
        telop = f['telop']
        try:
            min_temp = f['temperature']['min']['celsius']
        except TypeError:
            min_temp = "わからん"
        try:
            max_temp = f['temperature']['max']['celsius']
        except TypeError:
            max_temp = "わからん"

        message.send("{} の天気は {} 最低気温は {}, 最高気温は {} です。".format(label, telop, min_temp, max_temp))
