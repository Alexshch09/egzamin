import mysql.connector
from bs4 import BeautifulSoup

# Устанавливаем соединение с базой данных
conn = mysql.connector.connect(
    host='192.168.0.185',
    user='root',
    password='',
    database='ttt'
)
cursor = conn.cursor()

# Читаем HTML файл
with open('index.html', 'r', encoding='utf-8') as file:
    content = file.read()


# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(content, 'html.parser')

# Создаем таблицу, если её нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question_text TEXT,
        image_url TEXT,
        option_A TEXT,
        option_B TEXT,
        option_C TEXT,
        option_D TEXT,
        correct_answer TEXT
    )
''')
conn.commit()

# Итерируемся по каждому вопросу
for question_div in soup.find_all('div', class_='question'):
    question_text = question_div.find('div', class_='title').text.strip()
    image_url_tag = question_div.find('img')
    image_url = image_url_tag['src'] if image_url_tag else None
    options = [option.text.strip() for option in question_div.find_all('div', class_='answer')]
    correct_answer = question_div.find('div', class_='correct').text.strip()

    # Формируем SQL-запрос для вставки данных
    sql_query = '''
        INSERT INTO questions (question_text, image_url, option_A, option_B, option_C, option_D, correct_answer)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    
    # Выполняем SQL-запрос
    cursor.execute(sql_query, (question_text, image_url, options[0], options[1], options[2], options[3], correct_answer))
    conn.commit()

# Закрываем соединение с базой данных
conn.close()