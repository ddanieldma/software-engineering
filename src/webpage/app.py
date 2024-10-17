from flask import Flask, render_template, request, redirect, flash, session
from db import get_db_connection
from dotenv import load_dotenv
import hashlib
import os
import mysql.connector
from get_products import products_list

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM usuarios WHERE email = %s AND senha_hash = %s
            """, (email, password_hash))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user_id'] = user[0]
                flash('Login concluido!', 'success')
            else:
                flash('Invalid email or password', 'danger')
        except Exception as err:
            flash(f'Error: {err}', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Hash the password
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (%s, %s, %s)
                """, (nome, email, senha_hash))
            except mysql.connector.IntegrityError:
                flash('Error: Email already registered.', 'danger')

            conn.commit()
            cursor.close()
            conn.close()
            flash('Successfully! registered', 'success')
            return redirect('/register')
        except Exception as err:
            flash(f'Error: {err}', 'danger')

    return render_template('register.html')

@app.route('/products')
def products():
    return render_template('products.html', items=products_list)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
