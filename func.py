from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime

from more_itertools import pad_none

class Cliente:
    def __init__(self, endereco):
        self.enderco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar (self, valor):
        saldo = self.saldo
        if valor > saldo:
            print('Você não tem saldo suficiente para realizar o saque.')
        elif valor > 0:
            self._saldo -= valor
            print('Valor sacado com sucesso!')
            return True
        else:
            print('Saque inválido.')
        return False
    
    def depositar(self, valor):
        if valor > 0:
            print('DIposito realizado com sucesso!')
            self._saldo += valor
            
        else:
            print('Saque inválido.')
            return False
        
        return True
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
        [transacao for transacao in self.historico.transacoes 
        if transacao['tipo'] == Saque.__name__]
        )
        
        if valor > self._limite:
            print('Você não tem dinheiro suficiente para realizar o valor.')
        
        elif numero_saques > self._limite_saques:
            print('Você realizou todos os valor possíveis pro dia de hoje.')
        
        else:
            return super().sacar(valor)
                
        return False
    
    def __str__(self):
        return f'''\
            Agência: \t{self.agencia}
            C/C: \t{self.numero}
            Titular: \t{self.cliente.nome}'''


class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor
            }
        )  


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass 
    
    @abstractmethod
    def registrar(self, conta):
        pass
    
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
def sacar (clientes):
    cpf = input('Digite seu CPF (somente numero): ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Digite o valor a ser sacado: R$'))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def depositar (clientes):
    cpf = input('Digite seu CPF (somente numero): ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Digite o valor a ser depositado: R$'))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def mostrar_extrato(clientes):
    cpf = input('Digite seu CPF (somente numero): ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n Extrato ".center(40, '='))
    transacoes = conta.historico.transacoes
    
    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas transações.'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR${conta.saldo:.2f}")
    print(49 * '=')
    
def criar_cliente(clientes):
    cpf = input('Digite seu CPF (somente numero): ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print('Cliente já existe!')
        return
         
    nome = str(input('Digite seu nome: '))
    data_nascimento = input('Digite sua data de nascimento (dd-mm-aaaa): ')
    endereco = input('Digite seu endreço:')
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print('Usuário criado com sucesso!')
    
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = []
    for cliente in clientes:
        if cliente.cpf == cpf:
            clientes_filtrados.append(cliente)
            
    return clientes_filtrados[0] if clientes_filtrados else None
        
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possuí conta')
        return
    
    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas ):
    cpf = input('Digite seu CPF (somente numero): ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado!')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta criado com sucesso!')        
    
def lista_contas(contas):
    for conta in contas:
        print(100 * '=')
        print(str(conta))