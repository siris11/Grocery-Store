from flask import Flask, render_template, request, redirect, url_for, flash, session
from applications.model import DB, User, Section, Product
from flask import current_app as app

# ==================================== Controllers ==================================
@app.route('/admin')
def admin():
    if 'a_id' in session:
        products = Product.query.all()
        categories = Section.query.all()
        return render_template('admin.html', products = products,  categories = categories)
    flash('Admin login required!')
    return redirect(url_for('alogin'))

@app.route('/products/<int:c_id>', methods = ['GET', 'POST'])
def products(c_id):
    if 'a_id' in session:
        if request.method == 'GET':
            category = Section.query.filter_by(c_id = c_id).first()
            if category:
                products = Product.query.filter_by(c_id = category.c_id).all()
                return render_template('products.html', products = products)
            else:
                flash('Category not found!')
                return redirect(url_for('admin'))
    flash('Admin login required!')
    return redirect(url_for('alogin'))


@app.route('/alogin', methods = ['GET', 'POST'])
def alogin():
    if request.method == 'GET':
        return render_template('alogin.html')
    else:
        data = request.form
        admin = User.query.filter_by(email = data.get('email'), is_admin = True).first()
        if admin:
            if admin.password == data.get('password'):
                session['a_id'] = admin.id
                return redirect(url_for('admin'))
            else:
                flash('Password is incorrect!')
                return render_template('alogin.html')
        else:
            flash('Admin email is incorrect!')
            return render_template('alogin.html')

@app.route('/alogout')
def alogout():
    session.clear()
    return redirect(url_for('alogin'))


@app.route('/add_category', methods = ['GET', 'POST'])
def add_category():
    if 'a_id' in session:
        if request.method == 'GET':
            return render_template('add_category.html')
        if request.method == 'POST':
            data = request.form
            category_new = Section(name = data.get('category'))
            DB.session.add(category_new)
            DB.session.commit()
            flash('Category added successfully!')
            return redirect(url_for('admin'))
    flash('Admin login required!')
    return redirect(url_for('alogin'))

@app.route('/update_category/<int:c_id>', methods=['GET', 'POST'])
def update_category(c_id):
    if 'a_id' in session:
        if request.method == 'GET':
            category = Section.query.filter_by(c_id = c_id).first()
            if category:
                return render_template('update_category.html', category = category)
            else:
                flash('Category not found!')
                return redirect(url_for('admin'))
        if request.method == 'POST':
            category = Section.query.filter_by(c_id = c_id).first()
            if category:
                data = request.form
                category.name = data.get('category')
                DB.session.commit()
                flash('Category updated successfully!')
                return redirect(url_for('admin'))
            else:
                flash('Category not found!')
                return redirect(url_for('admin'))
        flash('Admin login required!')
    return redirect(url_for('alogin'))

@app.route('/delete_category/<int:c_id>', methods = ['GET', 'POST'])
def delete_category(c_id):
    if 'a_id' in session:
        if request.method == 'GET':
            category = Section.query.filter_by(c_id = c_id).first()
            if category:
                return render_template('delete_category.html', category = category)
            else:
                flash('Category not found!')
                return redirect(url_for('admin'))
        if request.method == 'POST':
            category = Section.query.filter_by(c_id = c_id).delete()
            DB.session.commit()
            flash('Category deleted successfully!')
            return redirect(url_for('admin'))
    flash('Admin login required!')
    return redirect(url_for('alogin'))


@app.route('/add_product/<int:c_id>', methods = ['GET', 'POST'])
def add_product(c_id):
    if 'a_id' in session:
        if request.method == 'GET':
            category = Section.query.filter_by(c_id = c_id).first()
            if category:
                return render_template('add_product.html', category = category)
            else:
                flash('Category not found!')
                return redirect(url_for('admin'))
        if request.method == 'POST':
            category = Section.query.filter_by(c_id = c_id).first()
            if category:
                data = request.form
                product_new = Product(name = data.get('product'), 
                                    description = data.get('description').strip(),
                                    category = category.name,
                                    rate = data.get('rate'), 
                                    unit = data.get('unit'),
                                    stock = data.get('stock'),
                                    c_id = category.c_id)
                DB.session.add(product_new)
                DB.session.commit()
                flash('Product added successfully!')
                return redirect(url_for('admin'))
            else:
                flash('Category not found!')
                return redirect(url_for('admin'))
    flash('Admin login required!')
    return redirect(url_for('alogin'))


@app.route('/update_product/<int:p_id>', methods = ['GET', 'POST'])
def update_product(p_id):
    if 'a_id' in session:
        if request.method == 'GET':
            product = Product.query.filter_by(p_id = p_id).first()
            if product:
                return render_template('update_product.html', product = product)
            else:
                flash('Product not found!')
                return redirect(url_for('admin'))
        if request.method == 'POST':
            product = Product.query.filter_by(p_id = p_id).first()
            if product:
                data = request.form
                product.name = data.get('product')
                product.description = data.get('description').strip()
                product.rate = data.get('rate')
                product.unit = data.get('unit')
                if int(data.get('stock')) > product.stock:
                    product.stock = data.get('stock')
                DB.session.commit()
                flash('Product updated successfully!')
                return redirect(url_for('admin'))
            else:
                flash('Product not found!')
                return redirect(url_for('admin'))
    flash('Admin login required!')
    return redirect(url_for('alogin'))


@app.route('/delete_product/<int:p_id>', methods = ['GET', 'POST'])
def delete_product(p_id):
    if 'a_id' in session:
        if request.method == 'GET':
            product = Product.query.filter_by(p_id = p_id).first()
            if product:
                return render_template('delete_product.html', product = product)
            else:
                flash('Product not found!')
                return redirect(url_for('admin'))
        if request.method == 'POST':
            product = Product.query.filter_by(p_id = p_id).delete()
            DB.session.commit()
            flash('Product deleted successfully!')
            return redirect(url_for('admin'))
    flash('Admin login required!')
    return redirect(url_for('alogin'))
    
    

