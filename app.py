from flask import Flask, render_template, request, send_file
import sqlite3
import pandas as pd
import os


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # アップロードファイルを保存するディレクトリ
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 正しく設定

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 問題、回答のハッシュ
enquirely = {
    "ljalkjsdf": ("エコポイントとはなんですか？", "回答１", "回答2"),
    "klsjklsdf": ("エコな行動は", "水を再利用", "水を捨てる")
}


# ルート画面


@ app.route("/")
def index():
    enquiry_list = [
        {"key": key, "title": value[0]} for key, value in enquirely.items()
        ]
    return render_template("index.html",
                           enquiry_list=enquiry_list,
                           title=enquirely,
                           other_links=[
                            {"url": "/next1", "text": "管理者画面"},
                            {"url": "/next2", "text": "customer共通画面"},
                            {"url": "/next3", "text": "customerスタンプ詳細画面"},
                            {"url": "/table", "text": "テーブル画面"},
                            {"url": "/next4", "text": "アンケート画面"},
                            {"url": "/next5", "text": "クイズ"},
                            ])


# @app.route('/enq/<key>')
@app.route('/next5/<key>')  # <key>をURLパラメータとして受け取る
def enq(key):
    # キーが辞書に存在しない場合のエラーハンドリング
    if key not in enquirely:
        return "指定されたキーは存在しません。", 404

    # キーに基づいて質問と選択肢を取得
    question, option1, option2 = enquirely[key]

    # quiz.htmlテンプレートにデータを渡してレンダリング
    return render_template("quiz.html",
                           key=key,
                           question=question,
                           option1=option1,
                           option2=option2
                           )


# アンケートにアクセスするkeyを使用


@app.route('/enq/<key>', endpoint='enq_key')  # エンドポイント名を変更
def enq_with_key(key):
    # enquirely辞書から指定されたキーの情報を取得
    if key not in enquirely:
        return "指定されたキーは存在しません。", 404  # エラーハンドリング

    # 出力用HTMLの生成
    output = f'''
    <h2>{enquirely[key][0]}</h2>
    <br>
    <form action="/ans/{key}" method="POST">
        <input type="radio" name="answer" value="1">{enquirely[key][1]}<br>
        <input type="radio" name="answer" value="2">{enquirely[key][2]}<br>
        <input type="submit" value="送信">
    </form>
    <br>
    <a href="/">戻る</a>
    '''
    return output


# 回答に関するkeyを使用


@ app.route('/ans/<key>', methods=["POST"])
def ans(key):
    ret = request.form.get("answer")
    answer = enquirely[key][int(ret)] if key in enquirely else ''
    output = f'''
    {enquirely[key][0] if key in enquirely else ''}

回答は、{answer}でした。
<br>
<a href="/">Back</a>
'''
    return output

# ネクストの中身を記述
# 1,管理者メニュー、db操作、db編集


@ app.route('/next1')
def next1():
    output = '''

    <h2>管理者メニュー</h2>
    <form action="/next1/search" method="POST">
        <h3>ユーザー検索</h3>
        名前: <input type="text" name="search_name">
        <input type="submit" value="検索">
    </form>
    <h3>データベース操作</h3>

    <form action="/next1/add" method="post">
        <h4>ユーザー追加</h4>
            新しい名前: <input type="text" name="add_name" required>
            新しいメール: <input type="email" name="add_email">
        <input type="submit" value="追加">
    </form>

    <form action="/next1/edit" method="POST">
        <h4>ユーザー情報編集</h4>
        既存の名前: <input type="text" name="current_name" required>
        新しい名前: <input type="text" name="new_name" required>
        新しいメール: <input type="email" name="new_email">
        <input type="submit" value="更新">
    </form>

    <h3>全ユーザー一覧</h3>
    <div id="user_list">
    '''

#  <! --ユーザー情報編集において、既存メールではなく、既存ユーザー名を検索し、新規ネームと、新規emailを作成する-->

#     <form action="/next1/delete" method="POST"
#    onsubmit="return confirm('本当に削除しますか？');">
#         <h4>ユーザー削除</h4>
#         メール: <input type="text" name="delete_>
#         <input type="submit" value="削除">

    with sqlite3.connect('data.db') as conn:
        df = pd.read_sql_query('SELECT * FROM USER', conn)
        output += df.to_html()

    output += '''
    </div>
    <br>
    <a href="/">トップに戻る</a>
    '''
    return output

# next1/serch内に検索結果を表示する


