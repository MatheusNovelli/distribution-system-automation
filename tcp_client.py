import socket, json
import time

def tcp_client(href):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8000))
    start_time = time.time()
    sending_data = True

    while sending_data:
        s.sendall(bytes(json.dumps(href).encode()))
        sending_data = False
        
    while True:
        try:
            data_rcv = json.loads(s.recv(1024))
            f = open("historiador.txt", "a")
            f.write(data_rcv + "\n")
            if float(data_rcv)/5.0 < 0.05:
                with open('below.txt', 'r') as f:
                    for line in f:
                        print(line.rstrip())
            
            elif float(data_rcv)/5.0 > 0.95:
                with open('above.txt', 'r') as f:
                    for line in f:
                        print(line.rstrip())

            graph_data = open("data.txt", "a")
            graph_data.write(str(round(time.time()-start_time))+","+str(data_rcv)+"\n")
        except:
            s.close()
        
        

    