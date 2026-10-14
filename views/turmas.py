from models import Turmas, Alunos, Disciplinas, Professores

class ViewTurmas():
    def __init__(self):
        self.turmas = Turmas()

    def getTotalTurmas(self):
        return len(self.turmas.listar_turmas())

    def getTotalAlunos(self):
        alunos = Alunos()
        return len(alunos.listar_alunos())

    def getTotalProfessores(self):
        professores = Professores()
        return len(professores.listar_professores())

    def getTotalDisciplinas(self):
        disciplinas = Disciplinas()
        return len(disciplinas.listar_disciplinas())

    def getTurmas(self):
        return self.turmas.listar_turmas()

