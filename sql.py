import sqlite3

conn = sqlite3.connect('gmbot.db')
c = conn.cursor()

# Удалить таблицу "ненужная_таблица", замените "ненужная_таблица" на фактическое имя вашей таблицы
c.execute("DROP TABLE IF EXISTS registration")

# c.execute("SELECT * FROM registration WHERE unique_id = ?")
# result = c.fetchall()
# for row in result:
#     print(row)



conn.commit()


# https://t.me/GMroboticsBot?start=53c39382-ca32-41e7-a3a4-abbd572b4df5


# d:/GM_robotics_bot/sql.py (1, 'test_user', 'John Doe', 'TEST123', '12345')
# (2, 'GMroboticsBot', 'peter', 'https://t.me/GMroboticsBot?start=02', '1034023400')  Я сделал запрос в registrastration и как видишь у меня там заполнилась колонка is_owner и unique_id  вот в таком формате  'https://t.me/GMroboticsBot?start=02'  Почему она автоматически не добавляется в scanning