from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import os


app = Flask(__name__, static_folder='static')

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

# next1の画面内容


@ app.route('/next1')
def next1():
    return render_template('admin.html')

# next1の中身

# ネクストの中身を記述
# 1,管理者メニュー、db操作、db編集

# next1/serch内に検索結果を表示する

@app.route('/next1/search', methods=['POST'])
def search_user():
    search_login_id = request.form.get('search_login_id')  # Get the login ID from the form

    if not search_login_id:
        return render_template('admin.html', error="ログインIDを入力してください")


    try:
        with sqlite3.connect('user.db') as conn:
            df = pd.read_sql(
                'SELECT * FROM USER WHERE loginId TEXT, ?',
                conn,
                params=['%' + search_login_id + '%']
            )

        if df.empty: # 検索結果がない場合の処理
            return render_template('search.html', error="該当するユーザーが見つかりません", search_name=search_login_id)

        return render_template('search_results.html', search_results=df, search_name=search_login_id)

    except Exception as e: # エラー処理
        return render_template('search.html', error=f"エラーが発生しました: {e}")


# @ app.route('/next1/search', methods=['POST'])
# def search_user():
#     search_name = request.form.get('search_name')
#     output = '<h2>検索結果</h2>'

#     with sqlite3.connect('user.db') as conn:
#         df = pd.read_sql(
#             'SELECT * FROM USER WHERE name LIKE ?',
#             conn,
#             params=['%' + search_name + '%']
#             )
#         output += df.to_html()

#     output += '''
#     <br>
#     <a href="/next1">管理者メニューに戻る</a>
#     <br>
#     <a href="/">トップに戻る</a>
#     '''
#     return output

# userを追加するためのコード


@ app.route('/next1/add', methods=['POST'])
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


# ext2の中身を表示
@app.route('/next2')
def next2():
    return render_template('ljalkjsdf.html')

# '''
#     <style>
#         .how-to-play {
#             margin: 20px;
#             padding: 15px;
#             background-color: #f5f5f5;
#             border-radius: 5px;
#         }
#         .map-button {
#             display: inline-block;
#             padding: 10px 20px;
#             background-color: #4CAF50;
#             color: white;
#             text-decoration: none;
#             border-radius: 5px;
#             margin: 10px 0;
#         }
#         .map-button:hover {
#             background-color: #45a049;
#         }
#     </style>

#     '''


# def pdf_to_base64_image(pdf_path, page_number=0):
#     """PDFをBase64エンコードされた画像データに変換する"""
#     try:
#         doc = fitz.open("image/map_ol2.pdf")
#         page = doc.load_page(1)  # 指定ページを読み込み (デフォルトは最初のページ)
#         pix = page.get_pixmap(alpha=False)  # 透明度なしで画像を取得
#         image_bytes = pix.tobytes("png") # PNG形式でバイトデータを取得
#         encoded_string = base64.b64encode(image_bytes).decode("utf-8")
#         return f"data:image/png;base64,{encoded_string}"
#     except Exception as e:
#         print(f"Error converting PDF to image: {e}")
#         return None


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


# @app.route('/enq/<key>')


# @ app.route('/next5/<key>')  # <key>をURLパラメータとして受け取る
# def enq(key):
#     # キーが辞書に存在しない場合のエラーハンドリング
#     if key not in enquirely:
#         return "指定されたキーは存在しません。", 404

#     # キーに基づいて質問と選択肢を取得
#     question, option1, option2 = enquirely[key]

#     # quiz.htmlテンプレートにデータを渡してレンダリング
#     return render_template("quiz.html",
#                            key=key,
#                            question=question,
#                            option1=option1,
#                            option2=option2
#                            )


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

# PDFファイルを提供するための新しいルート


# @ app.route('/map_ol2.pdf')
# def serve_pdf():
#     return send_file(
#         os.path.join(app.root_path, 'static', 'map_ol2.pdf'),
#         as_attachment=True)

# 全tableを表示


