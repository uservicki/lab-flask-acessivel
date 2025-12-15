from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://dev_user:dev_pass@localhost/todolist_db'
)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'chave_super_secreta_para_flash_msgs'
)

db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Tarefa {self.id}: {self.titulo}>'

@app.route('/')
def index():
    todas_tarefas = Tarefa.query.all()
    return render_template('index.html', tarefas=todas_tarefas)

if __name__ == '__main__':
    app.run(debug=True)
