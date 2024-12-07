from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from db import get_db_connection
from dotenv import load_dotenv
import hashlib
import os
import mysql.connector
from get_complete_data import vending_machines_products, problem_reports
from user import PersonDB

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Configurando sqlalchemy
usuario = os.getenv("MYSQL_USER")
senha = os.getenv("MYSQL_PASSWORD")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{usuario}:{senha}@localhost/coffe_map"

# Inicializando conexão com a base de dados
db = SQLAlchemy(app)

# Criando tabelas da base de dados
with app.app_context():
    db.create_all()

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
                user_object = PersonDB(user[0])

                if user_object.get_name() == "admin" or user_object.is_admin():
                    return redirect('/admin')
                
                return redirect('/')
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
                conn.commit()
                cursor.close()
                conn.close()
                flash('Successfully! registered', 'success')
                return redirect('/login')
            except mysql.connector.IntegrityError:
                flash('Error: Email already registered.', 'danger')

            
            return redirect('/register')
        except Exception as err:
            flash(f'Error: {err}', 'danger')

    return render_template('register.html')

@app.route('/vending/')
def vending_machines_page():
    return render_template('vending_machines.html', vending_machines=vending_machines_products.keys())

@app.route('/vending/<location>')
def products_page(location):
    vending_machine = next((vm for vm in vending_machines_products.keys() if vm.get_location() == location), None)
    if vending_machine:
        machine_products = vending_machines_products.get(vending_machine, {})
        return render_template('products.html', vending_machine=vending_machine, machine_products=machine_products)
    return redirect(url_for('vending_machines_page'))

@app.route('/product/<location>/<product_name>')
def product_detail_page(location, product_name):
    vending_machine = next((vm for vm in vending_machines_products.keys() if vm.get_location() == location), None)
    if vending_machine:
        machine_products = vending_machines_products.get(vending_machine, {})
        product = next((p for p in machine_products.keys() if p.get_name() == product_name), None)
        if product:
            return render_template('product_detail.html', vending_machine=vending_machine, product=product)
    return redirect(url_for('vending_machines_page'))

@app.route('/report_problem', methods=['GET', 'POST'])
def report_problem():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'danger')
        return redirect('/login')

    if request.method == 'POST':
        tipo_problema = request.form['tipo_problema']
        descricao = request.form['descricao']
        id_maquina = request.form.get('id_maquina')
        user_id = session['user_id']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO problemas_reportados (id_usuario, tipo_problema, descricao, id_maquina)
                VALUES (%s, %s, %s, %s)
            """, (user_id, tipo_problema, descricao, id_maquina))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Problem report submitted successfully!', 'success')
            return redirect('/report_problem')
        except Exception as err:
            flash(f'Error: {err}', 'danger')
            return redirect('/report_problem')

    return render_template('report_problem.html')

@app.route('/reports/')
def reports_page():
    return render_template('reports.html', problem_reports=problem_reports)

@app.route('/reports/<report_id>')
def report_page(report_id):
    report = next((r for r in problem_reports if r.get_id() == int(report_id)), None)
    print(report)
    if report:
        return render_template('report.html', report=report)
    return redirect(url_for('reports_page'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin_page.html')

if __name__ == '__main__':
    app.run(debug=True)
