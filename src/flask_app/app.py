from flask import Flask, render_template
from flask_app.get_products import products_list

app = Flask(__name__)

@app.route('/products')
def products():
    return render_template('products_page.html', items=products_list)

if __name__ == '__main__':
    app.run(debug=True)