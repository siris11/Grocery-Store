from flask import Flask, render_template, request, redirect, url_for, flash, session
from applications.model import DB, User, Product, Cart, Order
from flask import current_app as app
from sqlalchemy import func

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.form
        user = User.query.filter_by(email = data.get('email'), is_admin = False).first()
        if user:
            if user.password == data.get('password'):
                session['u_id'] = user.id
                session['name'] = user.name
                return redirect(url_for('dashboard'))
            else:
                flash('Password is incorrect!')
                return render_template('login.html')
        else:
            flash('User not found!')
            return render_template('login.html')
       

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = request.form
        user = User.query.filter_by(email = data.get('email'), is_admin = False).first()
        if not user:
            user_new = User(name = data.get('name'), email = data.get('email'), password = data.get('password'))
            DB.session.add(user_new)
            DB.session.commit()
            user = User.query.filter_by(email = data.get('email'), is_admin = False).first()
            session['u_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Email already exists!')
            return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'u_id' and 'name' in session:
        args = request.args.get('q')
        if args:
            query_string = f'%{args}%'
            results = Product.query.filter(
                (func.lower(Product.name).like(query_string)) |
                (func.lower(Product.category).like(query_string)) |
                (Product.rate == args)).all()
            return render_template("dashboard.html", products = results, user = session.get('name'))
        else:
            products = Product.query.all()
            return render_template('dashboard.html', products = products, user = session.get('name'))
    flash('User login required!')
    return redirect(url_for('login'))

@app.route('/cart_view')
def cart_view():
    if 'u_id' and 'name' in session:
        grand_total = 0
        details = []
        in_cart = Cart.query.filter_by(user_id = session.get('u_id')).all()
        for c in in_cart:
            p = Product.query.filter_by(p_id = c.product_id).first()
            details.append((c, p))
            grand_total += int(c.quantity) * int(p.rate)
        return render_template('cart_view.html', details = details, grand_total = grand_total, user = session.get('name'))
    flash('User login required!')
    return redirect(url_for('login'))

@app.route('/tocart/<int:p_id>', methods = ['GET', 'POST'])
def tocart(p_id):
    if 'u_id' and 'name' in session:
        product = Product.query.filter_by(p_id = p_id).first()
        if request.method == 'POST' and product:
            in_cart = Cart.query.filter_by(product_id = p_id).first()
            if not in_cart:
                data = request.form
                cart_new = Cart(quantity = int(data.get('quantity')),
                                product_id = product.p_id,
                                user_id = session.get("u_id"))
                DB.session.add(cart_new)
                DB.session.commit()
                flash("Product is added to cart!")
                return redirect(url_for('dashboard'))
        if request.method == 'GET' and product:
            in_cart = Cart.query.filter_by(product_id = p_id).first()
            if not in_cart:
                return render_template('tocart.html', product = product, user = session.get('name'))
            else:
                flash("Product already exists in the cart!")
                return redirect(url_for('dashboard'))
    flash('User login required!')
    return redirect(url_for('login'))


@app.route('/cart_purchase')
def cart_purchase():
    products = Cart.query.filter_by(user_id = session.get('u_id')).all()
    for p in products:
        product = Product.query.filter_by(p_id = p.product_id).first()
        if product and (product.stock - product.sold >= p.quantity):
            order_new = Order(product_name = product.name,
                            rate = str(product.rate) + product.unit,
                            quantity = p.quantity,
                            total = product.rate * int(p.quantity),
                            user_id = session.get("u_id"))
            product.sold = product.sold + int(p.quantity)
            DB.session.add(order_new)
    Cart.query.filter_by(user_id = session.get('u_id')).delete()
    DB.session.commit()
    flash("Thankyou for shopping with us!")
    return redirect(url_for('dashboard'))


@app.route('/orders')
def orders():
    if 'u_id' and 'name' in session:
        orders = Order.query.all()
        return render_template('orders.html', orders = orders, user = session.get('name'))
    flash('User login required!')
    return redirect(url_for('login'))