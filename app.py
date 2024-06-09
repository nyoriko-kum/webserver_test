from datetime import datetime
from flask import Flask, request, session, jsonify
import pytz
import random

app = Flask(__name__)
#session管理に暗号化をしているが、データ整合性を保つための鍵
app.secret_key ="noriko_kuma" 

# ユーザー名とパスワードのデータベースを仮定
users = {
    'admin': 'password',
    'user1': 'pass123'
}

#login機能
@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
#取得したJSONデータから、キーが'username'と'password'に対応する値を取り出して、それぞれの変数usernameとpasswordに代入しています。
    username = data['username']
    password = data['password']

#if b in a_listでa_listにbが含まれていた場合にTrueを返すかつusersリストのusername のもう一つのキーをだしてくる
#この場合usersリストに取得したusernameがあった場合にそのペアになっているキーを取得したpasswordの値と照合してあっているか確認している
    if username in users and users[username] == password:
        return jsonify({'message':'login successful'})
    else:
        return jsonify({'message':'sorry! login failed'})

# コマンド：content-typeをつけないとはじかれます。curl -X POST -H "Content-Type: application/json" -d '{"username": "user12", "password":"pass123"}' http://localhost:5000/login

#login 解答例======================================================================================

@app.route('/loginkaitou', methods=['POST'])
def login_message():
    """
    コマンド例: curl -X POST -d
    '{"username": "hoge", "password": "123456"}'
    http://localhost:5000/loginkaitou
    """
    #force = Trueにしておくと、Content-Typeに関係なくJSONとして扱ってくれます
    req = request.get_json(force=True)
    #reqに格納したJSONデータのkeyがusernameのものをusernameに格納、passwordをpasswordに格納
    username = req.get('username', None)
    password = req.get('password', None)
    return f'username..."{username}"とpassword..."{password}"を登録しました。'

#==================================================================================================



@app.route('/', methods=['GET'])
def hello():
    return 'No music No Life'

#以降の記述は、自分が作成した記述です。==============================================================
def tz():
    tz = datetime.now(pytz.timezone('Asia/Tokyo'))
    return tz

def calcurate():
    result = 1 + 20
    return result

@app.route('/time', methods=['GET'])
def change_json():
    from flask import jsonify
    result = calcurate()
    t = tz()
    return jsonify(result,t)

#===================================================================================================
#解答例からひっぱってきたやつ↓
@app.route('/test', methods=['GET'])
def current_time():
    dt_now = datetime.now(pytz.timezone('Asia/Tokyo'))
    date = dt_now.strftime('%Y年%m月%d日  %H時%M分%S秒')
    return f'現在時刻は{date}です'

#入力した日付から曜日を算出するやつ===================================================================
@app.route('/date', methods=['GET'])
def input_date():
    input_days = request.args.get('days')
    days_date = datetime.strptime(input_days, "%Y/%m/%d")
    week_list = ["月曜日","火曜日","水曜日","木曜日","金曜日","日曜日"]
    A = days_date.weekday()
    B = week_list[A]
    return f'その日は: {B}'

#ここから自分の記述↓偉人の名言をだしてくるやつ========================================================

@app.route('/aphorism')
def meigen():
    meigen_list = ["千里の道も一歩から","俺とおまえは意見が違うからお互いに存在価値があるんだ。","愛情は瞬間的な感情ではない.","一番幸せなのは、幸福なんて特別必要でないと悟ることだ","自分で選んだ道を誇りに思いたい．だから努力するんだ","忙しいことを理由にして，やりたいことを放棄しない","我々の人生は我々の後にも前にも、側にもなく、我々の中にある","固く握りしめた拳とは手をつなげない"]
    num = random.randint(0,len(meigen_list)-1)
    meigen = meigen_list[num]
    return f'{num}:\n{meigen}'

#こちらはおみくじ
@app.route('/fortune')
def omikuji():
    omikuji_list = ["大吉","小吉","中吉","大凶","凶","吉","これはめったにでない大大吉"]
    num = random.randint(0,len(omikuji_list)-1)
    omikuji = omikuji_list[num]
    return f'{omikuji}'

#こちらは、ねぎらいの言葉をかけるAPI
@app.route('/message')
def negirai():
    word_list = ["君はとてもがんばっているよ","君ほどの努力家はいないさ","家事に仕事に毎日お疲れさまです","あなたががんばっていることは、みんなわかっているよ","今日もたくさんがんばったね","そのがんばりがこれからの希望になっているよ","一日着実にすすんでいるね！"]
    selecter = random.randint(0,len(word_list)-1)
    word_today = word_list[selecter]
    return f'{word_today}'



#**********************************************************************************************
#itsdangerous moduleの検証とsecret_Keyを使用した署名のテスト
@app.route('/testkey')
def testkey():
    from itsdangerous import TimestampSigner, BadSignature

    secret_key = "nonon"
    
    #TimestampSignerオブジェクトを作成
    signer = TimestampSigner(secret_key)
    
    #データに署名を付与
    data = "Hello, World!"
    signed_data = signer.sign(data)

    try:
        # 署名の検証
        original_data = signer.unsign(signed_data)
        return f'{original_data}'
    except BadSignature:
        return 'Signature verification failed'

#***********************************************************************************************



if __name__ == "__main__":
    app.run()