@ app.route('/next1/search', methods=['POST'])
def search_user():
    search_name = request.form.get('search_name')
    output = '<h2>検索結果</h2>'

    with sqlite3.connect('data.db') as conn:
        df = pd.read_sql(
            'SELECT * FROM USER WHERE name LIKE ?',
            conn,
            params=['%' + search_name + '%']
            )
        output += df.to_html()

    output += '''
    <br>
    <a href="/next1">管理者メニューに戻る</a>
    <br>
    <a href="/">トップに戻る</a>
    '''
    return output

# userを追加するためのコード


@app.route('/next1/add', methods=['POST'])
def add_user():
    #  add_name を取得
    name = request.form.get('add_name')
    # add_email を取得
    email = request.form.get('add_email')

    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO USER (name, email, date) VALUES (?, ?, '
        'datetime("now", "localtime"))',
        (name, email)
    )
    conn.commit()

    return '''
    <h2>ユーザーを追加しました</h2>
    <a href="/next1">管理者メニューに戻る</a>
    <br>
    <a href="/">トップに戻る</a>
    '''

# userを編集するためのコード


@ app.route('/next1/edit', methods=['POST'])
def edit_user():
    current_name = request.form.get('current_name')
    new_name = request.form.get('new_name')
    new_email = request.form.get('new_email')

    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            # 既存ユーザーの確認と現在のメールアドレスの取得
            cursor.execute(
                'SELECT email FROM USER WHERE name = ?',
                [current_name]
                )

            result = cursor.fetchone()

            if not result:
                return '''
                <h2>エラー：指定された名前のユーザーが見つかりません</h2>
                <a href="/next1">管理者メニューに戻る</a>
                '''

            # 新しいメールアドレスが入力されていない場合は既存のものを使用
            current_email = result[0]
            if not new_email:
                new_email = current_email

            # ユーザー情報の更新
            cursor.execute(
                '''
                    UPDATE USER SET name = ?, email = ?,
                    date = datetime("now", "localtime")
                    WHERE name = ?
                ''',
                [new_name, new_email, current_name])
            conn.commit()

        return '''
        <h2>ユーザー情報を更新しました</h2>
        <a href="/next1">管理者メニューに戻る</a>
        <br>
        <a href="/">トップに戻る</a>
        '''

    except sqlite3.Error as e:
        return f'''
        <h2>エラーが発生しました</h2>
        <p>データベースの更新中にエラーが発生しました: {e}</p>
        <a href="/next1">管理者メニューに戻る</a>
        '''

# userを削除するためのコード
# @app.route('/delete', methods=['POST'])
# def delete_route():
#     name = request.form.get('name')  # フォームから名前を取得
#     if name:
#         delete_result = delete_by_name(name)
#         return delete_result
#     else:
#         return "Name parameter is missing."
#     return output


# PDFファイルを提供するための新しいルート
@app.route('/map_ol2.pdf')
def serve_pdf():
    return send_file(
        os.path.join(app.root_path, 'static', 'map_ol2.pdf'),
        as_attachment=True)


# ext2の中身を表示
@app.route('/next2')
def next2():
    output = '''
    <h2>エコスタンプラリーへようこそ！</h2>

    <div class="how-to-play">
        <h3>遊び方</h3>
        <ol>
            <li>街の環境に優しいスポットを訪れる</li>
            <li>各スポットでQRコードを探す</li>
            <li>QRコードを読み取ってスタンプを獲得</li>
            <li>スタンプを集めて景品をゲット！</li>
        </ol>
    </div>

    <div class="map-section">
        <h3>街の地図</h3>
        <p>下のボタンをクリックして地図をダウンロードできます</p>
        <a href="/map_ol2.pdf" target="_blank" class="map-button">
            地図をダウンロード（PDF）

    <style>
        .how-to-play {
            margin: 20px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        .map-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 0;
        }
        .map-button:hover {
            background-color: #45a049;
        }
    </style>

    <br>
    <a href="/">トップページに戻る</a>
    '''
    return output

# next3の中身を表示
# ユーザーIDを受け取るように変更


