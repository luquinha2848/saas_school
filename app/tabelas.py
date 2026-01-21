# app/tabelas.py
from . import db
from datetime import datetime
import math
from flask import current_app

def get_conn():
    """Obtém uma conexão com o banco de dados."""
    return db.engine.raw_connection()

def criar_tabelas():
    """Cria as tabelas essenciais do banco de dados no schema public."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            print("Creating database tables...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS responsavel (
                    id SERIAL PRIMARY KEY,
                    nome_completo VARCHAR(120) NOT NULL,
                    telefone VARCHAR(20) NOT NULL,
                    parentesco VARCHAR(50) NOT NULL,
                    data_cadastro TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS aluno (
                    id SERIAL PRIMARY KEY,
                    nome_completo VARCHAR(120) NOT NULL,
                    data_nascimento DATE NOT NULL,
                    email VARCHAR(120) UNIQUE,
                    telefone VARCHAR(15),
                    data_cadastro TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    ativo BOOLEAN DEFAULT TRUE,
                    responsavel_id INTEGER REFERENCES responsavel(id) ON DELETE SET NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS professor (
                    id SERIAL PRIMARY KEY,
                    nome_completo VARCHAR(120) NOT NULL,
                    cpf VARCHAR(11) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    telefone VARCHAR(15),
                    data_contratacao TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    ativo BOOLEAN DEFAULT TRUE
                );
            """)
            conn.commit()
            print("Database tables created successfully!")
    finally:
        conn.close()

def dict_fetchone(cursor):
    desc = cursor.description
    return dict(zip([col[0] for col in desc], cursor.fetchone())) if desc else None

def dict_fetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] if desc else []

def listar_alunos(query, page, per_page):
    offset = (page - 1) * per_page
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            count_sql = "SELECT COUNT(id) FROM aluno"
            base_sql = "SELECT a.*, r.nome_completo as responsavel_nome FROM aluno a LEFT JOIN responsavel r ON a.responsavel_id = r.id"
            params = []

            if query:
                search_query = f"%{query.upper()}%"
                where_clause = " WHERE UPPER(a.nome_completo) LIKE %s OR UPPER(a.email) LIKE %s"
                count_sql += where_clause
                base_sql += where_clause
                params.extend([search_query, search_query])

            current_app.logger.info(f"Executando SQL: {cur.mogrify(count_sql, tuple(params)).decode('utf-8')}")
            cur.execute(count_sql, tuple(params))
            total = cur.fetchone()[0]

            base_sql += " ORDER BY a.nome_completo LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            current_app.logger.info(f"Executando SQL: {cur.mogrify(base_sql, tuple(params)).decode('utf-8')}")
            cur.execute(base_sql, tuple(params))
            alunos = dict_fetchall(cur)
            
            total_pages = math.ceil(total / per_page) if total > 0 else 0
            pagination = {
                'items': alunos, 'page': page, 'per_page': per_page, 'total': total,
                'pages': total_pages, 'has_prev': page > 1, 'prev_num': page - 1 if page > 1 else None,
                'has_next': page < total_pages, 'next_num': page + 1 if page < total_pages else None,
                'iter_pages': list(range(1, total_pages + 1))
            }
            return pagination
    finally:
        conn.close()

def criar_aluno(form_data):
    nome_completo = form_data['nome_completo'].upper()
    email = form_data['email']
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql_check_email = "SELECT id FROM aluno WHERE email = %s"
            current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_check_email, (email,)).decode('utf-8')}")
            cur.execute(sql_check_email, (email,))
            if cur.fetchone():
                raise ValueError("Este e-mail já está cadastrado.")

            responsavel_id = None
            if form_data.get('menor_idade'):
                sql_insert_responsavel = "INSERT INTO responsavel (nome_completo, telefone, parentesco) VALUES (%s, %s, %s) RETURNING id"
                responsavel_data = (
                    form_data['responsavel_nome'].upper(),
                    form_data['responsavel_telefone'],
                    form_data['responsavel_parentesco']
                )
                current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_insert_responsavel, responsavel_data).decode('utf-8')}")
                cur.execute(sql_insert_responsavel, responsavel_data)
                responsavel_id = cur.fetchone()[0]

            sql_insert_aluno = "INSERT INTO aluno (nome_completo, data_nascimento, email, telefone, responsavel_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
            aluno_data = (
                nome_completo, datetime.strptime(form_data['data_nascimento'], '%Y-%m-%d').date(),
                email, form_data['telefone'], responsavel_id
            )
            current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_insert_aluno, aluno_data).decode('utf-8')}")
            cur.execute(sql_insert_aluno, aluno_data)
            aluno_id = cur.fetchone()[0]

            conn.commit()
            current_app.logger.info(f"Aluno {nome_completo} cadastrado com sucesso!")
            return {'id': aluno_id, 'nome_completo': nome_completo}
    finally:
        conn.close()

