import itertools
import hashlib
import socket
import threading


def create_pass(size_pass):
    # Function to create all the possible passwords
    letters = '0123456789abcdefghijklmnopqrstuvwxyz'
    passwords = itertools.product(letters, repeat=size_pass)  # Passwords list
    return passwords


def calculate_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def copy_to_regular_list(itertools_list):
    new_list = []
    for item in itertools_list:
        new_list.append("".join(item))
    return new_list


def decode_md5(hashed_password, start_letter, end_letter):
    for password_tuple in possible_passwords:
        if (password_tuple[0] == start_letter) and (password_tuple[(len(password_tuple)) - 1] == end_letter):
            # print("Trying: {}".format(password))
            if calculate_md5(password_tuple) == hashed_password:
                print("The password is: {}".format(password_tuple))
                return password_tuple
    print("Password not found")
    return None


def get_hashcode():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 8080))
    recv_message = sock.recv(1024)
    print("Received new message: {}".format(recv_message.decode()))  # Decode received data
    sock.close()
    return recv_message


if __name__ == "__main__":
    received_message = get_hashcode().decode()  # Remove leading/trailing whitespace

    possible_passwords = create_pass(6)
    possible_passwords = copy_to_regular_list(possible_passwords)

    middle_index = int(len(possible_passwords) / 2)

    t1 = threading.Thread(target=decode_md5, args=(received_message, 'c', '6'))
    t2 = threading.Thread(target=decode_md5, args=(received_message, 'c', '6'))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done")

