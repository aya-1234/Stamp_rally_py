import sqlite3

conn = sqlite3.connect('user.db')
cursor = conn.cursor()

try:
    data = [
        (1, '2023-10-26 10:00:00', 1, 'user1', 1, 1, 0),
        (2, '2023-10-26 12:00:00', 0, 'user2', 0, 1, 1),
        (3, '2023-10-27 09:00:00', 1, 'user3', 1, 0, 0),
        (4, '2023-10-27 15:00:00', 0, 'user4', 0, 0, 1),
        (5, '2023-10-28 11:00:00', 1, 'user5', 1, 1, 0),
        (6, '2023-10-28 17:00:00', 1, 'user6', 0, 1, 1),
        (7, '2023-10-29 08:00:00', 0, 'user7', 1, 0, 0),
        (8, '2023-10-29 14:00:00', 0, 'user8', 0, 0, 1)
    ]
        # ... 他のデータ

    cursor.executemany("INSERT INTO USER VALUES (?, ?, ?, ?, ?, ?, ?)", data) # idがAUTOINCREMENTでない場合
    # もしくは id が AUTOINCREMENT の場合
    # cursor.executemany("INSERT INTO USER (datetime, login_status, user_name, service_a, service_b, service_c) VALUES (?, ?, ?, ?, ?, ?)", data)


    conn.commit()
    print("データが挿入されました。")

except sqlite3.IntegrityError as e: # 主キー制約違反などのエラーをキャッチ
    print(f"エラーが発生しました: {e}。idが重複していないか確認してください。")
    conn.rollback()
except sqlite3.Error as e:
    print(f"エラーが発生しました: {e}")
    conn.rollback()
finally:
    conn.close()