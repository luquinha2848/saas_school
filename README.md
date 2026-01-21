# Projeto de Gestão Escolar com PostgreSQL

Este projeto é uma aplicação web de gestão escolar que utiliza Flask e PostgreSQL. Ele foi migrado de SQLite para PostgreSQL e agora usa `conection.py` para centralizar a conexão com o banco de dados.

## Funcionalidades

-   **Gestão de Alunos:** Cadastrar, editar, listar e excluir alunos.
-   **Conexão com PostgreSQL:** A aplicação se conecta a um banco de dados PostgreSQL.
-   **Criação Automática de Tabelas:** As tabelas do banco de dados são criadas automaticamente com base nos modelos definidos no código.

---

## Como Configurar e Executar o Projeto

Siga os passos abaixo para executar o projeto no seu ambiente de desenvolvimento.

### Pré-requisitos

-   **Python 3.6+**
-   **PostgreSQL:** Um servidor PostgreSQL em execução e acessível.
-   **VS Code:** Com a extensão [Python da Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.python) instalada.

### 1. Configure as Credenciais do PostgreSQL

O projeto se conecta ao PostgreSQL usando as seguintes credenciais, que podem ser ajustadas no arquivo `app/__init__.py`:

-   **Host:** `localhost`
-   **Port:** `5432`
-   **Database:** `saas_escola`
-   **User:** `postgres`
-   **Password:** `xbala`

**Importante:** Certifique-se de que o banco de dados `saas_escola` exista no seu servidor PostgreSQL antes de rodar a aplicação.

### 2. Instale as Dependências

Abra um terminal no VS Code (**Terminal > New Terminal**) e instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 3. Execute a Aplicação

Para iniciar a aplicação, execute o arquivo `run.py` no terminal do VS Code:

```bash
python run.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

---

## Como Testar Manualmente

### Criação de Tabelas

Ao iniciar a aplicação com o comando `python run.py`, as tabelas `aluno`, `responsavel` e `professor` serão criadas automaticamente no banco de dados `saas_escola`. Você verá a seguinte mensagem no terminal:

```
Creating database tables...
Database tables created successfully!
```

### Cadastro de Alunos

1.  Acesse a aplicação no seu navegador.
2.  Navegue até a página de "Alunos".
3.  Clique em "Novo Aluno".
4.  Preencha o formulário com os dados do aluno e clique em "Salvar".
5.  Você será redirecionado para a lista de alunos, e o novo aluno deverá aparecer na lista.
6.  No terminal do VS Code, você verá uma mensagem indicando que o aluno foi cadastrado com sucesso.
```
