import socket
import json
import struct
from collections import deque

from expression_cls import Expression
from db import *

UDP_MAX_SIZE = 1024


def handle_req(host: str = '127.0.0.1', port: int = 9999):
    """
        Создаем сокет, "слушаем" запросы от клиента,
    """

    conn = create_db_connection()
    create_table(conn)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.bind((host, port))
    print(f'Server {host}:{port} started')

    fifo_queue = deque()  # FIFO очередь

    while True:
        try:
            msg, addr = server_socket.recvfrom(UDP_MAX_SIZE)
            print(f'Request: raw - {msg} from {addr}')
            expression_str = msg.decode()
            expression = Expression(expression_str)

            # Добавляем сообщение в конец очереди
            fifo_queue.append((expression, addr))

            # Проверяем, есть ли сообщения в очереди для обработки
            while fifo_queue:
                # Получаем сообщение из начала очереди
                expr, client_addr = fifo_queue.popleft()

                try:
                    answer = expr.evaluate()
                except ValueError as e:  # Не будет передано в следующий стек
                    server_socket.sendto(str(e).encode(), client_addr)
                    continue
                except IndexError as e:
                    server_socket.sendto(f'Ошибка: Выражение {expr.string}'
                                         f' не имеет смысла или '
                                         f'записано не правильно'.encode(),
                                         client_addr)
                    continue
                # Отправляем ответ клиенту
                server_socket.sendto(str(answer).encode(), client_addr)
                # Cохраняем в бд результат и само выражение
                insert_expression(conn, client_addr[0], expression_str, answer)

        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    handle_req()
