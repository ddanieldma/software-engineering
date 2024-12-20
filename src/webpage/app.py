from flask import Flask, render_template, request, redirect, flash, session, url_for
from db import get_db_connection
from dotenv import load_dotenv
import hashlib
import os
from get_complete_data import vending_machines_products, problem_reports
from functools import wraps
from database_managment import DBConnection
from flask import jsonify
from report_builder.report_builder import ReportGenerator
from flask import Response
from report_builder.strategies import VendingMachineReportStrategy

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
            db = DBConnection()
            
            # Insert the purchase record into the 'compras' table
            db.execute_query("""
                INSERT INTO compras (product_name, product_price, machine_id, user_id)
                VALUES (%s, %s, %s, %s)
            """, (product_name, product_price, machine_id, user_id))

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
            db=DBConnection()

            db.execute_query("""
                INSERT INTO problemas_reportados (id_usuario, tipo_problema, descricao, id_maquina)
                VALUES (%s, %s, %s, %s)
            """, (user_id, tipo_problema, descricao, id_maquina))
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
            db=DBConnection()

            # Insert evaluation into the 'avaliacoes' table
            db.execute_query("""
                INSERT INTO avaliacoes (id_usuario, id_maquina, id_produto, nota_produto, nota_maquina, comentario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, machine_id, product_id, nota_produto, nota_maquina, comentario))


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
    

@app.route('/generate_report', methods=['GET', 'POST'])
@login_required
def generate_report():
    if request.method == 'POST':
        # Select strategy based on user input (you can add more strategies as needed)
        strategy = VendingMachineReportStrategy()

        # Create a report generator with the selected strategy
        report_generator = ReportGenerator(strategy)

        # Generate the report using the strategy
        report_data = report_generator.generate_report(initial_data=[])

        # Extract the revenue and rating data as CSV for download
        revenue_and_rating_csv = report_data['revenue_and_rating'].to_csv(index=False)
        stock_csv = report_data['stock_csv']  # Already in CSV format
        stock_json = report_data['stock_json']  # Already in JSON format

        # Return multiple files (CSV and JSON) as responses
        response = Response(
            revenue_and_rating_csv,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=revenue_and_rating.csv"}
        )

        # You can also provide stock_csv and stock_json similarly
        # Or combine them into a zip file if necessary

        return response  # Return the first response (you can add logic to combine CSV and JSON if necessary)

    # If it's a GET request, render the strategy selection form
    return render_template('generate_report.html')





if __name__ == '__main__':
    app.run(debug=True)

