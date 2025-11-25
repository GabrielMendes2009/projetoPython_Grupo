"""
Nome: Gabriel Mendes, Diogo Dias, Rodrigo Pereira
Turma: PIPL0924
Trabalho: Projeto de Gestão de Restaurante
"""

# --- Funções de Validação de Entrada ---
def pedir_int(msg):
    """Pede um valor ao usuário e garante que seja um número inteiro."""
    while True:
        valor = input(msg)
        # Verifica se a string contém apenas dígitos
        if valor.isdigit():
            return int(valor) # Converte e retorna o valor como inteiro
        print("Erro: introduza um número inteiro.\n") # Mensagem de erro se não for dígito

def pedir_float(msg):
    """Pede um valor ao usuário e garante que seja um número de ponto flutuante (float)."""
    while True:
        valor = input(msg)
        try:
            # Tenta converter o valor para float
            return float(valor)
        except ValueError:
            # Captura o erro se a conversão falhar (ex: texto inserido)
            print("Erro: introduza um número válido (ex: 12.50).\n")

# --- Classes de Entidades ---
class Reserva:
    """Representa uma reserva de mesa no restaurante."""
    def __init__(self, cliente, num_pessoas, data_hora):
        # Inicializa a reserva com o nome do cliente
        self.cliente = cliente
        # Número de pessoas na reserva
        self.num_pessoas = num_pessoas
        # Data e hora da reserva (armazenada como string)
        self.data_hora = data_hora

class Pedido:
    """Representa um pedido de pratos feito por um cliente."""
    def __init__(self, cliente, data_hora, pratos):
        self.cliente = cliente
        self.data_hora = data_hora
        # Lista de objetos Prato que compõem o pedido
        self.pratos = pratos
        # Estado inicial do pedido é "Pendente"
        self.estado = "Pendente"

    def __str__(self):
        """Define como o objeto Pedido deve ser representado como string (para impressão)."""
        # Cria uma string com os nomes dos pratos separados por vírgula
        pratos_str = ", ".join([p.nome for p in self.pratos])
        # Retorna uma string formatada com os detalhes do pedido
        return f"Cliente: {self.cliente}, Hora: {self.data_hora}, Pratos: {pratos_str}, Estado: {self.estado}"

    def atualizar_estado(self, novo_estado):
        """Atualiza o estado do pedido, validando se o novo estado é permitido."""
        # Verifica se o novo estado está na lista de estados válidos
        if novo_estado in ["Pendente", "Em preparação", "Concluído"]:
            self.estado = novo_estado

