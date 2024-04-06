import sqlite3

conn = sqlite3.connect('gmbot.db')
c = conn.cursor()

# Удалить таблицу "ненужная_таблица", замените "ненужная_таблица" на фактическое имя вашей таблицы
c.execute("DROP TABLE IF EXISTS scanning")

conn.commit()