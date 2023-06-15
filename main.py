from clp import ClientOPC, ServerTCP
from tcp_client import tcp_client
from tanque_conico import TanqueConico
from multiprocessing import Process
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def animate(i):
    file_data = open("data.txt","r").read()
    dataArray = file_data.split('\n')
    time = []
    distance = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            time.append(float(x))
            distance.append(float(y))

    ax.clear()
    ax.plot(time[2:],distance[2:])

def main():
    open('data.txt', 'w').close()

    client_opc_thread = ClientOPC()
    server_tcp_thread = ServerTCP()
    tanque_conico_thread = TanqueConico()

    href = input("Insira o setpoint de altura do tanque (Deve ser menor que a altura máxima especificada): ")

    tcp_client_process = Process(target=tcp_client, args=[href])
    
    server_tcp_thread.start()
    tcp_client_process.start()
    tanque_conico_thread.start()
    client_opc_thread.start()
    
    ani = animation.FuncAnimation(fig, animate)
    plt.show()

    client_opc_thread.join()
    tanque_conico_thread.join()
    server_tcp_thread.join()
    tcp_client_process.terminate()

    print("Fim do ciclo de controle")

if __name__ == "__main__":
    main()