from models import Turmas, Alunos, Disciplinas, Professores

class ViewHome():
    def __init__(self):
        self.turmas = Turmas()
        self.alunos = Alunos()
        self.professores = Professores()
        self.disciplinas = Disciplinas()

    def getTotalTurmas(self):
        return self.turmas.query.count()

    def getTotalAlunos(self):
        return self.alunos.query.count()

    def getTotalProfessores(self):
        return self.professores.query.count()

    def getTotalDisciplinas(self):
        return self.disciplinas.query.count()