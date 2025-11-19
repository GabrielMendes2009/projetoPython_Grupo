"""
Nome: Gabriel Mendes, Diogo Dias, Rodrigo Pereira
Turma: PIPL0924
Trabalho: Projeto de Gestão de Restaurante
"""

def pedir_int(msg):
    while True:
        valor = input(msg)
        if valor.isdigit():
            return int(valor)
        print("Erro: introduza um número inteiro.\n")

def pedir_float(msg):
    while True:
        valor = input(msg)
        try:
            return float(valor)
        except ValueError:
            print("Erro: introduza um número válido (ex: 12.50).\n")

class Reserva:
    def __init__(self, cliente, num_pessoas, data_hora):
        self.cliente = cliente
        self.num_pessoas = num_pessoas
        self.data_hora = data_hora

class Pedido:
    def __init__(self, cliente, data_hora, pratos):
        self.cliente = cliente
        self.data_hora = data_hora
        self.pratos = pratos
        self.estado = "Pendente"

    def __str__(self):
        pratos_str = ", ".join([p.nome for p in self.pratos])
        return f"Cliente: {self.cliente}, Hora: {self.data_hora}, Pratos: {pratos_str}, Estado: {self.estado}"

    def atualizar_estado(self, novo_estado):
        if novo_estado in ["Pendente", "Em preparação", "Concluído"]:
            self.estado = novo_estado

class Restaurante:
    def __init__(self, nome):
        self.nome = nome
        self.horario = "08:00 - 22:00"
        self.max_clientes_por_hora = 50
        self.menu = []
        self.reservas = []
        self.pedidos = []

    def definir_horario(self, novo_horario):
        self.horario = novo_horario

    def definir_max_clientes(self, max_clientes):
        self.max_clientes_por_hora = max_clientes

    def adicionar_prato(self, prato):
        self.menu.append(prato)
        print(f"Prato '{prato.nome}' adicionado com sucesso.\n")

    def remover_prato(self, nome_prato):
        encontrado = False
        for p in self.menu:
            if p.nome == nome_prato:
                self.menu.remove(p)
                print(f"Prato '{nome_prato}' removido com sucesso.\n")
                encontrado = True
                break
        if not encontrado:
            print(f"Erro: prato '{nome_prato}' não existe no menu.\n")

    def atualizar_preco_prato(self, nome_prato, novo_preco):
        encontrado = False
        for p in self.menu:
            if p.nome == nome_prato:
                p.preco = novo_preco
                print(f"Preço do prato '{nome_prato}' atualizado para {novo_preco:.2f} €.\n")
                encontrado = True
                break
        if not encontrado:
            print(f"Erro: prato '{nome_prato}' não existe.\n")

    def consultar_menu(self):
        return self.menu

    def fazer_reserva(self, cliente, num_pessoas, data_hora):
        total = sum(r.num_pessoas for r in self.reservas if r.data_hora == data_hora)
        if total + num_pessoas > self.max_clientes_por_hora:
            restante = self.max_clientes_por_hora - total
            print(f"Erro: capacidade máxima excedida. Só há espaço para {restante} pessoas nesse horário.\n")
            return None
        reserva = Reserva(cliente, num_pessoas, data_hora)
        self.reservas.append(reserva)
        print(f"Reserva criada para {cliente}, {num_pessoas} pessoas às {data_hora}.\n")
        return reserva

    def pedir_pratos(self, cliente, data_hora, nomes_pratos):
        reserva = next((r for r in self.reservas if r.cliente == cliente and r.data_hora == data_hora), None)
        if not reserva:
            print("Erro: não existe uma reserva com esse nome nesse horário.\n")
            return None

        pratos = []
        invalidos = []
        for nome in nomes_pratos:
            prato = next((p for p in self.menu if p.nome == nome), None)
            if prato:
                pratos.append(prato)
            else:
                invalidos.append(nome)

        if invalidos:
            print("Erro: os seguintes pratos não existem no menu:")
            for p in invalidos:
                print(f"- {p}")
            print("")
            return None

        pedido = Pedido(cliente, data_hora, pratos)
        self.pedidos.append(pedido)
        print(f"Pedido registado para {cliente} às {data_hora}.\n")
        return pedido

    def consultar_pedidos(self):
        return self.pedidos

class Cliente:
    def __init__(self, nome, restaurante):
        self.nome = nome
        self.restaurante = restaurante

    def consultar_menu(self):
        return self.restaurante.consultar_menu()

    def fazer_reserva(self, num_pessoas, data_hora):
        return self.restaurante.fazer_reserva(self.nome, num_pessoas, data_hora)

    def pedir_pratos(self, data_hora, nomes_pratos):
        return self.restaurante.pedir_pratos(self.nome, data_hora, nomes_pratos)

