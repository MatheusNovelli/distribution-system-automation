from clp import ClientOPC, ServerTCP
from tcp_client import tcp_client
from tanque_conico import TanqueConico
from multiprocessing import Process

def main():
    client_opc_thread = ClientOPC()
    server_tcp_thread = ServerTCP()
    tanque_conico_thread = TanqueConico()

    tcp_client_process = Process(target=tcp_client)

    
    server_tcp_thread.start()
    tcp_client_process.start()
    tanque_conico_thread.start()
    client_opc_thread.start()

    server_tcp_thread.join()
    tcp_client_process.terminate()
    tanque_conico_thread.join()
    client_opc_thread.join()
    


if __name__ == "__main__":
    while True:
        main()