# @ app.route("/table")
# def table():
#     enquiry_list = [
#         {"key": key, "title": value[0]} for key, value in enquirely.items()
#         ]
#     return render_template("table.html",
#                            enquiry_list=enquiry_list,
#                            all_table=enquirely,
#                            other_links=[
#                             {"url": "/user_t", "text": "userテーブル"},
#                             {"url": "/quiz_t", "text": "クイズテーブル"},
#                             {"url": "/survey_t", "text": "アンケートテーブル"},
#                             ])


@ app.route('/table')
def table():
     output = '''
     <table>
         <thead>
             <tr>
                 <th>ID</th>
                 <th>名前</th>
                 <th>登録日時</th>
             </tr>
         </thead>
         <tbody>
     '''

     with sqlite3.connect('data.db') as conn:
         cursor = conn.cursor()
         cursor.execute('SELECT * FROM user')
         users = cursor.fetchall()

         for user in users:
            output += f'''
            <tr>
                <td>{user[0]}</td>
                <td>{Markup.escape(str(user[1]))}</td>  # エスケープ処理を追加
                <td>{user[2]}</td>
            </tr>
            '''

     output += '''
         </tbody>
     </table>
         <br>
     <a href="/">トップページに戻る</a>
     '''

     return output


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
                            {"url": "/quiz_1", "text": "クイズ1_アンケート"},
                            {"url": "/quiz_2_survey", "text": "クイズ2_アンケート"},
                            {"url": "/quiz_3_survey", "text": "クイズ3_アンケート"},
                            {"url": "/quiz_4_survey", "text": "クイズ4_アンケート"},
                            {"url": "/quiz_5_survey", "text": "クイズ5_アンケート"},
                            {"url": "/quiz_6_survey", "text": "クイズ6_アンケート"},
                            {"url": "/quiz_7_survey", "text": "クイズ7_アンケート"},
                            {"url": "/quiz_8_survey", "text": "クイズ8_アンケート"},
                            {"url": "/end", "text": "終わりアンケート"},
                            ])



@ app.route("/next5")
def quiz_all():
    enquiry_list = [
        {"key": key, "title": value[0]} for key, value in enquirely.items()
        ]
    return render_template("index.html",
                           enquiry_list=enquiry_list,
                           quiz_all = enquirely,
                           other_links = [
                             {"url": "/quiz_1", "text": "クイズ1"},
                             {"url": "/quiz_2", "text": "クイズ2"},
                             {"url": "/quiz_3", "text": "クイズ3"},
                             {"url": "/quiz_4", "text": "クイズ4"},
                             {"url": "/quiz_5", "text": "クイズ5"},
                             {"url": "/quiz_6", "text": "クイズ6"},
                             {"url": "/quiz_7", "text": "クイズ7"},
                             {"url": "/quiz_8", "text": "クイズ8"},
                             ])


DATABASE = 'quiz.db'  # データベースファイル名を統一

def quiz():

        # アプリケーション起動時にデータベースとテーブルを作成、データ挿入
    insert_quiz_data()
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
            conn.commit()  # 変更をコミット

            # テーブル作成後の処理 (例: データの挿入)
            insert_quiz_data(conn, cursor)

    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
        return "データベースエラー", 500  # エラーレスポンスを返す

    return "テーブルが作成されました", 201 # 成功レスポンスを返す



def insert_quiz_data(conn, cursor):
    quizzes = [
        ("quiz_1", "クイズ1のタイトル", "クイズ1の内容..."),
        ("quiz_2", "クイズ2のタイトル", "クイズ2の内容..."),
        # ... 他のクイズデータ
    ]
    try:
        cursor.executemany("INSERT OR IGNORE INTO quizzes (key, title, content) VALUES (?, ?, ?)", quizzes)
        conn.commit()
    except sqlite3.Error as e:
        print(f"データ挿入エラー: {e}")
        conn.rollback()  # エラーが発生した場合はロールバック

    #cursor.executemany("INSERT OR IGNORE INTO quizzes (key, title, content) VALUES (?, ?, ?)", quizzes)

