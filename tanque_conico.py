import math
from threading import Thread
from opcua import Client
from timer import LoopTimer
from time import sleep

cv = 1.2
r0 = 1
r1 = 2
max_height = 5.0
alpha = (r1-r0)/max_height
T = 0.1

class TanqueConico(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.h = 0.0

    def run(self):
        clientOPC = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer")

        clientOPC.connect()

        node1 = clientOPC.get_node("ns=3;i=1008")
        node2 = clientOPC.get_node("ns=3;i=1009")
        qin = node2

        def tank_behavior():
                self.h = (T*(qin.get_value()-cv*math.sqrt(self.h)))/math.pow((math.pi * (r0 + alpha*self.h)), 2) + self.h
                # print("Altura do tanque: ", self.h)
                node1.set_value(self.h) 
        
        timer = LoopTimer(0.1, tank_behavior)
        
        timer.start()

        sleep(120)

        timer.cancel()