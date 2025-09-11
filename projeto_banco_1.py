import textwrap

def menu():
    menu = """\n
    ==========================================
        BEM-VINDO AO BANCO NASCIMENTO
    ==========================================

    [0]\t Depositar
    [1]\t Sacar
    [2]\t Extrato
    [3]\t Nova Conta
    [4]\t Listar Contas
    [5]\t Novo Usuário
    [6]\t Sair

    ==========================================
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor >=0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n Depósito Realizado!")
    else:
        print("\n Valor informado é Invalido")
        
    return saldo, extrato
    
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("Você não tem Saldo Suficente")
        
    elif excedeu_limite:
        print("Valor do Saque Excedu o Limete")
        
    elif excedeu_saques:
        print("Número Máximo de saques Excedeu")
        
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque Realizado com Sucesso")
        
    else:
        print("O Vlor informado é inávalido")
        
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, / , *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações, até o momento." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (Somente Números): ")
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print(" Já existe usuário com esse CPF!")
        return 
    
    nome = input("Informe o Nome Completo: ")
    data_nascimento = input("infome sua data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu Endereço (Logradouro, nro - bairro - cidade/sigla Estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco":endereco})
    
    print("Usuário cadastrado com Sucesso!")  

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"]==cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do Usuário: ")
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print("\n Conta Criada Com Sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n Usuário não encontrado, criação de conta encerrado")
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t {conta['numero_conta']}
            Titular:\t {conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))
  

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
   
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "0":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "1":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato,numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            
            )
       
        elif opcao == "2":
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações, até o momento." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")
        
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "5":
            criar_usuario(usuarios)
        
        elif opcao == "3":
            numero_conta = len(contas) + 1
            conta =  criar_conta(AGENCIA, numero_conta, usuarios)
        
            if conta:
                contas.append(conta)
        
        elif opcao == "4":
            listar_contas(contas)

        elif opcao == "6":
            break

        else:
            print("Por favor selecione novamente a operação desejada.")
        
main()