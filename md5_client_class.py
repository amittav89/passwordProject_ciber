import socket
import threading
import json
import itertools


def calculate_md5(text):
    import hashlib
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def decode_md5(hashed_password, start_range, end_range):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

    # Convert start and end range from base 36 to integers
    start_index = int(start_range, 36)
    end_index = int(end_range, 36)

    password_length = len(start_range)

    password_range = alphabet[start_index:end_index + 1]

    for password_tuple in itertools.product(password_range, repeat=password_length):
        password = "".join(password_tuple)
        hashed = calculate_md5(password)
        if hashed == hashed_password:
            return password  # Return the cracked password

    return None


def send_password_to_server(password):
    try:
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8080))
        message = {"password": password}
        sock.send(json.dumps(message).encode('utf-8'))
    except socket.error as e:
        print("Socket error while sending password to server:", e)
    finally:
        sock.close()


def get_hashcode():
    try:
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8080))
        recv_message = sock.recv(1024)
        print("Received new message: {}".format(recv_message.decode()))  # Decode received data
        return recv_message.strip().decode()  # Remove leading/trailing whitespace
    except socket.error as e:
        print("Socket error while getting hashcode from server:", e)
    finally:
        sock.close()


def try_to_crack_password(data):
    try:
        password_length = len(data['start'])  # Calculate password length from the received range

        start_range = data['start']  # Extract start range from JSON
        end_range = data['end']  # Extract end range from JSON

        cracked_password = decode_md5(data['password'], start_range, end_range)

        if cracked_password:
            print("The password is: {}".format(cracked_password))
            send_password_to_server(cracked_password)
        else:
            print("Password not found")
    except Exception as e:
        print("Error in try_to_crack_password:", e)


if __name__ == "__main__":
    received_message = get_hashcode()  # Get the MD5 hash and range from the server's JSON
    data = json.loads(received_message)

    # Create a thread to attempt to crack the password
    crack_thread = threading.Thread(target=try_to_crack_password, args=(data,))
    crack_thread.start()

    # You can add more threads if needed

    crack_thread.join()
    print("Done")
