from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.Integer(), primary_key=True)
    email = DB.Column(DB.String(50), nullable=False, unique=True)
    name = DB.Column(DB.String(30), nullable=False)
    password = DB.Column(DB.String(10), nullable=False)
    is_admin = DB.Column(DB.Boolean, nullable=False, default=False)
    carts = relationship('Cart', backref='user', lazy=True)
    orders = relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return "<User %r>" % self.name

class Section(DB.Model):
    c_id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    products = relationship('Product', backref='section',
                            lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<category {self.name}>"

class Product(DB.Model):
    p_id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    rate = DB.Column(DB.Integer(), nullable=False)
    stock = DB.Column(DB.Integer(), nullable=False)
    sold = DB.Column(DB.Integer(), nullable=False, default=0)
    unit = DB.Column(DB.String(), nullable=False)
    description = DB.Column(DB.String(100))
    category = DB.Column(DB.String(50), nullable=False)
    c_id = DB.Column(DB.Integer(), DB.ForeignKey('section.c_id'), nullable=False)
    carts = relationship('Cart', backref='product',
                         lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<product {self.name}>"

class Cart(DB.Model):
    cart_id = DB.Column(DB.Integer(), primary_key=True)
    quantity = DB.Column(DB.Integer(), nullable=False)
    user_id = DB.Column(DB.Integer(), DB.ForeignKey("user.id"), nullable=False)
    product_id = DB.Column(DB.Integer(), DB.ForeignKey("product.p_id"), nullable=False)

class Order(DB.Model):
    o_id = DB.Column(DB.Integer(), primary_key=True)
    quantity = DB.Column(DB.Integer(), nullable=False)
    total = DB.Column(DB.Integer(), nullable=False)
    rate = DB.Column(DB.Integer(), nullable=False)
    product_name = DB.Column(DB.String(50), nullable=False)
    user_id = DB.Column(DB.Integer(), DB.ForeignKey("user.id"), nullable=False)