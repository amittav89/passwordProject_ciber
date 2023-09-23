import socket
import select
import json

alphabet = ['\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

curr_range = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
password = "fc1198178c3594bfdda3ca2996eb65cb"
finish = False


def calculate_next_range(index):
    if index < 0 or index >= len(curr_range):
        return

    if curr_range[index] == len(alphabet) - 1:
        curr_range[index] = 1
        calculate_next_range(index - 1)
    elif curr_range[index] < len(alphabet):
        curr_range[index] += 1


def format_range_to_user(array):
    return ''.join([alphabet[value] for value in array if value != 0])


def send_range(client_socket):
    start_range = curr_range.copy()
    calculate_next_range(len(curr_range) - 4)

    respond = {
        "password": password,
        "start": format_range_to_user(start_range),
        "end": format_range_to_user(curr_range)
    }

    msg = json.dumps(respond).encode('utf-8')
    client_socket.send(msg)
    print(f"Sent: {msg.decode('utf-8')}")


def response_from_client(client_socket):
    global finish
    while not finish:
        send_range(client_socket)

        readable, _, _ = select.select([client_socket], [], [], 1)
        if client_socket in readable:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Received: {data}")

            if data != "":
                print(f"Cracked: the pass is {data}")
                # global finish
                finish = True
                break


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)

    global finish

    while not finish:
        print("Waiting for a connection...")
        client_socket, _ = server_socket.accept()
        print("Connected!")

        response_from_client(client_socket)

    server_socket.close()
    print("\nHit enter to continue...")


if __name__ == "__main__":
    main()
