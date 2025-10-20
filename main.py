from abc import ABC, abstractmethod
from datetime import datetime

# ====================================
# CLASSE TRANSACAO (ABSTRATA)
# ====================================
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


# ====================================
# CLASSE DEPOSITO
# ====================================
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ====================================
# CLASSE SAQUE
# ====================================
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ====================================
# CLASSE HISTÓRICO
# ====================================
class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def exibir(self):
        print("\n========== EXTRATO ==========")
        for t in self._transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
        if not self._transacoes:
            print("Nenhuma transação registrada.")
        print("=============================")


# ====================================
# CLASSE CONTA
# ====================================
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
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

    def sacar(self, valor):
        saldo_insuficiente = valor > self._saldo

        if saldo_insuficiente:
            print("\n✗ Operação falhou! Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print(f"\n✓ Saque de R$ {valor:.2f} realizado com sucesso!")
            return True
        else:
            print("\n✗ Valor inválido para saque.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n✓ Depósito de R$ {valor:.2f} realizado com sucesso!")
            return True
        else:
            print("\n✗ Valor inválido para depósito.")
            return False


# ====================================
# CLASSE CONTA CORRENTE (HERANÇA)
# ====================================
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [t for t in self.historico._transacoes if t["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"\n✗ Valor do saque excede o limite de R$ {self._limite:.2f}.")
        elif excedeu_saques:
            print(f"\n✗ Limite diário de {self._limite_saques} saques atingido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.cliente.nome}"


# ====================================
# CLASSE CLIENTE
# ====================================
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


# ====================================
# CLASSE PESSOA FÍSICA (HERANÇA)
# ====================================
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# ====================================
# FUNÇÕES AUXILIARES
# ====================================
def menu():
    print("""
========== BANCO POO ==========
[1] Criar cliente
[2] Criar conta
[3] Listar contas
[4] Depositar
[5] Sacar
[6] Extrato
[0] Sair
==============================
""")
    return input("=> ")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def listar_contas(contas):
    for conta in contas:
        print("=" * 40)
        print(conta)


# ====================================
# PROGRAMA PRINCIPAL
# ====================================
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            cpf = input("Informe o CPF (somente números): ")
            cliente = filtrar_cliente(cpf, clientes)

            if cliente:
                print("\n✗ Já existe cliente com esse CPF.")
                continue

            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
            clientes.append(cliente)
            print("\n✓ Cliente criado com sucesso!")

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n✗ Cliente não encontrado.")
                continue

            numero_conta = len(contas) + 1
            conta = ContaCorrente.nova_conta(cliente, numero_conta)
            contas.append(conta)
            cliente.adicionar_conta(conta)
            print("\n✓ Conta criada com sucesso!")

        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "4":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n✗ Cliente não encontrado.")
                continue

            valor = float(input("Valor do depósito: R$ "))
            transacao = Deposito(valor)
            cliente.realizar_transacao(cliente._contas[0], transacao)

        elif opcao == "5":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n✗ Cliente não encontrado.")
                continue

            valor = float(input("Valor do saque: R$ "))
            transacao = Saque(valor)
            cliente.realizar_transacao(cliente._contas[0], transacao)

        elif opcao == "6":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n✗ Cliente não encontrado.")
                continue

            conta = cliente._contas[0]
            conta.historico.exibir()

        elif opcao == "0":
            print("\n✓ Obrigado por usar o Banco POO. Até logo!")
            break

        else:
            print("\n✗ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
