from flask import Flask, render_template, redirect, url_for, session, request, flash
from config import Config
from models import db
from login_config import login_required
from sqlalchemy.sql import text
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

app = Flask(__name__)
app.config.from_object(Config)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0 
    response.headers["Pragma"] = "no-cache"
    return response

app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        user = db.session.execute(text("SELECT NOME FROM ESTUDANTES WHERE ID = :id"), {'id': session['user_id']}).fetchone()
        if not user:
            user = db.session.execute(text("SELECT NOME FROM PROFESSORES WHERE ID = :id"), {'id': session['user_id']}).fetchone()
        
        if user:
            user_name = user[0]
        else:
            user_name = "Unknown User"
        
        estudante_livros = db.session.execute(text("SELECT LIVROS FROM ESTUDANTES WHERE ID = :id"), {'id': session['user_id']}).fetchone()
        if estudante_livros and estudante_livros[0]:
            livros = db.session.execute(text("SELECT * FROM LIVROS WHERE ID IN :livros"), {'livros': tuple(estudante_livros[0].split(','))}).fetchall()
        else:
            livros = db.session.execute(text("SELECT * FROM LIVROS WHERE NUMERO_COPIAS > 0")).fetchall()
        
        user_books = db.session.execute(text("""
            SELECT LIVROS.ID, LIVROS.TITULO, LIVROS.AUTOR, LIVROS.ANO, LIVROS.ISBN, LIVROS.CATEGORIA
            FROM EMPRESTIMOS
            JOIN LIVROS ON EMPRESTIMOS.LIVRO_ID = LIVROS.ID
            WHERE EMPRESTIMOS.ALUNO_ID = :id OR EMPRESTIMOS.PROFESSOR_ID = :id
        """), {'id': session['user_id']}).fetchall()
        
        available_books = db.session.execute(text("SELECT * FROM LIVROS WHERE NUMERO_COPIAS > 0")).fetchall()
        
        return render_template('index.html', livros=livros, user_books=user_books, available_books=available_books, user_name=user_name)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        nome = request.form.get('nome')
        password = request.form.get('password')
        
        user = db.session.execute(text("SELECT ID, PASS FROM ESTUDANTES WHERE NOME = :nome"), {'nome': nome}).fetchone()
        if user is None:
            user = db.session.execute(text("SELECT ID, PASS FROM PROFESSORES WHERE NOME = :nome"), {'nome': nome}).fetchone()
        
        if user is None or not check_password_hash(user[1], password):  # Use integer index for 'PASS'
            return render_template('login.html', message='Invalid credentials')
        else:
            session['user_id'] = user[0]  # Use integer index for 'ID'
            return redirect(url_for('index'))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user_type = request.form.get('user_type')
        nome = request.form.get('nome')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        contacto = request.form.get('contacto')
        email = request.form.get('email')
        
        if nome == '' or password == '':
            return render_template('register.html', message='Username and password are required')
        if password != confirmation:
            return render_template('register.html', message='Passwords must match')
        
        if user_type == 'student':
            numero_estudante = request.form.get('numero_estudante')
            curso = request.form.get('curso')
            
            existing_user = db.session.execute(text("SELECT ID FROM ESTUDANTES WHERE NOME = :nome"), {'nome': nome}).fetchone()
            if existing_user:
                return render_template('register.html', message='Username already exists')
            
            try:
                stmt = text("INSERT INTO ESTUDANTES (NOME, NUMERO_ESTUDANTE, CURSO, CONTACTO, EMAIL, PASS) VALUES (:nome, :numero_estudante, :curso, :contacto, :email, :password)")
                db.session.execute(stmt, {'nome': nome, 'numero_estudante': numero_estudante, 'curso': curso, 'contacto': contacto, 'email': email, 'password': generate_password_hash(password)})
                db.session.commit()
                
                user = db.session.execute(text("SELECT ID FROM ESTUDANTES WHERE NOME = :nome"), {'nome': nome}).fetchone()
                if user:
                    session['user_id'] = user[0]  
                    return redirect(url_for('index'))
                else:
                    return render_template('register.html', message='User registration failed')
            except Exception as e:
                return render_template('register.html', message='An error occurred during registration')
        
        elif user_type == 'professor':
            numero_funcionario = request.form.get('numero_funcionario')
            departamento = request.form.get('departamento')
            
            existing_user = db.session.execute(text("SELECT ID FROM PROFESSORES WHERE NOME = :nome"), {'nome': nome}).fetchone()
            if existing_user:
                return render_template('register.html', message='Username already exists')
            
            try:
                stmt = text("INSERT INTO PROFESSORES (NOME, NUMERO_FUNCIONARIO, DEPARTAMENTO, CONTACTO, EMAIL, PASS) VALUES (:nome, :numero_funcionario, :departamento, :contacto, :email, :password)")
                db.session.execute(stmt, {'nome': nome, 'numero_funcionario': numero_funcionario, 'departamento': departamento, 'contacto': contacto, 'email': email, 'password': generate_password_hash(password)})
                db.session.commit()
                
                user = db.session.execute(text("SELECT ID FROM PROFESSORES WHERE NOME = :nome"), {'nome': nome}).fetchone()
                if user:
                    session['user_id'] = user[0]  
                    return redirect(url_for('index'))
                else:
                    return render_template('register.html', message='User registration failed')
            except Exception as e:
                return render_template('register.html', message='An error occurred during registration')
        
        else:
            return render_template('register.html', message='Invalid user type')

