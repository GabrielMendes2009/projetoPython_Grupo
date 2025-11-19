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

class Restaurante:
    def __init__(self, nome):
        self.nome = nome
        self.horario = "08:00 - 22:00"
        self.max_clientes_por_hora = 50
        self.menu = []
        self.pedidos = []
        self.reservas = []

    def definir_horario(self, novo_horario):
        self.horario = novo_horario

    def definir_max_clientes(self, max_clientes):
        self.max_clientes_por_hora = max_clientes

    def adicionar_prato(self, prato):
        self.menu.append(prato)

    def remover_prato(self, nome_prato):
        self.menu = [prato for prato in self.menu if prato.nome != nome_prato]

    def consultar_pedidos(self):
        return self.pedidos

    def consultar_menu(self):
        return self.menu

    def fazer_reserva(self, cliente, num_pessoas, data_hora):
        total_reservado = sum(r.num_pessoas for r in self.reservas if r.data_hora == data_hora)
        if total_reservado + num_pessoas > self.max_clientes_por_hora:
            return None
        reserva = Reserva(cliente, num_pessoas, data_hora)
        self.reservas.append(reserva)
        return reserva

    def pedir_pratos(self, cliente, data_hora, nomes_pratos):
        reserva = next((r for r in self.reservas if r.cliente == cliente and r.data_hora == data_hora), None)
        if not reserva:
            return None
        pratos = [p for p in self.menu if p.nome in nomes_pratos]
        pedido = Pedido(cliente, data_hora, pratos)
        self.pedidos.append(pedido)
        return pedido

    def consultar_reservas(self):
        return self.reservas
    


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
    def __init__(self, restaurante):
        self.restaurante = restaurante

    def definir_horario(self, novo_horario):
        self.restaurante.definir_horario(novo_horario)

    def definir_max_clientes(self, max_clientes):
        self.restaurante.definir_max_clientes(max_clientes)

    def adicionar_prato(self, nome, preco):
        prato = Prato(nome, preco)
        self.restaurante.adicionar_prato(prato)

    def remover_prato(self, nome_prato):
        self.restaurante.remover_prato(nome_prato)

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
        return f"{self.nome}{cat}: {self.descricao} - € {self.preco:.2f}"


class MenuApp:
    def __init__(self, gestor, restaurante):
        self.gestor = gestor
        self.restaurante = restaurante

    def mostrar_menu_principal(self):
        while True:
            print("\n--- Menu Principal ---")
            print("1. Menu do Gestor")
            print("2. Menu do Cliente")
            print("3. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.mostrar_menu_gestor()
            elif escolha == '2':
                self.mostrar_menu_cliente()
            elif escolha == '3':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def mostrar_menu_gestor(self):
        while True:
            print("\n--- Menu do Gestor ---")
            print("1. Definir horário do restaurante")
            print("2. Definir número máximo de clientes por hora")
            print("3. Adicionar prato ao menu")
            print("4. Remover prato do menu")
            print("5. Consultar lista de pedidos")
            print("6. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                novo_horario = input("Digite o novo horário (ex.: 08:00 - 22:00): ")
                self.gestor.definir_horario(novo_horario)
                print("Horário atualizado.")
            elif escolha == '2':
                max_clientes = int(input("Digite o número máximo de clientes por hora: "))
                self.gestor.definir_max_clientes(max_clientes)
                print("Número máximo de clientes atualizado.")
            elif escolha == '3':
                nome_prato = input("Digite o nome do prato: ")
                preco_prato = float(input("Digite o preço do prato: "))
                descricao = input("Digite a descrição do prato: ")
                categoria = input("Digite a categoria (opcional): ")
                categoria = categoria if categoria else None
                prato = Prato(nome_prato, preco_prato, descricao, categoria)
                self.gestor.restaurante.adicionar_prato(prato)
                print("Prato adicionado ao menu.")
            elif escolha == '4':
                nome_prato = input("Digite o nome do prato a ser removido: ")
                self.gestor.remover_prato(nome_prato)
                print("Prato removido do menu.")
            elif escolha == '5':
                pedidos = self.gestor.consultar_pedidos()
                if pedidos:
                    print("Lista de Pedidos:")
                    for pedido in pedidos:
                        print(pedido)
                else:
                    print("Nenhum pedido registrado.")
            elif escolha == '6':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def mostrar_menu_cliente(self):
        nome_cliente = input("Digite seu nome: ")
        cliente = Cliente(nome_cliente, self.restaurante)
        while True:
            print("\n--- Menu do Cliente ---")
            print("1. Consultar menu do restaurante")
            print("2. Fazer reserva")
            print("3. Pedir pratos")
            print("4. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                pratos = cliente.consultar_menu()
                if pratos:
                    print("Menu do Restaurante:")
                    for prato in pratos:
                        print(prato)
                else:
                    print("Menu vazio.")
            elif escolha == '2':
                num_pessoas = int(input("Número de pessoas: "))
                data_hora = input("Data e hora da reserva (ex: 2025-11-19 19:00): ")
                reserva = cliente.fazer_reserva(num_pessoas, data_hora)
                if reserva:
                    print("Reserva realizada com sucesso!")
                else:
                    print("Não há capacidade disponível para essa hora.")
            elif escolha == '3':
                data_hora = input("Data e hora da reserva para o pedido: ")
                nomes_pratos = input("Digite os nomes dos pratos separados por vírgula: ").split(",")
                nomes_pratos = [n.strip() for n in nomes_pratos]
                pedido = cliente.pedir_pratos(data_hora, nomes_pratos)
                if pedido:
                    print("Pedido realizado com sucesso!")
                else:
                    print("Reserva não encontrada para esse horário ou pratos inválidos.")
            elif escolha == '4':
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    restaurante = Restaurante("Restaurante Exemplo")
    gestor = Gestor(restaurante)
    menu_app = MenuApp(gestor, restaurante)
    menu_app.mostrar_menu_principal()