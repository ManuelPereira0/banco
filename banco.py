from func import *

menu = '''*************************
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta
[6] Listar Contas
[0] Sair
*************************'''

clientes = []
contas = []

print (menu)
opcao = int(input('Digite sua opção: '))
while True:
    if opcao == 0:
        break
    
    elif opcao == 1:
        depositar(clientes)
        
    elif opcao == 2:
        sacar(clientes)
        
    elif opcao == 3:
        mostrar_extrato(clientes) 
    
    elif opcao == 4:
        criar_cliente(clientes)
                    
    elif opcao == 5:
        numero_conta = len(contas) + 1
        criar_conta(numero_conta, clientes, contas)
    
    elif opcao == 6:
        lista_contas(contas)
        
    else:
        print('Opção inválida!')
    print(menu)
    opcao = int(input('Digite sua opção: '))

