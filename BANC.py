"""
Sistema Bancário - Desafio DIO
Operações: Depósito, Saque e Extrato
"""

# Variáveis do sistema
saldo = 0
limite_saque = 500
numero_saques = 0
LIMITE_SAQUES_DIARIOS = 3
extrato_movimentacoes = ""

# Menu principal
menu = """
================ BANCO DIO ================

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

===========================================
=> """

while True:
    opcao = input(menu).lower()

    # Operação de Depósito
    if opcao == "d":
        print("\n========== DEPÓSITO ==========")
        valor = float(input("Informe o valor do depósito: R$ "))
        
        if valor > 0:
            saldo += valor
            extrato_movimentacoes += f"Depósito:  R$ {valor:.2f}\n"
            print(f"\n✓ Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\n✗ Operação falhou! O valor informado é inválido.")
    
    # Operação de Saque
    elif opcao == "s":
        print("\n========== SAQUE ==========")
        valor = float(input("Informe o valor do saque: R$ "))
        
        # Validações
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite_saque
        excedeu_saques = numero_saques >= LIMITE_SAQUES_DIARIOS
        
        if excedeu_saldo:
            print("\n✗ Operação falhou! Você não tem saldo suficiente.")
        
        elif excedeu_limite:
            print(f"\n✗ Operação falhou! O valor do saque excede o limite de R$ {limite_saque:.2f}.")
        
        elif excedeu_saques:
            print(f"\n✗ Operação falhou! Número máximo de saques diários ({LIMITE_SAQUES_DIARIOS}) excedido.")
        
        elif valor > 0:
            saldo -= valor
            extrato_movimentacoes += f"Saque:     R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"\n✓ Saque de R$ {valor:.2f} realizado com sucesso!")
            print(f"Saques restantes hoje: {LIMITE_SAQUES_DIARIOS - numero_saques}")
        
        else:
            print("\n✗ Operação falhou! O valor informado é inválido.")
    
    # Operação de Extrato
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        
        if extrato_movimentacoes:
            print(extrato_movimentacoes)
        else:
            print("Não foram realizadas movimentações.")
        
        print(f"\nSaldo:     R$ {saldo:.2f}")
        print("=========================================")
    
    # Sair do sistema
    elif opcao == "q":
        print("\n✓ Obrigado por usar o Banco DIO. Até logo!")
        break
    
    else:
        print("\n✗ Operação inválida! Por favor, selecione uma opção válida.")
