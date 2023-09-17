import socket

sock = socket.socket()
sock.connect(("127.0.0.1", 8080))

while True:
    received_message = sock.recv(1024)
    print("Received new message: {}".format(received_message.decode()))  # Decode received data
    message = input("enter your message: \n")
    sock.send(message.encode())

sock.close()
