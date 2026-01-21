# app/routes.py
from flask import current_app as app, render_template, request, redirect, url_for, flash
from . import tabelas

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html', title='Login')

@app.route('/')
def index():
    return render_template('index.html', title='Página Inicial')

@app.route('/alunos')
def alunos():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = tabelas.listar_alunos(query, page, per_page)
    return render_template('alunos.html', title='Gestão de Alunos', alunos=pagination['items'], pagination=pagination, query=query)

@app.route('/alunos/novo', methods=['GET', 'POST'])
def novo_aluno():
    if request.method == 'POST':
        try:
            tabelas.criar_aluno(request.form)
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('alunos'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('novo_aluno.html', title='Inserir Novo Aluno', form_data=request.form)
    
    return render_template('novo_aluno.html', title='Inserir Novo Aluno', form_data=None)

@app.route('/aluno/editar/<int:aluno_id>', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    if request.method == 'POST':
        tabelas.atualizar_aluno(aluno_id, request.form)
        flash('Aluno atualizado com sucesso!', 'success')
        return redirect(url_for('alunos'))
    
    aluno = tabelas.obter_aluno(aluno_id)
    return render_template('editar_aluno.html', title='Editar Aluno', aluno=aluno)

@app.route('/aluno/visualizar/<int:aluno_id>')
def visualizar_aluno(aluno_id):
    aluno = tabelas.obter_aluno(aluno_id)
    return render_template('visualizar_aluno.html', title='Visualizar Aluno', aluno=aluno)

@app.route('/aluno/excluir/<int:aluno_id>', methods=['POST'])
def excluir_aluno(aluno_id):
    tabelas.excluir_aluno(aluno_id)
    flash('Aluno excluído com sucesso!', 'success')
    return redirect(url_for('alunos'))

@app.route('/professores')
def professores():
    professores = tabelas.listar_professores()
    return render_template('professores.html', title='Gestão de Professores', professores=professores)

@app.route('/professores/novo', methods=['GET', 'POST'])
def novo_professor():
    if request.method == 'POST':
        try:
            tabelas.criar_professor(request.form)
            flash('Professor cadastrado com sucesso!', 'success')
            return redirect(url_for('professores'))
        except Exception as e:
            flash(f'Erro ao cadastrar professor: {e}', 'error')
            return render_template('novo_professor.html', title='Novo Professor', form_data=request.form)
    return render_template('novo_professor.html', title='Novo Professor', form_data=None)

# Manter rotas placeholder para funcionalidades futuras, mas sem lógica complexa
@app.route('/cursos')
def cursos():
    return render_template('cursos.html', title='Gestão de Cursos')

@app.route('/financeiro')
def financeiro():
    return render_template('financeiro.html', title='Gestão Financeira')