def obter_aluno(aluno_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = "SELECT a.*, r.nome_completo as responsavel_nome, r.telefone as responsavel_telefone, r.parentesco as responsavel_parentesco FROM aluno a LEFT JOIN responsavel r ON a.responsavel_id = r.id WHERE a.id = %s;"
            current_app.logger.info(f"Executando SQL: {cur.mogrify(sql, (aluno_id,)).decode('utf-8')}")
            cur.execute(sql, (aluno_id,))
            aluno = dict_fetchone(cur)
            if not aluno:
                from werkzeug.exceptions import NotFound
                raise NotFound()
            return aluno
    finally:
        conn.close()

def atualizar_aluno(aluno_id, form_data):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql_select_responsavel = "SELECT responsavel_id FROM aluno WHERE id = %s"
            current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_select_responsavel, (aluno_id,)).decode('utf-8')}")
            cur.execute(sql_select_responsavel, (aluno_id,))
            result = cur.fetchone()
            if not result:
                from werkzeug.exceptions import NotFound
                raise NotFound()

            responsavel_id = result[0]
            if form_data.get('menor_idade'):
                responsavel_data = (
                    form_data['responsavel_nome'].upper(),
                    form_data['responsavel_telefone'],
                    form_data['responsavel_parentesco']
                )
                if responsavel_id:
                    sql_update_responsavel = "UPDATE responsavel SET nome_completo = %s, telefone = %s, parentesco = %s WHERE id = %s"
                    current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_update_responsavel, responsavel_data + (responsavel_id,)).decode('utf-8')}")
                    cur.execute(sql_update_responsavel, responsavel_data + (responsavel_id,))
                else:
                    sql_insert_responsavel = "INSERT INTO responsavel (nome_completo, telefone, parentesco) VALUES (%s, %s, %s) RETURNING id"
                    current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_insert_responsavel, responsavel_data).decode('utf-8')}")
                    cur.execute(sql_insert_responsavel, responsavel_data)
                    responsavel_id = cur.fetchone()[0]
            elif responsavel_id:
                responsavel_id = None

            sql_update_aluno = "UPDATE aluno SET nome_completo = %s, data_nascimento = %s, email = %s, telefone = %s, ativo = %s, responsavel_id = %s WHERE id = %s;"
            aluno_data = (
                form_data['nome_completo'].upper(),
                datetime.strptime(form_data['data_nascimento'], '%Y-%m-%d').date(),
                form_data['email'], form_data['telefone'],
                form_data.get('ativo') == 'true', responsavel_id, aluno_id
            )
            current_app.logger.info(f"Executando SQL: {cur.mogrify(sql_update_aluno, aluno_data).decode('utf-8')}")
            cur.execute(sql_update_aluno, aluno_data)

            conn.commit()
            current_app.logger.info(f"Aluno {form_data['nome_completo'].upper()} atualizado com sucesso!")
    finally:
        conn.close()

def excluir_aluno(aluno_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM aluno WHERE id = %s"
            current_app.logger.info(f"Executando SQL: {cur.mogrify(sql, (aluno_id,)).decode('utf-8')}")
            cur.execute(sql, (aluno_id,))
            conn.commit()
            current_app.logger.info(f"Aluno com ID {aluno_id} excluído com sucesso!")
    finally:
        conn.close()

def listar_professores():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = "SELECT id, nome_completo FROM professor WHERE ativo = TRUE ORDER BY nome_completo"
            cur.execute(sql)
            return dict_fetchall(cur)
    finally:
        conn.close()

def criar_professor(form_data):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO professor (nome_completo, cpf, email, telefone) VALUES (%s, %s, %s, %s) RETURNING id"
            cur.execute(sql, (
                form_data['nome_completo'].upper(),
                form_data['cpf'],
                form_data['email'],
                form_data['telefone']
            ))
            professor_id = cur.fetchone()[0]
            conn.commit()
            print(f"Professor {form_data['nome_completo'].upper()} criado com sucesso!")
            return {'id': professor_id}
    finally:
        conn.close()
