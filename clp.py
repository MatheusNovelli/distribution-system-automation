from threading import Thread
import socket, json
from timer import LoopTimer
import time
from opcua import Client

h = 0.0

class ClientOPC(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.qin = 0.0
        self.I = 0.0
        self.error = 0.0
        self.prev_error = 0.0
    
    def run(self):
        print("Rodando client")
        clientOPC = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer")

        clientOPC.connect()

        node1 = clientOPC.get_node("ns=3;i=1008")

        global h
        h = node1

        node2 = clientOPC.get_node("ns=3;i=1009")
        
        href = 4.0
        K = 2
        Ti = 30
        Td = 0.5
        T = 0.1

        def control_system():
            prev_h = h.get_value()
            P = self.error
            self.I = self.error * T + self.I
            D = (self.error - self.prev_error)/T

            self.qin = K * (P + (1/Ti)*self.I + Td * D)
            
            self.error = href - h.get_value()
            self.prev_error = href - prev_h

            node2.set_value(self.qin)
        
        timer = LoopTimer(0.1, control_system)
        
        timer.start()

        time.sleep(120)

        timer.cancel()

class ServerTCP(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((socket.gethostname(), 8000))
        s.listen()    
        print("Rodando server")
        clientsocket, address = s.accept()

        def send_message():
            clientsocket.sendall(bytes(json.dumps(str(h.get_value())).encode()))

        timer = LoopTimer(0.2, send_message)
        
        timer.start()

        time.sleep(120)

        timer.cancel()
