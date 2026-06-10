from datetime import date

# classe geral
class Item:
    def __init__(self, nome):
        self.__nome = nome  #atributo privado

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        self.__nome = nome

    # metodo que será sobrescrito
    def exibir(self):
        return self.__nome


class Tarefa(Item):  # HERANÇA
    def __init__(self, nome, categoria, prioridade, data):
        super().__init__(nome)  #chama o construtor
        self.__categoria = categoria  #atributo privado
        self.__prioridade = prioridade  #atributo privado
        self.__data = data  #atributo privado
        self.__status = None  #atributo privado


    #@property - get


    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, valor):
        self.__categoria = valor

    @property
    def prioridade(self):
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, valor):
        self.__prioridade = valor

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, valor):
        self.__data = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    # retorna como será exibido
    def exibir(self):
        return f"{self.get_nome()} - {self.__categoria}"


class Sistema:
    def __init__(self):
        self.tarefas = []  #lista que armazena os objetos Tarefa
        self.categorias = ["ESCOLA", "TRABALHO", "PESSOAL", "OUTRO"]
        self.prioridades = {
            1: "URGENTE",
            2: "POUCO URGENTE",
            3: "NÃO URGENTE"
        }

    def adicionar_tarefa(self):
        nome = input("Nome da tarefa: ")
        data_texto = input("Data (dd/mm/aaaa): ")

        #converter texto em data
        dia, mes, ano = map(int, data_texto.split("/"))
        data_entrega = date(ano, mes, dia)

        prioridade = int(input("Prioridade (1-URGENTE / 2-POUCO / 3-NÃO): "))
        classificacao = int(input("Categoria (0-ESCOLA / 1-TRABALHO / 2-PESSOAL / 3-OUTRO): "))

        categoria = self.categorias[classificacao]

        #cria objeto da classe Tarefa
        tarefa = Tarefa(nome, categoria, prioridade, data_entrega)

        self.tarefas.append(tarefa)  #adiciona na lista
        print("Tarefa adicionada!")

    def listar_tarefas(self):
        if len(self.tarefas) == 0:
            print("Nenhuma tarefa cadastrada.")
            return

        print("\nTAREFAS:")

        #ordena por data e prioridade
        ordenadas = sorted(self.tarefas, key=lambda t: (t.data, t.prioridade))

        for t in ordenadas:
            status = self.calcular_status(t.data)
            situacao = self.prioridades.get(t.prioridade, "CÓDIGO INEXISTENTE")

            print(
                t.data.strftime("%d/%m/%Y"),
                "-",
                t.exibir(),
                "-",
                status,
                "-",
                situacao,
                "-",
                t.categoria,
            )

    def calcular_status(self, data):
        hoje = date.today()  #pega a data atual

        if data < hoje:
            return "ATRASADA"
        elif data == hoje:
            return "HOJE"
        else:
            dias = (data - hoje).days
            return f"Faltam {dias} dias"

    def remover_tarefa(self):
        self.listar_tarefas()

        nome = input("Digite o nome da tarefa para remover: ")

        for t in self.tarefas:
            if t.get_nome() == nome:
                self.tarefas.remove(t)
                print("Tarefa removida!")
                return

        print("Tarefa não encontrada.")

    #função para listar somente tarefas urgentes
    def ver_urgentes(self):

        urgentes = []  #lista para armazenar tarefas urgentes

        #percorre todas as tarefas
        for t in self.tarefas:
            if t.prioridade == 1:
                urgentes.append(t)

        print("\nTAREFAS URGENTES:")

        if len(urgentes) == 0:
            print("Nenhuma tarefa urgente.")
            return

        #mostra todas as tarefas urgentes
        for t in urgentes:
            print(
                t.data.strftime("%d/%m/%Y"),
                "-",
                t.exibir(),
                "- URGENTE",
            )

    #função para listar tarefas por categoria
    def listar_por_categoria(self):

        print("\nEscolha a categoria:")
        print("0 - ESCOLA")
        print("1 - TRABALHO")
        print("2 - PESSOAL")
        print("3 - OUTRO")

        opcao = int(input("Digite o número da categoria: "))

        if opcao < 0 or opcao > 3:
            print("Categoria inválida.")
            return

        categoria_escolhida = self.categorias[opcao]

        tarefas_filtradas = []  #lista para armazenar filtradas

        for t in self.tarefas:
            if t.categoria == categoria_escolhida:
                tarefas_filtradas.append(t)

        print(f"\nTarefas da categoria {categoria_escolhida}:")

        if len(tarefas_filtradas) == 0:
            print("Nenhuma tarefa nesta categoria.")
            return

        for t in tarefas_filtradas:
            status = self.calcular_status(t.data)
            situacao = self.prioridades.get(t.prioridade, "CÓDIGO INEXISTENTE")

            print(
                t.data.strftime("%d/%m/%Y"),
                "-",
                t.exibir(),
                "-",
                status,
                "-",
                situacao,
                "-",
                t.categoria,
            )

    def editar_tarefa(self):

        self.listar_tarefas()

        nome = input("Digite o nome da tarefa que deseja editar: ")

        for t in self.tarefas:
            if t.get_nome() == nome:

                print("1 - Alterar nome")
                print("2 - Alterar data")
                print("3 - Alterar prioridade")
                print("4 - Alterar categoria")

                op = input("Escolha: ")

                if op == "1":
                    novo_nome = input("Novo nome: ")
                    t.set_nome(novo_nome)

                elif op == "2":
                    data_texto = input("Nova data (dd/mm/aaaa): ")
                    dia, mes, ano = map(int, data_texto.split("/"))
                    nova_data = date(ano, mes, dia)
                    t.data = nova_data  #usando property

                elif op == "3":
                    nova_prioridade = int(input("Nova prioridade: "))
                    t.prioridade = nova_prioridade  #usando property

                elif op == "4":
                    print("0 - ESCOLA")
                    print("1 - TRABALHO")
                    print("2 - PESSOAL")
                    print("3 - OUTRO")
                    opcao = int(input("Nova categoria: "))
                    t.categoria = self.categorias[opcao]  #usando property

                print("Tarefa atualizada!")
                return

        print("Tarefa não encontrada.")

    #função para salvar tarefas em arquivo texto
    def salvar_tarefas(self):
        if len(self.tarefas) == 0:
            print("Nenhuma tarefa para salvar.")
            return

        #abre/cria arquivo texto
        with open("tarefas.txt", "w", encoding="utf-8") as arquivo:

            #percorre todas as tarefas
            for t in self.tarefas:
                linha = f"{t.get_nome()} | {t.categoria} | {t.prioridade} | {t.data}\n"
                arquivo.write(linha)

        print("Tarefas salvas em tarefas.txt!")

    def menu(self):

        while True:

            print("\n1 - Adicionar")
            print("2 - Listar")
            print("3 - Ver urgentes")
            print("4 - Listar por categoria")
            print("5 - Remover tarefa")
            print("6 - Salvar as tarefas em um arquivo")
            print("7 - Editar tarefa")
            print("0 - Sair")

            op = input("Escolha: ")

            if op == "1":
                self.adicionar_tarefa()

            elif op == "2":
                self.listar_tarefas()

            elif op == "3":
                self.ver_urgentes()

            elif op == "4":
                self.listar_por_categoria()

            elif op == "5":
                self.remover_tarefa()

            elif op == "6":
                self.salvar_tarefas()

            elif op == "7":
                self.editar_tarefa()

            elif op == "0":
                break

            else:
                print("Opção inválida.")


#sistema
if __name__ == "__main__":
    sistema = Sistema()
    sistema.menu()
