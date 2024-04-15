import sqlite3

conn = sqlite3.connect('gmbot.db')
c = conn.cursor()

# Удалить таблицу "ненужная_таблица", замените "ненужная_таблица" на фактическое имя вашей таблицы
c.execute("DROP TABLE IF EXISTS scanning")



conn.commit()


# https://t.me/GMroboticsBot?start=53c39382-ca32-41e7-a3a4-abbd572b4df5