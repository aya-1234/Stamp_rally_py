import sqlite3

# データベース接続
conn = sqlite3.connect('user.db')  # 適切なデータベース名に変更
cursor = conn.cursor()

# テーブル作成 (既に存在する場合は何もしない)
cursor.execute('''
CREATE TABLE IF NOT EXISTS USER (
    id INTEGER PRIMARY KEY,
    issuedAt DATETIME,
    isUsed BOOLEAN,
    loginId TEXT,
    isLoggedin BOOLEAN,
    isAgree BOOLEAN,
    isEnded BOOLEAN
)
''')

# データ挿入
try:
    cursor.execute("INSERT INTO USER (issuedAt, isUsed, loginId, isLoggedin, isAgree, isEnded) VALUES (?, ?, ?, ?, ?, ?)",(datetime.datetime.now(), False, "some_login_id", False, True, False)) # 適切な値に置き換える
    conn.commit() 
    print("Data inserted successfully.")

except sqlite3.IntegrityError as e:  # 例: loginIdが一意制約に違反した場合
    print(f"Error inserting data: {e}")
except Exception as e:  # その他のエラー
    print(f"An unexpected error occurred: {e}")


# 接続を閉じる (必須)
conn.close()