class Restaurante:
    """A classe principal que gerencia o menu, reservas e pedidos."""
    def __init__(self, nome):
        self.nome = nome
        # Horário padrão de funcionamento
        self.horario = "08:00 - 22:00"
        # Capacidade máxima de clientes por hora
        self.max_clientes_por_hora = 50
        # Lista para armazenar objetos Prato
        self.menu = []
        # Lista para armazenar objetos Reserva
        self.reservas = []
        # Lista para armazenar objetos Pedido
        self.pedidos = []

    # --- Métodos de Configuração ---

    def definir_horario(self, novo_horario):
        """Define um novo horário de funcionamento."""
        self.horario = novo_horario

    def definir_max_clientes(self, max_clientes):
        """Define a capacidade máxima de clientes por hora."""
        self.max_clientes_por_hora = max_clientes

    # --- Métodos de Gestão de Menu ---

    def adicionar_prato(self, prato):
        """Adiciona um objeto Prato ao menu."""
        self.menu.append(prato)
        print(f"Prato '{prato.nome}' adicionado com sucesso.\n")

    def remover_prato(self, nome_prato):
        """Remove um prato do menu pelo nome."""
        encontrado = False
        # Itera sobre a lista de pratos
        for p in self.menu:
            if p.nome == nome_prato:
                self.menu.remove(p) # Remove o prato
                print(f"Prato '{nome_prato}' removido com sucesso.\n")
                encontrado = True
                break # Sai do loop após remover o prato
        if not encontrado:
            print(f"Erro: prato '{nome_prato}' não existe no menu.\n")

    def atualizar_preco_prato(self, nome_prato, novo_preco):
        """Atualiza o preço de um prato existente."""
        encontrado = False
        for p in self.menu:
            if p.nome == nome_prato:
                p.preco = novo_preco # Atualiza o atributo preco do objeto Prato
                print(f"Preço do prato '{nome_prato}' atualizado para {novo_preco:.2f} €.\n")
                encontrado = True
                break
        if not encontrado:
            print(f"Erro: prato '{nome_prato}' não existe.\n")

    def consultar_menu(self):
        """Retorna a lista completa de pratos no menu."""
        return self.menu

    # --- Métodos de Gestão de Reserva ---
    def fazer_reserva(self, cliente, num_pessoas, data_hora):
        """Cria uma nova reserva, verificando a capacidade do restaurante."""
        # Calcula o total de pessoas já reservadas para a mesma data/hora
        total = sum(r.num_pessoas for r in self.reservas if r.data_hora == data_hora)
        
        # Verifica se a nova reserva excede a capacidade máxima
        if total + num_pessoas > self.max_clientes_por_hora:
            restante = self.max_clientes_por_hora - total
            print(f"Erro: capacidade máxima excedida. Só há espaço para {restante} pessoas nesse horário.\n")
            return None # Retorna None se a reserva não puder ser feita
            
        # Cria o objeto Reserva
        reserva = Reserva(cliente, num_pessoas, data_hora)
        self.reservas.append(reserva) # Adiciona à lista de reservas
        print(f"Reserva criada para {cliente}, {num_pessoas} pessoas às {data_hora}.\n")
        return reserva

    # --- Métodos de Gestão de Pedido ---
    def pedir_pratos(self, cliente, data_hora, nomes_pratos):
        """Registra um pedido de pratos, associado a uma reserva existente."""
        # Busca a reserva do cliente para a data/hora especificada.
        # Usa 'next' para buscar o primeiro item que satisfaz a condição, ou None se não encontrar.
        reserva = next((r for r in self.reservas if r.cliente == cliente and r.data_hora == data_hora), None)
        
        if not reserva:
            print("Erro: não existe uma reserva com esse nome nesse horário.\n")
            return None

        pratos = []
        invalidos = []
        # Itera sobre os nomes de pratos solicitados
        for nome in nomes_pratos:
            # Busca o objeto Prato correspondente no menu
            prato = next((p for p in self.menu if p.nome == nome), None)
            if prato:
                pratos.append(prato) # Adiciona o objeto Prato à lista
            else:
                invalidos.append(nome) # Registra pratos não encontrados

        if invalidos:
            print("Erro: os seguintes pratos não existem no menu:")
            for p in invalidos:
                print(f"- {p}")
            print("")
            return None # Retorna None se houver pratos inválidos

        # Cria o objeto Pedido com os pratos válidos
        pedido = Pedido(cliente, data_hora, pratos)
        self.pedidos.append(pedido) # Adiciona à lista de pedidos
        print(f"Pedido registado para {cliente} às {data_hora}.\n")
        return pedido

    def consultar_pedidos(self):
        """Retorna a lista completa de pedidos."""
        return self.pedidos

class Cliente:
    """Representa um cliente e suas ações no sistema."""
    def __init__(self, nome, restaurante):
        self.nome = nome
        # O cliente tem acesso ao objeto Restaurante para realizar ações
        self.restaurante = restaurante

    def consultar_menu(self):
        """Delega a consulta do menu ao objeto Restaurante."""
        return self.restaurante.consultar_menu()

    def fazer_reserva(self, num_pessoas, data_hora):
        """Delega a criação da reserva ao Restaurante, passando o próprio nome."""
        return self.restaurante.fazer_reserva(self.nome, num_pessoas, data_hora)

    def pedir_pratos(self, data_hora, nomes_pratos):
        """Delega o pedido de pratos ao Restaurante, passando o próprio nome."""
        return self.restaurante.pedir_pratos(self.nome, data_hora, nomes_pratos)