# アプリケーション起動時にデータ挿入 (必要に応じてコメントアウト)
#insert_quiz_data()

def get_quiz_data_from_db():
     db = getattr(app, '_database', None)
     if db is None:
         db = app._database = sqlite3.connect(DATABASE)
         db.row_factory = sqlite3.Row  # ディクショナリのようなアクセスを可能にする
     return db

# @ app.route("/quiz1")
# def quiz(quiz_id):
#     enquirely = get_quiz_data_from_db()
#     if enquirely is None:  # データベースエラーが発生した場合
#         return "データベースエラー", 500
#     if 1 <= quiz_id <= len(enquirely):
#         quiz_key = f"quiz_{quiz_id}"
#         quiz_title = enquirely[quiz_key][0]
#         quiz_content = enquirely[quiz_key][1]
#         i = quiz_id
#         o = quiz_content
#         other_links ={"url": f"/quiz/{i 1}", "text": f"クイズ{o}"} for:i in range(1, len(enquirely) +)
#         return render_template("quiz.html",
#                                 quiz_title=quiz_title,
#                                 quiz_content=quiz_content, # クイズの内容を渡す
#                                 other_links=other_links,
#                                 current_quiz_id=quiz_id) # 現在のクイズIDを渡す
#     else:
#     return "クイズが見つかりません", 404
#     # クイズIDが無効な場合のエラー処理                     )

@app.route("/quiz_<int:quiz_id>")
def quiz(quiz_id):
    enquirely = get_quiz_data_from_db()
    if enquirely is None:  # データベースエラーが発生した場合
        return "データベースエラー", 500
    if 1 <= quiz_id <= len(enquirely):
        quiz_key = f"quiz_{quiz_id}"
        quiz_title = enquirely[quiz_key][0]
        quiz_content = enquirely[quiz_key][1]  # クイズの内容を追加
        other_links = [
            {"url": f"/quiz/{i}", "text": f"クイズ{i}"} for i in range(1, len(enquirely) + 1)
        ]
        return render_template("quiz.html",
                               quiz_title=quiz_title,
                               quiz_content=quiz_content, # クイズの内容を渡す
                               other_links=other_links,
                               current_quiz_id=quiz_id) # 現在のクイズIDを渡す
    else:
        return "クイズが見つかりません", 404
    # クイズIDが無効な場合のエラー処理


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(app, '_database', None)
#     if db is not None:
#         db.close()


# # データベースの初期化 (初回起動時のみ実行)
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# schema.sql (データベースのスキーマ定義)
# quiz.dbと同じディレクトリに配置
# ルートURL (グループ選択画面)


# クイズ画面
# @app.route('/next6/<int:group_id>', methods=['GET', 'POST'])
# def quiz(group_id):
#     db = get_db()
#     group = db.execute(
#         'SELECT name FROM quiz_groups WHERE id = ?',
#         (group_id,)).fetchone()
#     if group is None:
#         return "グループが見つかりません", 404

#     questions = db.execute(
#         'SELECT * FROM questions WHERE group_id = ?', (group_id,)
#         ).fetchall()
#     if not questions:
#         return "このグループには問題がありません。", 404

#     if request.method == 'POST':
#         score = 0
#         results = []
#         for question in questions:
#             user_answer = request.form.get(f"question_{question['id']}")
#             correct = user_answer == question['correct_answer']
#             score += int(correct)
#             results.append({
#                 'question': question['question_text'],
#                 'user_answer': user_answer,
#                 'correct_answer': question['correct_answer'],
#                 'is_correct': correct,
#                 'options': [
#                     question['option_1'],
#                     question['option_2'],
#                     question['option_3']
#                             ]
#             })
#         return render_template(
#             'results.html', results=results, score=score, total=len(questions),
#             group_name=group['name'])

#     return render_template(
#         'quiz.html', questions=questions, group_name=group['name'])

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)