@ app.route('/next3/<user_id>')
def next3(user_id):

    with sqlite3.connect('data.db') as conn:
        # スタンプ情報を取得
        cursor = conn.cursor()
        cursor.execute(
            '''
                SELECT location, quiz_key, acquired
                FROM stamps
            '''
        )
        # WHERE user_id=? , (user_id,))  # 必要に応じてユーザーIDで絞り込み
        stamps = cursor.fetchall()

        # クイズ情報を取得 (必要に応じて)
        quiz_info = {}
        for stamp in stamps:
            if stamp[1]:
                # quiz_key が存在する場合のみ
                quiz_info[stamp[0]] = enquirely.get(stamp[1])
                # 地点名をキーにクイズ情報を格納

    return render_template(
        'next3.html', stamps=stamps, quiz_info=quiz_info, user_id=user_id
        )
# カスタマー用の現在のスタンプの獲得情報や、スタンプカードインデックスに使用

# 全tableを表示


@ app.route("/table")
def table():
    enquiry_list = [
        {"key": key, "title": value[0]} for key, value in enquirely.items()
        ]
    return render_template("table.html",
                           enquiry_list=enquiry_list,
                           all_table=enquirely,
                           other_links=[
                            {"url": "/user_t", "text": "userテーブル"},
                            {"url": "/quiz_t", "text": "クイズテーブル"},
                            {"url": "/survey_t", "text": "アンケートテーブル"},
                            ])


@ app.route('/table')
def user_t():
    output = '''
    <h3>全ユーザー一覧</h3>
    
    '''

#<div id="user_list">
# @ app.route('/table')
# def table():
#     output = '''
#     <table>
#         <thead>
#             <tr>
#                 <th>ID</th>
#                 <th>名前</th>
#                 <th>登録日時</th>
#             </tr>
#         </thead>
#         <tbody>
#     '''

#     with sqlite3.connect('data.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM USER')
#         users = cursor.fetchall()

#         for user in users:
#             output += f'''
#             <tr>
#                 <td>{user[0]}</td>
#                 <td>{user[1]}</td>
#                 <td>{user[2]}</td>
#             </tr>
#             '''

#     output += '''
#         </tbody>
#     </table>
#         <br>
#     <a href="/">トップページに戻る</a>
#     '''

#     return output


# def table():
#     try:
#         output = ""  # 初期化

#         with sqlite3.connect('USER_TEMP.db') as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#         CREATE TABLE IF NOT EXISTS USER_TEMP (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             email TEXT,
#             date TEXT
#         )
#     ''')

#         conn.commit()

#         return output
    # 以前のコードでtryの外に出したreturn文

    # except sqlite3.Error as e:
    #     print(f"データベースエラー: {e}")
    #     return f"データベースエラー: {e}", 500
    # except内でもreturnする
    # with sqlite3.connect('USER_TEMP.db') as conn:
    #     df = pd.read_sql_query('name TEXT,email TEXT,date NUM', conn)
    #     output += df.to_html()

    # with sqlite3.connect('aaa_stamps.db') as conn:
    #     df = pd.read_sql_query('SELECT * FROM stamps', conn)
    #     output += df.to_html()

    # output += '''<br>Next1<br><a href="/">Back</a>'''
    # return output

    # except sqlite3.Error as e:
    #     print(f"データベースエラー: {e}")
    #     return f"データベースエラー: {e}", 500

# アンケートに関する記述？


# @ app.route('/next4/surver')
# def table(survey):


# @app.route("/next4")
# def survey_a():
#     return render_template("survey.html")


@app.route('/user/<int:id>')
def user(id):
    output = ''

    with sqlite3.connect('data.db')as conn:
        df = pd.read_sql(
            'SELECT * FROM USER WHERE id=?', conn, params=[id]
            )
        output = df.to_html()
    output += '''
<br>Next1
<br>
<a href="/">Back</a>
'''
    return output

# アンケート画面


@ app.route("/next4")
def survey():
    enquiry_list = [
        {"key": key, "survey": value[0]} for key, value in enquirely.items()
        ]
    return render_template("index.html",
                           enquiry_list=enquiry_list,
                           survey=enquirely,
                           other_links=[
                            {"url": "/start", "text": "初めてアンケート"},
                            {"url": "/end", "text": "終わりアンケート"},
                            ])


@ app.route("/next5")
def next5():
    enquiry_list = [
        {"key": key, "quiz_t": value[0]} for key, value in enquirely.items()
        ]
    return render_template("quiz.html",
                           enquiry_list=enquiry_list,
                           quiz_t=enquirely,
                           other_links=[
                            {"url": "/user_t", "text": "userテーブル"},
                            {"url": "/quiz_t", "text": "クイズテーブル"},
                            {"url": "/survey_t", "text": "アンケートテーブル"},
                            ])


if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)
