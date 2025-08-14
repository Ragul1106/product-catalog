from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('index.html', products=products)

@main.route('/in-stock')
def in_stock():
    products = Product.query.filter_by(in_stock=True).all()
    return render_template('in_stock.html', products=products)

@main.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        in_stock = 'in_stock' in request.form
        description = request.form['description']

        product = Product(name=name, price=price, in_stock=in_stock, description=description)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_product.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.in_stock = 'in_stock' in request.form
        product.description = request.form['description']

        db.session.commit()
        flash('Product updated successfully!', 'info')
        return redirect(url_for('main.index'))

    return render_template('edit_product.html', product=product)

@main.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('main.index'))
