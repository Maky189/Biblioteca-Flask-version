from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from config import Config
from models import db
from login_config import login_required
from sqlalchemy.sql import text, bindparam
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
        estudante_livros = db.session.execute(text("SELECT LIVROS FROM ESTUDANTES WHERE ID = :id"), {'id': session['user_id']}).fetchone()
        if estudante_livros is None:
            livros = db.session.execute(text("SELECT * FROM LIVROS WHERE NUMERO_COPIAS > 0")).fetchall()
            return render_template('index.html', livros=livros)
        else:
            livros = []
        return render_template('index.html', livros=livros)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        nome = request.form.get('nome')
        password = request.form.get('password')
        user = db.session.execute(text("SELECT ID, PASS FROM ESTUDANTES WHERE NOME = :nome"), {'nome': nome}).fetchone()
        
        if user is None or not check_password_hash(user['PASS'], password):
            return render_template('login.html', message='Invalid credentials')
        else:
            session['user_id'] = user['ID']
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
                    session['user_id'] = user[0]  # Ensure the correct index is used to retrieve the ID
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
                    session['user_id'] = user[0]  # Ensure the correct index is used to retrieve the ID
                    return redirect(url_for('index'))
                else:
                    return render_template('register.html', message='User registration failed')
            except Exception as e:
                return render_template('register.html', message=e)
        
        else:
            return render_template('register.html', message='Invalid user type')


if __name__ == '__main__':
    app.run(debug=True, port=5001)