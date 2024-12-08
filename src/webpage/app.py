from flask import Flask, render_template, request, redirect, flash, session, url_for
from db import get_db_connection
from dotenv import load_dotenv
import hashlib
import os
from get_complete_data import vending_machines_products, problem_reports
from functools import wraps
from database_managment import DBConnection
from flask import jsonify

load_dotenv()


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
            query = """
                SELECT id, is_admin FROM usuarios WHERE email = %s AND senha_hash = %s"""
            params = (email, password_hash)

            db = DBConnection()
            user = db.execute_query(query, params, fetch_all=False)

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
            query = """
                INSERT INTO usuarios (nome, email, senha_hash, is_admin)
                VALUES (%s, %s, %s, %s)
            """
            params = (nome, email, senha_hash, is_admin)

            db = DBConnection()
            db.execute_query(query, params)
            flash('Successfully registered!', 'success')
            return redirect('/login')
        except Exception as err:
            flash(f'Error: {err}', 'danger')

    return render_template('register.html')

@app.route('/vending/')
@login_required
def vending_machines_page():
    # get favorite vending machines
    db = DBConnection()

    query = """
        SELECT id_maquina, is_favorite
        FROM favoritos
        WHERE id_usuario = %s
    """

    user_id = session.get('user_id')

    favorites = db.execute_query(query, (user_id,), True)
    favorites = [x[0] for x in favorites if x[1] == 1]
    print(favorites)

    return render_template('vending_machines.html', vending_machines=vending_machines_products.keys(), favorites=favorites)

@app.route('/vending/<location>')
@login_required
def products_page(location):
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

@app.route('/user_home')
@login_required
def user_home():
    return render_template('user_page.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect('/')

@app.route('/save_favorites', methods=['POST'])
def save_favorites():
    try:
        data = request.get_json()
        favorites = data.get('favorites', [])

        if not favorites:
            return jsonify({"message": "Nenhuma máquina selecionada como favorita."}), 400
        
        # Cria a conexão com o banco de dados
        db = DBConnection()

        user_id = session.get('user_id')

        # Primeiro, definimos todas as máquinas de venda do usuário como não favoritas (FALSE)
        query_reset = """
            UPDATE favoritos
            SET is_favorite = FALSE
            WHERE id_usuario = %s
        """
        db.execute_query(query_reset, (user_id,))

        # Agora, atualizamos para TRUE as máquinas que estão na lista de favoritos
        query_update_favorites = """
            INSERT INTO favoritos (id_usuario, id_maquina, is_favorite)
            VALUES (%s, %s, TRUE)
            ON DUPLICATE KEY UPDATE is_favorite = TRUE
        """

        for machine_id in favorites:
            db.execute_query(query_update_favorites, (user_id, machine_id))

        return jsonify({"message": "Favoritos salvos com sucesso."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
