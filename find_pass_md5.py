import itertools
import hashlib


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
            print("Trying: {}".format(password))
            if calculate_md5(password) == hashed_password:
                print("The password is: {}".format(password))
                return password
    print("Password not found")
    return None


if __name__ == "__main__":
    decode_md5(hashed_password="f6182f0359f72aae12fb90d305ccf9eb", size_pass=5, start_letter='y', end_letter='g')
