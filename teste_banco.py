import sqlite3

conn = sqlite3.connect("database/frequencia.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

for tabela in cursor.fetchall():
    print(tabela)

conn.close()