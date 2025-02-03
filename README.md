# Biblioteca Universitária - Sistema de Gestão

## Contexto do Projeto
Este projeto consiste em desenvolver um sistema de gestão para uma biblioteca universitária que facilita a administração de livros e o acompanhamento dos empréstimos realizados por estudantes e professores. O sistema é composto por uma Base de Dados relacional MySQL e uma aplicação com interface gráfica (GUI) desenvolvida em Python utilizando Flask.

## Funcionalidades do Sistema
- **Gestão de Utilizadores**: Registo e gestão de estudantes e professores.
- **Gestão de Livros**: Registo e gestão de livros, incluindo categorias.
- **Empréstimos e Devoluções**: Registo de empréstimos e devoluções de livros.
- **Consultas e Relatórios**: Consultas de livros e utilizadores, e geração de relatórios.

## Requisitos
- Python 3.x
- MySQL
- Flask
- Flask-SQLAlchemy
- Flask-Login
- pymysql

## Instalação

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/biblioteca-universitaria.git
cd biblioteca-universitaria
```

### Passo 2: Criar e Ativar um Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```

### Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar a Base de Dados
Certifique-se de que o MySQL está instalado e em execução. Crie uma base de dados chamada `Biblioteca` e configure as credenciais no arquivo `config.py`.

```sql
CREATE DATABASE Biblioteca;
```

### Passo 5: Executar os Scripts SQL
Execute os scripts SQL para criar as tabelas e inserir dados iniciais.
Substitua usuario pelo seu username em Mysql

```bash
mysql -u usuario -p Biblioteca < basedados/create.sql
```

## Executar a Aplicação

### Passo 1: Configurar MYySql na apllicação
Mude o nome pelo seu username em mysql e coloque o seu password em config.py:

```python
f"mysql+pymysql://nome:password@localhost/Biblioteca"
```

### Passo 2: Iniciar a Aplicação Flask
```bash
flask run
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

## Estrutura do Projeto
- `app.py`: Arquivo principal da aplicação Flask.
- `models.py`: Definição dos modelos de dados utilizando SQLAlchemy.
- `login_config.py`: Configuração de login e autenticação.
- `config.py`: Configurações da aplicação.
- `basedados/create.sql`: Script SQL para criação das tabelas e inserção de dados iniciais.
- `static/styles.css`: Arquivo CSS para estilização da aplicação.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.