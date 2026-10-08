from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost:3306/suap'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Professores(db.Model):
    __tablename__ = 'professores'

    idProfessor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    def listar_professores(self):
        professores = Professores.query.all()
        return professores

@app.route("/")
def home():
    professores = Professores().listar_professores()

    html_template = """
    <h1>Projeto Sabor SUAP</h1>
    <ul>
        {% for professor in professores %}
            <li>{{ professor.idProfessor }} - {{ professor.nome }}</li>
        {% endfor %}
    </ul>
    <p>Bem-vindo ao projeto inicial.</p>
    """

    return render_template_string(html_template, professores=professores)


if __name__ == "__main__":
    app.run(debug=True)
