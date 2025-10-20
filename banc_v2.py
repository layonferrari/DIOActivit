"""
Sistema Bancário - Versão 2 (Desafio DIO)
Operações: Depósito, Saque, Extrato, Criar Usuário e Criar Conta
"""

# ==============================
# VARIÁVEIS GLOBAIS DO SISTEMA
# ==============================
AGENCIA_PADRAO = "0001"
usuarios = []
contas = []


# ==============================
# FUNÇÃO: DEPÓSITO
# ==============================
def depositar(saldo, valor, extrato, /):
    """Recebe os argumentos por posição (positional only)."""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"\n✓ Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("\n✗ Operação falhou! O valor informado é inválido.")
    return saldo, extrato


# ==============================
# FUNÇÃO: SAQUE
# ==============================
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Recebe os argumentos apenas por nome (keyword only)."""
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n✗ Operação falhou! Saldo insuficiente.")
    elif excedeu_limite:
        print(f"\n✗ Operação falhou! O valor excede o limite de R$ {limite:.2f}.")
    elif excedeu_saques:
        print(f"\n✗ Operação falhou! Número máximo de saques ({limite_saques}) excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"\n✓ Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("\n✗ Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


# ==============================
# FUNÇÃO: EXTRATO
# ==============================
def exibir_extrato(saldo, /, *, extrato):
    """Recebe argumentos por posição e nome."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("=========================================")


# ==============================
# FUNÇÃO: CRIAR USUÁRIO
# ==============================
def criar_usuario(usuarios):
    """Cria um novo usuário e adiciona à lista."""
    cpf = input("Informe o CPF (somente números): ")

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n✗ Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\n✓ Usuário criado com sucesso!")


# ==============================
# FUNÇÃO: FILTRAR USUÁRIO
# ==============================
def filtrar_usuario(cpf, usuarios):
    """Retorna o usuário que possui o CPF informado."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


# ==============================
# FUNÇÃO: CRIAR CONTA
# ==============================
def criar_conta(agencia, numero_conta, usuarios):
    """Cria uma nova conta vinculada a um usuário existente."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("\n✓ Conta criada com sucesso!")
    else:
        print("\n✗ Usuário não encontrado. Criação de conta encerrada.")


# ==============================
# FUNÇÃO: LISTAR CONTAS
# ==============================
def listar_contas(contas):
    """Exibe todas as contas cadastradas."""
    for conta in contas:
        linha = f"""
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
"""
        print("=" * 40)
        print(linha)


# ==============================
# MENU PRINCIPAL
# ==============================
def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        menu = """
================ BANCO DIO ================

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[l] Listar Contas
[q] Sair

===========================================
=> """
        opcao = input(menu).lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA_PADRAO, numero_conta, usuarios)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            print("\n✓ Obrigado por usar o Banco DIO. Até logo!")
            break

        else:
            print("\n✗ Operação inválida! Tente novamente.")


# Executa o sistema
if __name__ == "__main__":
    main()
