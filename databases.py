import sqlite3

conn = sqlite3.connect('.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            option_1 TEXT NOT NULL,
            option_2 TEXT NOT NULL,
            option_3 TEXT NOT NULL,
            FOREIGN KEY (group_id) REFERENCES quiz_groups(id)
               )
''')

conn.commit()
conn.close()

print("データベースとテーブルが作成されました。")