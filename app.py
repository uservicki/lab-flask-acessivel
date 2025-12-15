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

# Rota para Adicionar Tarefa (Entrada: POST com 'titulo')
@app.route('/adicionar', methods=['POST'])
def adicionar():
    if request.method == 'POST':
        # Entrada: Obtém o valor do input 'titulo'
        titulo = request.form.get('titulo')

        # Qualidade (Confiabilidade): Validação de entrada
        if not titulo:
            flash('O título da tarefa não pode estar vazio.', 'error')
            return redirect(url_for('index'))

        # Segurança (OWASP A03: Injection)
        nova_tarefa = Tarefa(titulo=titulo)

        db.session.add(nova_tarefa)
        db.session.commit()

    return redirect(url_for('index'))


# Rota para Alternar Conclusão
@app.route('/alternar/<int:tarefa_id>', methods=['POST'])
def alternar(tarefa_id):
    tarefa = db.get_or_404(Tarefa, tarefa_id)

    tarefa.concluida = not tarefa.concluida
    db.session.commit()

    return redirect(url_for('index'))


# Rota para Deletar Tarefa
@app.route('/deletar/<int:tarefa_id>', methods=['POST'])
def deletar(tarefa_id):
    tarefa = db.get_or_404(Tarefa, tarefa_id)

    db.session.delete(tarefa)
    db.session.commit()

    flash('Tarefa excluída.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