class Gestor:
    """Representa o gestor do restaurante e suas ações administrativas."""
    def __init__(self, restaurante, password="1234"):
        self.restaurante = restaurante
        # Palavra-passe de acesso (simples, hardcoded)
        self.password = password

    def autenticar(self):
        """Verifica a palavra-passe para permitir acesso ao menu do gestor."""
        senha = input("Introduza a palavra-passe do gestor: ")
        return senha == self.password # Retorna True se a senha estiver correta

    # --- Métodos de Gestão (Fachada para Restaurante) ---
    def definir_horario(self, novo_horario):
        self.restaurante.definir_horario(novo_horario)
        print(f"Horário definido para {novo_horario}.\n")

    def definir_max_clientes(self, max_clientes):
        self.restaurante.definir_max_clientes(max_clientes)
        print(f"Capacidade máxima definida para {max_clientes} clientes/hora.\n")

    def adicionar_prato(self, nome, preco, descricao="", categoria=None):
        # Cria um novo objeto Prato e o adiciona ao Restaurante
        self.restaurante.adicionar_prato(Prato(nome, preco, descricao, categoria))

    def remover_prato(self, nome_prato):
        self.restaurante.remover_prato(nome_prato)

    def atualizar_preco_prato(self, nome_prato, novo_preco):
        self.restaurante.atualizar_preco_prato(nome_prato, novo_preco)

    def consultar_pedidos(self):
        return self.restaurante.consultar_pedidos()

class Prato:
    """Representa um item individual no menu do restaurante."""
    def __init__(self, nome, preco, descricao="", categoria=None):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria

    def __str__(self):
        """Define a representação em string do Prato para exibição no menu."""
        # Adiciona a categoria se ela existir
        cat = f" ({self.categoria})" if self.categoria else ""
        # Formata o preço com duas casas decimais e o símbolo de Euro
        return f"{self.nome}{cat}: {self.descricao} - {self.preco:.2f} €"

# --- Interface de Usuário (MenuApp) ---
class MenuApp:
    """Gerencia a interface de linha de comando e a navegação entre menus."""
    def __init__(self, gestor, restaurante):
        self.gestor = gestor
        self.restaurante = restaurante

    def mostrar_menu_principal(self):
        """Loop principal para escolher entre Gestor e Cliente."""
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Entrar como Gestor")
            print("2. Entrar como Cliente")
            print("0. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                # Tenta autenticar o gestor
                if self.gestor.autenticar():
                    self.mostrar_menu_gestor() # Se autenticado, entra no menu do gestor
                else:
                    print("Palavra-passe incorreta.\n")
            elif escolha == "2":
                self.mostrar_menu_cliente() # Entra no menu do cliente
            elif escolha == "0":
                print("A encerrar a aplicação...")
                break # Sai do loop principal
            else:
                print("Opção inválida.\n")

    def mostrar_menu_gestor(self):
        """Loop para as ações administrativas do gestor."""
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
                # Usa a função de validação para garantir que a entrada é um inteiro
                max_c = pedir_int("Máx. clientes/hora: ")
                self.gestor.definir_max_clientes(max_c)
            elif escolha == "3":
                nome = input("Nome do prato: ")
                # Usa a função de validação para garantir que a entrada é um float
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
                    # Imprime cada pedido usando o método __str__ da classe Pedido
                    for p in pedidos:
                        print(p)
                    print("")
            elif escolha == "0":
                break # Volta ao menu principal
            else:
                print("Opção inválida.\n")

    def mostrar_menu_cliente(self):
        """Loop para as ações do cliente."""
        nome = input("Nome do cliente: ")
        # Cria uma instância de Cliente para o usuário atual
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
                    # Imprime cada prato usando o método __str__ da classe Prato
                    for prato in menu:
                        print(prato)
                    print("")
            elif escolha == "2":
                num = pedir_int("Número de pessoas: ")
                data_hora = input("Data e hora (AAAA-MM-DD HH:MM): ")
                cliente.fazer_reserva(num, data_hora) # Chama o método que delega ao Restaurante
            elif escolha == "3":
                data_hora = input("Data e hora da reserva: ")
                nomes = input("Pratos separados por vírgula: ").split(",") # Pega a lista de pratos
                nomes = [n.strip() for n in nomes] # Remove espaços em branco de cada nome
                cliente.pedir_pratos(data_hora, nomes) # Chama o método que delega ao Restaurante
            elif escolha == "0":
                break # Volta ao menu principal
            else:
                print("Opção inválida.\n")

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    # Este bloco só é executado se o script for rodado diretamente (não importado)
    # 1. Inicializa o objeto Restaurante
    restaurante = Restaurante("Restaurante Simples")
    
    # 2. Inicializa o objeto Gestor, associando-o ao Restaurante
    gestor = Gestor(restaurante)
    
    # 3. Inicializa a aplicação de menu, passando o Gestor e o Restaurante
    app = MenuApp(gestor, restaurante)
    
    # 4. Inicia o loop principal da aplicação
    app.mostrar_menu_principal()

    