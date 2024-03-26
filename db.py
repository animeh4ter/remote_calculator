import psycopg2


"""
Подключение к базе данных PostgreSQL
Если нет бд - сначала создать ее через psql
CREATE DATABASE udp_server_db OWNER username;
"""


def create_db_connection():
    conn = psycopg2.connect(
        database="udp_server_db",
        user="postgres",
        password="qwe45asd46",
        port=5432
    )
    return conn


# Создание таблицы в базе данных
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expressions (
            id SERIAL PRIMARY KEY,
            client_ip VARCHAR(255),
            expression TEXT,
            result DOUBLE PRECISION
        )
    ''')
    conn.commit()


# Вставка операции в таблицу
def insert_expression(conn, client_ip, expression_str, result):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expressions (client_ip, expression, result) VALUES (%s, %s, %s)', (client_ip, expression_str, result))
    conn.commit()
