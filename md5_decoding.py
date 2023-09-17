import itertools
import hashlib


def create_pass():
    # Function to create all the possible passwords
    letters = '0123456789abcdefghijklmnopqrstuvwxyz'
    passwords = itertools.product(letters, repeat=4)  # Passwords list
    return passwords


def calculate_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def decode_md5(hashed_password):
    possible_passwords = create_pass()
    for password_tuple in possible_passwords:
        password = "".join(password_tuple)
        print("Trying: {}".format(password))
        if calculate_md5(password) == hashed_password:
            print("The password is: {}".format(password))
            return password
    print("Password not found")
    return None


if __name__ == "__main__":
    decode_md5(hashed_password="ee4e8eb1417026452d7ab42013a07838")
