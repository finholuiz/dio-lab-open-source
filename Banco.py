from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco, nome=None, data_nascimento=None, cpf=None):
        self.endereco = endereco
        self.contas = []
        # opcional: guardar dados pessoais diretamente (usado para PessoaFisica)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_contas(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco, nome=nome, data_nascimento=data_nascimento, cpf=cpf)
        # já inicializa os atributos na superclasse


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Não há saldo suficiente.")
            return False

        if valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        print("\nValor informado é inválido. Operação falhou!")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso.")
            return True

        print("\nOperação falhou! O valor informado é inválido.")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        # conta o número de saques já realizados no histórico
        numero_saques = len(
            [
                t
                for t in self.historico.transacoes
                if t["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nO valor do saque excede o limite.")
            return False

        if excedeu_saques:
            print("\nNúmero máximo de saques excedido.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return textwrap.dedent(
            f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome if self.cliente.nome else '—'}
            """
        )


class Transacao(ABC):
    @property
    @abstractmethod
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


# ---------- Funções auxiliares / UI ----------


def menu():
    menu_text = """\n
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
    return input(textwrap.dedent(menu_text))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente ainda não possui conta!")
        return None
    # FIXME: permitir o cliente escolher qual conta (aqui retorna sempre a primeira)
    return cliente.contas[0]


def criar_cliente(clientes, cpf=None):
    # Se cpf for passado, reutiliza; caso contrário pergunta
    if cpf is None:
        cpf = input("Informe o CPF (Somente Números): ").strip()
    else:
        cpf = str(cpf).strip()

    cliente_existente = filtrar_cliente(cpf, clientes)
    if cliente_existente:
        print("Já existe usuário com esse CPF!")
        return cliente_existente

    nome = input("Informe o Nome Completo: ")
    data_nascimento = input("Informe sua data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu Endereço (Logradouro, nro - bairro - cidade/UF): ")

    novo = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo)
    print("Usuário cadastrado com sucesso!")
    return novo


def criar_conta(numero_conta, clientes, contas, cpf=None):
    if cpf is None:
        cpf = input("Informe o CPF do Usuário: ").strip()

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado. Fluxo de criação de conta encerrado!")
        return None

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")
    return conta


def depositar(clientes, contas):
    cpf = input("Informe o CPF do Cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        opcao = input("Deseja cadastrar um novo cliente com esse CPF? (s/n): ").strip().lower()
        if opcao == "s":
            cliente = criar_cliente(clientes, cpf)
        else:
            return

    # se cliente não possuir conta, perguntar se deseja criar
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        opcao = input("Cliente não possui conta. Deseja criar uma nova conta agora? (s/n): ").strip().lower()
        if opcao == "s":
            conta = criar_conta(len(contas) + 1, clientes, contas, cpf=cliente.cpf)
            if not conta:
                return
        else:
            return

    try:
        valor = float(input("Informe o Valor do Depósito: ").strip())
    except ValueError:
        print("\nValor inválido.")
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes, contas):
    cpf = input("Informe o CPF do Cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        opcao = input("Deseja cadastrar um novo cliente com esse CPF? (s/n): ").strip().lower()
        if opcao == "s":
            cliente = criar_cliente(clientes, cpf)
        else:
            return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        opcao = input("Cliente não possui conta. Deseja criar uma nova conta agora? (s/n): ").strip().lower()
        if opcao == "s":
            conta = criar_conta(len(contas) + 1, clientes, contas, cpf=cliente.cpf)
            if not conta:
                return
        else:
            return

    try:
        valor = float(input("Informe o valor para saque: ").strip())
    except ValueError:
        print("\nValor inválido.")
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes, contas):
    cpf = input("Informe o CPF do Cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        opcao = input("Deseja cadastrar um novo cliente com esse CPF? (s/n): ").strip().lower()
        if opcao == "s":
            cliente = criar_cliente(clientes, cpf)
        else:
            return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\nCliente não possui conta.")
        opcao = input("Deseja criar uma conta agora? (s/n): ").strip().lower()
        if opcao == "s":
            conta = criar_conta(len(contas) + 1, clientes, contas, cpf=cliente.cpf)
            if not conta:
                return
        else:
            return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações, até o momento."
    else:
        for t in transacoes:
            extrato += f"\n{t['tipo']}:\n\tR$ {t['valor']:.2f} em {t['data']}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return

    for conta in contas:
        print("=" * 40)
        print(conta)  # __str__ do ContaCorrente já formata
        print("=" * 40)


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu().strip()

        if opcao == "0":
            depositar(clientes, contas)

        elif opcao == "1":
            sacar(clientes, contas)

        elif opcao == "2":
            exibir_extrato(clientes, contas)

        elif opcao == "3":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "4":
            listar_contas(contas)

        elif opcao == "5":
            criar_cliente(clientes)

        elif opcao == "6":
            print("\nEncerrando. Até mais!")
            break

        else:
            print("Por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()