class Gestor:
    def __init__(self, restaurante, password="1234"):
        self.restaurante = restaurante
        self.password = password

    def autenticar(self):
        senha = input("Introduza a palavra-passe do gestor: ")
        return senha == self.password

    def definir_horario(self, novo_horario):
        self.restaurante.definir_horario(novo_horario)
        print(f"Horário definido para {novo_horario}.\n")

    def definir_max_clientes(self, max_clientes):
        self.restaurante.definir_max_clientes(max_clientes)
        print(f"Capacidade máxima definida para {max_clientes} clientes/hora.\n")

    def adicionar_prato(self, nome, preco, descricao="", categoria=None):
        self.restaurante.adicionar_prato(Prato(nome, preco, descricao, categoria))

    def remover_prato(self, nome_prato):
        self.restaurante.remover_prato(nome_prato)

    def atualizar_preco_prato(self, nome_prato, novo_preco):
        self.restaurante.atualizar_preco_prato(nome_prato, novo_preco)

    def consultar_pedidos(self):
        return self.restaurante.consultar_pedidos()

class Prato:
    def __init__(self, nome, preco, descricao="", categoria=None):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria

    def __str__(self):
        cat = f" ({self.categoria})" if self.categoria else ""
        return f"{self.nome}{cat}: {self.descricao} - {self.preco:.2f} €"

class MenuApp:
    def __init__(self, gestor, restaurante):
        self.gestor = gestor
        self.restaurante = restaurante

    def mostrar_menu_principal(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Entrar como Gestor")
            print("2. Entrar como Cliente")
            print("0. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                if self.gestor.autenticar():
                    self.mostrar_menu_gestor()
                else:
                    print("Palavra-passe incorreta.\n")
            elif escolha == "2":
                self.mostrar_menu_cliente()
            elif escolha == "0":
                print("A encerrar a aplicação...")
                break
            else:
                print("Opção inválida.\n")

    def mostrar_menu_gestor(self):
        while True:
            print("\n--- MENU DO GESTOR ---")
            print("1. Definir horário")
            print("2. Definir capacidade máxima")
            print("3. Adicionar prato")
            print("4. Remover prato")
            print("5. Atualizar preço de prato")
            print("6. Consultar pedidos")
            print("0. Voltar")
            escolha = input("Escolha: ")

            if escolha == "1":
                novo = input("Novo horário (ex: 08:00 - 22:00): ")
                self.gestor.definir_horario(novo)
            elif escolha == "2":
                max_c = pedir_int("Máx. clientes/hora: ")
                self.gestor.definir_max_clientes(max_c)
            elif escolha == "3":
                nome = input("Nome do prato: ")
                preco = pedir_float("Preço: ")
                desc = input("Descrição: ")
                cat = input("Categoria: ")
                self.gestor.adicionar_prato(nome, preco, desc, cat)
            elif escolha == "4":
                nome = input("Nome do prato a remover: ")
                self.gestor.remover_prato(nome)
            elif escolha == "5":
                nome = input("Nome do prato: ")
                preco = pedir_float("Novo preço: ")
                self.gestor.atualizar_preco_prato(nome, preco)
            elif escolha == "6":
                pedidos = self.gestor.consultar_pedidos()
                if not pedidos:
                    print("Nenhum pedido registado.\n")
                else:
                    print("\n--- PEDIDOS ---")
                    for p in pedidos:
                        print(p)
                    print("")
            elif escolha == "0":
                break
            else:
                print("Opção inválida.\n")

    def mostrar_menu_cliente(self):
        nome = input("Nome do cliente: ")
        cliente = Cliente(nome, self.restaurante)

        while True:
            print("\n--- MENU DO CLIENTE ---")
            print("1. Consultar menu")
            print("2. Fazer reserva")
            print("3. Pedir pratos")
            print("0. Voltar")
            escolha = input("Escolha: ")

            if escolha == "1":
                menu = cliente.consultar_menu()
                if not menu:
                    print("Menu vazio.\n")
                else:
                    print("\n--- MENU ---")
                    for prato in menu:
                        print(prato)
                    print("")
            elif escolha == "2":
                num = pedir_int("Número de pessoas: ")
                data_hora = input("Data e hora (AAAA-MM-DD HH:MM): ")
                cliente.fazer_reserva(num, data_hora)
            elif escolha == "3":
                data_hora = input("Data e hora da reserva: ")
                nomes = input("Pratos separados por vírgula: ").split(",")
                nomes = [n.strip() for n in nomes]
                cliente.pedir_pratos(data_hora, nomes)
            elif escolha == "0":
                break
            else:
                print("Opção inválida.\n")

if __name__ == "__main__":
    restaurante = Restaurante("Restaurante Simples")
    gestor = Gestor(restaurante)
    app = MenuApp(gestor, restaurante)
    app.mostrar_menu_principal()
