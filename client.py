import socket
import json


def main():
    # Создание UDP сокета
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            expression = input("Введите математическое выражение (например, "
                               "2+2) или exit чтобы завершить программу: ")

            if expression.strip().lower() == 'exit':
                print(f'...terminating...')
                break

            client_socket.sendto(expression.encode(), ('127.0.0.1', 9999))
            result, _ = client_socket.recvfrom(1024)
            print("Результат:", result.decode())

    except ConnectionResetError:
        print(f'Server is not running, terminating...')


if __name__ == "__main__":
    main()
