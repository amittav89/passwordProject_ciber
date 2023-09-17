import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 8888  # Port should be an integer, not a string
sock.bind((ip, port))  # Use a tuple to specify the address

sock.listen(1)

print("Server is listening")
connection, address = sock.accept()

connection.send("8090010fecf012081f80f6b154077f08".encode())

while True:
    received_message = connection.recv(1024)
    if not received_message:
        break
    print("Received new message: {}".format(received_message.decode()))  # Decode received data

connection.close()
sock.close()
