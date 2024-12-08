from flask import Flask, render_template, request, redirect, flash, session, url_for
from db import get_db_connection
from dotenv import load_dotenv
import hashlib
import os
import mysql.connector
from get_complete_data import vending_machines_products, problem_reports
from user import PersonDB
from functools import wraps

load_dotenv()

import logging

# Set up logging configuration
logging.basicConfig(
    filename='app.log',  # Logs will be saved to this file
    level=logging.DEBUG,  # Log all levels DEBUG and above
    format='%(asctime)s - %(levelname)s - %(message)s'
)



app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
SPECIAL_ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin', False):
            flash('Admin access required!', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

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
                SELECT id, is_admin FROM usuarios WHERE email = %s AND senha_hash = %s
            """, (email, password_hash))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user_id'] = user[0]
                session['is_admin'] = bool(user[1])  # Convert to Python's boolean
                flash('Login successful!', 'success')

                if session['is_admin']:
                    return redirect('/admin')
                else:
                    return redirect('/user_home')
                
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
        admin_password = request.form.get('admin_password', '')  # Optional field

        # Hash the password
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        # Determine if the user is an admin
        is_admin = 1 if admin_password == SPECIAL_ADMIN_PASSWORD else 0

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO usuarios (nome, email, senha_hash, is_admin)
                VALUES (%s, %s, %s, %s)
                """, (nome, email, senha_hash, is_admin))
                conn.commit()
                cursor.close()
                conn.close()
                flash('Successfully registered!', 'success')
                return redirect('/login')
            except mysql.connector.IntegrityError:
                flash('Error: Email already registered.', 'danger')

            return redirect('/register')
        except Exception as err:
            flash(f'Error: {err}', 'danger')

    return render_template('register.html')

@app.route('/vending/')
@login_required
def vending_machines_page():
    return render_template('vending_machines.html', vending_machines=vending_machines_products.keys())


@app.route('/vending/<location>', methods=['GET','POST'])
@login_required
def products_page(location):
    if request.method == "POST":
        # Extract product details from the form
        product_name = request.form["product_name"]
        product_price = request.form["product_price"]
        machine_id = request.form["machine_id"]
        user_id = session.get('user_id')  # Get the logged-in user's ID
        product_id = request.form["product_id"]

        # Store purchase info in the session
        session['last_purchase'] = {
            'product_id': product_name,
            'product_price': product_price,
            'machine_id': machine_id,
            'user_id': user_id,
            'product_id': product_id
        }

        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert the purchase record into the 'compras' table
            cursor.execute("""
                INSERT INTO compras (product_name, product_price, machine_id, user_id)
                VALUES (%s, %s, %s, %s)
            """, (product_name, product_price, machine_id, user_id))

            # Commit the transaction
            conn.commit()

            cursor.close()
            conn.close()

            flash('Buy registered', 'success')

            # Redirect to the evaluation page
            return redirect('/evaluate')

        except Exception as err:
            flash(f'Error: {err}', 'danger')

    # Retrieve and display products if the request method is GET
    vending_machine = next((vm for vm in vending_machines_products.keys() if vm.get_location() == location), None)
    if vending_machine:
        machine_products = vending_machines_products.get(vending_machine, {})
        if session.get('is_admin'):
            return render_template('products.html', vending_machine=vending_machine, machine_products=machine_products)
        else:
            return render_template('products_user.html', vending_machine=vending_machine, machine_products=machine_products)
    return redirect(url_for('vending_machines_page'))

@app.route('/product/<location>/<product_name>')
@login_required
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
@login_required
def report_page(report_id):
    report = next((r for r in problem_reports if r.get_id() == int(report_id)), None)
    print(report)
    if report:
        return render_template('report.html', report=report)
    return redirect(url_for('reports_page'))


@app.route('/')
def home():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect('/admin')
        else:
            return redirect('/user_home')
    return render_template('index.html')  # For unauthenticated users


@app.route('/admin')
@admin_required
def admin_page():
    return render_template('admin_page.html')

@app.route('/evaluate', methods=['GET', 'POST'])
@login_required
def evaluate():
    # Retrieve purchase info from session
    purchase_info = session.get('last_purchase')

    if not purchase_info:
        flash('No purchase information available. Please make a purchase first.', 'danger')
        logging.warning("Evaluation attempted without purchase information.")
        return redirect('/vending')  # Redirect back to vending page if no purchase was made

    # Log the retrieved purchase info
    logging.debug(f"Retrieved purchase info: {purchase_info}")

    if request.method == 'POST':
        # Retrieve user inputs from the form
        nota_produto = request.form.get('nota_produto')
        nota_maquina = request.form.get('nota_maquina')
        comentario = request.form.get('comentario', '')

        # Retrieve stored purchase info
        machine_id = purchase_info.get('machine_id')
        user_id = purchase_info.get('user_id')
        product_id = purchase_info.get('product_id')

        # Log the evaluation data being processed
        logging.debug(
            f"Evaluation data: user_id={user_id}, machine_id={machine_id}, product_id={product_id}, "
            f"nota_produto={nota_produto}, nota_maquina={nota_maquina}, comentario={comentario}"
        )

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert evaluation into the 'avaliacoes' table
            cursor.execute("""
                INSERT INTO avaliacoes (id_usuario, id_maquina, id_produto, nota_produto, nota_maquina, comentario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, machine_id, product_id, nota_produto, nota_maquina, comentario))

            conn.commit()
            cursor.close()
            conn.close()

            # Log successful insertion
            logging.info(f"Evaluation successfully inserted: user_id={user_id}, product_id={product_id}, machine_id={machine_id}.")

            # Clear the purchase info from the session after saving the evaluation
            session.pop('last_purchase', None)

            flash('Avaliação registrada com sucesso!', 'success')
            return redirect('/evaluate')
        except Exception as err:
            # Log the error details
            logging.error(f"Error inserting evaluation into the database: {err}")
            flash(f'Erro ao registrar avaliação: {err}', 'danger')

    return render_template('evaluation.html', purchase_info=purchase_info)




@app.route('/user_home')
@login_required
def user_home():
    return render_template('user_page.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

