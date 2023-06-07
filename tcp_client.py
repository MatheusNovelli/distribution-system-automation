import socket, json

def tcp_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8000))
    while True:
        data_rcv = json.loads(s.recv(1024))
        f = open("historiador.txt", "a")
        f.write(data_rcv + "\n")
