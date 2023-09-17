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


def decode_md5(hashed_password, possible_passwords, start_letter, end_letter):
    for password_tuple in possible_passwords:
        if (password_tuple[0] == start_letter) and (password_tuple[(len(password_tuple)) - 1] == end_letter):
            password = "".join(password_tuple)
            print("Trying: {}".format(password))
            if calculate_md5(password) == hashed_password:
                print("The password is: {}".format(password))
                return password
    print("Password not found")
    return None


def get_hashcode():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 8888))
    recv_message = sock.recv(1024)
    print("Received new message: {}".format(recv_message.decode()))  # Decode received data
    sock.close()
    return recv_message


if __name__ == "__main__":
    received_message = get_hashcode().decode()  # Remove leading/trailing whitespace

    possible_passwords = create_pass(8)
    possible_passwords = copy_to_regular_list(possible_passwords)

    middle_index = int(len(possible_passwords) / 2)

    start_to_middle = possible_passwords[: middle_index]
    middle_to_end = possible_passwords[middle_index]

    t1 = threading.Thread(target=decode_md5, args=(received_message, start_to_middle, 'a', 't'))
    t2 = threading.Thread(target=decode_md5, args=(received_message, middle_to_end, 'a', 't'))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done")

