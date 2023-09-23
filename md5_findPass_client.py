import itertools
import hashlib
import socket


def create_pass(size_pass):
    # Function to create all the possible passwords
    letters = '0123456789abcdefghijklmnopqrstuvwxyz'
    passwords = itertools.product(letters, repeat=size_pass)  # Passwords list
    return passwords


def calculate_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def decode_md5(hashed_password, size_pass, start_letter, end_letter):
    possible_passwords = create_pass(size_pass)
    for password_tuple in possible_passwords:
        if (password_tuple[0] == start_letter) and (password_tuple[size_pass - 1] == end_letter):
            password = "".join(password_tuple)
            # print("Trying: {}".format(password))
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
    # start pass &&  end  ==>len
    decode_md5(hashed_password=received_message,size_pass=8, start_letter='t', end_letter='i')