@app.route('/gerenciar_usuarios', methods=['POST'])
@login_required
def manage_users():
    nome = request.form.get('nome')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')
    contacto = request.form.get('contacto')
    email = request.form.get('email')
    
    if nome == '' or password == '':
        return redirect(url_for('index', message='Nome de usuário e senha são obrigatórios'))
    if password != confirmation:
        return redirect(url_for('index', message='As senhas devem coincidir'))
    
    try:
        stmt = text("INSERT INTO ESTUDANTES (NOME, CONTACTO, EMAIL, PASS) VALUES (:nome, :contacto, :email, :password)")
        db.session.execute(stmt, {'nome': nome, 'contacto': contacto, 'email': email, 'password': generate_password_hash(password)})
        db.session.commit()
        return redirect(url_for('index', message='Usuário salvo com sucesso'))
    except Exception as e:
        return redirect(url_for('index', message='Ocorreu um erro ao salvar o usuário'))

@app.route('/gerenciar_livros', methods=['POST'])
@login_required
def manage_books():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    ano = request.form.get('ano')
    isbn = request.form.get('isbn')
    categoria = request.form.get('categoria')
    numero_copias = request.form.get('numero_copias')
    
    if titulo == '' or autor == '':
        return redirect(url_for('index', message='Título e autor são obrigatórios'))
    
    try:
        stmt = text("INSERT INTO LIVROS (TITULO, AUTOR, ANO, ISBN, CATEGORIA, NUMERO_COPIAS) VALUES (:titulo, :autor, :ano, :isbn, :categoria, :numero_copias)")
        db.session.execute(stmt, {'titulo': titulo, 'autor': autor, 'ano': ano, 'isbn': isbn, 'categoria': categoria, 'numero_copias': numero_copias})
        db.session.commit()
        return redirect(url_for('index', message='Livro salvo com sucesso'))
    except Exception as e:
        return redirect(url_for('index', message='Ocorreu um erro ao salvar o livro'))

@app.route('/gerenciar_emprestimos', methods=['POST'])
@login_required
def manage_loans():
    book_title = request.form.get('book_id')
    
    if book_title == '':
        flash('Nome do livro é obrigatório')
        return redirect(url_for('index'))
    
    try:
        book = db.session.execute(text("SELECT ID, NUMERO_COPIAS FROM LIVROS WHERE TITULO = :titulo"), {'titulo': book_title}).fetchone()
        if not book:
            flash('Livro não encontrado')
            return redirect(url_for('index'))
        
        if book.NUMERO_COPIAS <= 0:
            flash('Livro indisponível')
            return redirect(url_for('index'))
        
        user_id = session['user_id']
        user_type = db.session.execute(text("SELECT 'ESTUDANTE' AS tipo FROM ESTUDANTES WHERE ID = :id UNION SELECT 'PROFESSOR' AS tipo FROM PROFESSORES WHERE ID = :id"), {'id': user_id}).fetchone()
        
        if not user_type:
            flash('Usuário não encontrado')
            return redirect(url_for('index'))
        
        if user_type.tipo == 'ESTUDANTE':
            stmt = text("INSERT INTO EMPRESTIMOS (ALUNO_ID, LIVRO_ID, DATA_ENTRADA) VALUES (:user_id, :book_id, CURDATE())")
        else:
            stmt = text("INSERT INTO EMPRESTIMOS (PROFESSOR_ID, LIVRO_ID, DATA_ENTRADA) VALUES (:user_id, :book_id, CURDATE())")
        
        db.session.execute(stmt, {'user_id': user_id, 'book_id': book.ID})
        db.session.execute(text("UPDATE LIVROS SET NUMERO_COPIAS = NUMERO_COPIAS - 1 WHERE ID = :id"), {'id': book.ID})
        db.session.commit()
        
        loan_details = db.session.execute(text("""
            SELECT DATA_ENTRADA, DATA_SAIDA
            FROM EMPRESTIMOS
            WHERE LIVRO_ID = :book_id AND (ALUNO_ID = :user_id OR PROFESSOR_ID = :user_id)
            ORDER BY ID DESC LIMIT 1
        """), {'book_id': book.ID, 'user_id': user_id}).fetchone()
        
        user_books = db.session.execute(text("""
            SELECT LIVROS.ID, LIVROS.TITULO, LIVROS.AUTOR, LIVROS.ANO, LIVROS.ISBN, LIVROS.CATEGORIA
            FROM EMPRESTIMOS
            JOIN LIVROS ON EMPRESTIMOS.LIVRO_ID = LIVROS.ID
            WHERE EMPRESTIMOS.ALUNO_ID = :id OR EMPRESTIMOS.PROFESSOR_ID = :id
        """), {'id': session['user_id']}).fetchall()
        
        available_books = db.session.execute(text("SELECT * FROM LIVROS WHERE NUMERO_COPIAS > 0")).fetchall()
        
        flash(f'Empréstimo salvo com sucesso. Data de Entrada: {loan_details.DATA_ENTRADA}, Data de Saída: {loan_details.DATA_SAIDA}')
        return render_template('index.html', user_books=user_books, available_books=available_books)
    except Exception as e:
        flash(f'Ocorreu um erro ao salvar o empréstimo: {str(e)}')
        flash(f'Book Title: {book_title}')
        flash(f'User ID: {user_id}')
        flash(f'Executed Query: {stmt}')
        return redirect(url_for('index'))

@app.route('/livros', methods=['GET'])
@login_required
def livros():
    livros = db.session.execute(text("SELECT * FROM LIVROS WHERE NUMERO_COPIAS > 0")).fetchall()
    return render_template('livros.html', livros=livros)

@app.route('/utilizadores', methods=['GET'])
@login_required
def utilizadores():
    estudantes = db.session.execute(text("SELECT * FROM ESTUDANTES")).fetchall()
    professores = db.session.execute(text("SELECT * FROM PROFESSORES")).fetchall()
    return render_template('utilizadores.html', estudantes=estudantes, professores=professores)

if __name__ == '__main__':
    app.run(debug=True, port=5001)