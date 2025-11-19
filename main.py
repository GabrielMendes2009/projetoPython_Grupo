"""
Nome: Gabriel Mendes, Diogo Dias, Rodrigo Pereira
Turma: PIPL0924
Trabalho: Trabalho Prático Sistema de Gestão de Restaurante (App)
"""

class Restaurante:
    def __init__(self, nome):
        self.nome = nome
        self.horario = "08:00 - 22:00"
        self.max_clientes_por_hora = 50
        self.menu = []
        self.pedidos = []

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
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class MenuApp:
    def __init__(self, gestor):
        self.gestor = gestor

    def mostrar_menu_principal(self):
        while True:
            print("\n--- Menu Principal ---")
            print("1. Menu do Gestor")
            print("2. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.mostrar_menu_gestor()
            elif escolha == '2':
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
                self.gestor.adicionar_prato(nome_prato, preco_prato)
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

if __name__ == "__main__":
    restaurante = Restaurante("Restaurante Exemplo")
    gestor = Gestor(restaurante)
    menu_app = MenuApp(gestor)
    menu_app.mostrar_menu_principal()

