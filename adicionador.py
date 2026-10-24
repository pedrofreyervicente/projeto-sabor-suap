class Turma:
    def __init__(self, id_turma, nome, ano):
        self.id_turma = id_turma
        self.nome = nome
        self.ano = ano

    def __str__(self) -> str:
        return f"Turma {self.nome} ({self.ano}) - ID: {self.id_turma}"


class Disciplina:
    def __init__(self, id_disciplina, nome, turma: Turma = None):
        self.id_disciplina = id_disciplina
        self.nome = nome
        self.turma = turma

    def __str__(self) -> str:
        turma_info = self.turma.nome if self.turma else "Nenhuma"
        return f"Disciplina {self.nome} - ID: {self.id_disciplina} | Turma: {turma_info}"


class Aluno:
    def __init__(self, id_aluno, nome, data_nascimento, turma: Turma):
        self.id_aluno = id_aluno
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.turma = turma

    def __str__(self) -> str:
        return f"Aluno: {self.nome} (ID: {self.id_aluno}) - Turma: {self.turma.nome}"


class Professor:
    def __init__(self, id_professor, nome, disciplina: Disciplina):
        self.id_professor = id_professor
        self.nome = nome
        self.disciplina = disciplina

    def __str__(self) -> str:
        return f"Professor: {self.nome} (ID: {self.id_professor}) - Disciplina: {self.disciplina.nome}"


lista_turmas = []
lista_disciplinas = []
lista_alunos = []
lista_professores = []

quantidade = int(input("Quantas matérias/registros você deseja inserir?\n"))

for i in range(1, quantidade + 1):
    print(f"\n--- Cadastro da Matéria {i} ---")

    t = Turma(
        input("Digite o ID da turma:\n"),
        input("Digite o curso da turma junto do ano letivo:\n(Ex.: INFO2)\n"),
        input("Digite o ano atual:\n")
    )
    lista_turmas.append(t)

    d = Disciplina(
        i,
        input("Digite a matéria do professor:\n"),
        turma=t
    )
    lista_disciplinas.append(d)

    a = Aluno(
        input("Digite o ID do aluno:\n"),
        input("Digite o nome do(a) aluno(a):\n"),
        input("Digite a data de nascimento do aluno:\n"),
        turma=t
    )
    lista_alunos.append(a)

    p = Professor(
        id_professor=input("Digite o ID do professor:\n"),
        nome=input("Digite o nome do professor:\n"),
        disciplina=d
    )
    lista_professores.append(p)

print("\n\n=== RESUMO DOS CADASTROS ===")
for i in range(quantidade):
    print(f"\nRegistro {i + 1}:")
    print(lista_turmas[i])
    print(lista_disciplinas[i])
    print(lista_alunos[i])
    print(lista_professores[i])