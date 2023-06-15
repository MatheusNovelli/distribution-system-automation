# Trabalho Prático Final

## Descrição do projeto

Operação e controle da altura do líquido de um tanque industrial, garantindo que este não transborde e nem fique em um nível abaixo do esperado. A arquitetura do projeto consiste em um par cliente/servidor TCP se comunicando com um par cliente/servidor OPC que faz ligação direta com um cliente OPC que simula o comportamento do tanque

## Especificações do tanque

-> Altura máxima: 5.0m
-> Raio 0 (entrada): 1.0m
-> Raio 1 (saída): 2.0m
-> Coeficiente de descarga de saída: 1.2

## Estrutura de arquivos

O projeto está separado em arquivos por threads, além de contar com a função main.

**-> tanque_conico:**
Thread do tanque cônico, client OPC responsável pelo comportamento do enchimento do tanque e envio e recebimento de dados ao servidor OPC.

**-> clp:**
Este arquivo contém a thread ClientOPC, responsável pelo controle da vazão de entrada do tanque de acordo com o valor atual da altura, que é resgatada pelo servidor OPC, e da altura de referência, que é passada pelo servidor TCP. O ClientOPC fornece constantemente o valor da vazão de entrada ao servidor OPC.
Além do ClientOPC, este arquivo também contem o ServerTCP, responsável por receber o valor de referência do client TCP e enviar os valores de altura atual, recebidos do cliente OPC, via socket.

**-> tcp_client:**
Processo que se comunica com o servidor TCP/IP via socket, responsável por armazenar os valores da altura do líquido do tanque em um arquivo historiador e também pela inserção e envio da altura de referência para o servidor, além de escrever no arquivo data, responsável pelos pontos utilizados na construção do gráfico, e também da exibição de alertas no terminal. É recomendado a deleção do arquivo historiador depois de cada vez que o processo é executado. Pois este
pode ficar com um tamanho muito grande, devido ao grande fluxo de dados que chegam até ele.

**-> timer:**
Dispositivo responsável pela repetição de tarefas, recebe como argumentos o tempo dessa repetição e a função de callback,
que seria a tarefa a ser repetida.

**-> main:**
Processo principal, responsável por inicializar e encerrar thread e processos.

## Instalando dependências

Neste projeto foi utilizada a biblioteca opcua. Para instalar as dependência do projeto de maneira prática, basta rodar o comando `pip install -r requirements.txt`.

## Rodando o projeto

Para rodar o projeto, é necessário inicializar o servidor OPC Prosys OPC UA Simulation Server e adicionar as variáveis de altura do líquido do tanque e vazão de entrada ("ns=3;i=1008" e "ns=3;i=1009").
Em seguida, basta rodar o comando `python main.py`.
Feito isso, o programa irá solicitar uma altura de referência que, deve ser MENOR que a altura máxima do tanque (5.0).
Após 2 minutos, as threads param e o programa exibe o gráfico final da altura do líquido do tanque, que estava sendo exibido em tempo real. Ao fechá-lo, o programa se encerra.
