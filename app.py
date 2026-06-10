from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
import json
import os
import re

app = Flask(__name__)
app.secret_key = 'vibrant-ecommerce-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index_page():
    return redirect(url_for('login_page'))

@app.route('/home')
def home_page():
    return render_template('Ecommerce.html', user=session.get('user_name'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful! Welcome back, ' + user.name, 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html', user=session.get('user_name'))

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login_page'))
        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session['user_name'] = new_user.name
        flash('Account created! Welcome, ' + name, 'success')
        return redirect(url_for('home_page'))
    return render_template('signup.html', user=session.get('user_name'))

@app.route('/convert')
def convert():
    amount = request.args.get('amount', 0)
    to = request.args.get('to', 'USD')
    try:
        url = f'http://localhost:8080/convert?amount={amount}&to={to}'
        with urllib.request.urlopen(url, timeout=3) as res:
            data = json.loads(res.read().decode())
        return jsonify(data)
    except Exception:
        return jsonify({'error': 'Java currency server is not running'}), 503

def generate_chatbot_reply(message):
    msg = (message or '').strip().lower()
    if not msg:
        return "Please type your question, and I'll help you right away. 😊"

    if any(word in msg for word in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
        return "Hi! 👋 I'm your shopping assistant. I can help with login, products, cart, payments, and orders."

    if any(word in msg for word in ['login', 'sign in', 'signin']):
        return "To login, open the Login page from the navbar, enter your email and password, then click Login."

    if any(word in msg for word in ['signup', 'sign up', 'register', 'create account']):
        return "To create an account, go to Signup, enter your details, and submit the form. You'll be logged in automatically after signup."

    if 'logout' in msg:
        return "To logout, click the Logout button in the navbar."

    if any(word in msg for word in ['product', 'products', 'item', 'items', 'category']):
        return "You can browse products from Home or Products page. Use the category cards and sections to discover items quickly."

    if any(word in msg for word in ['cart', 'add to cart', 'remove', 'quantity']):
        return "Use the Add to Cart button for any item. In Cart, you can update quantity or remove products before checkout."

    if any(word in msg for word in ['payment', 'pay', 'checkout', 'upi', 'card', 'cash on delivery', 'cod']):
        return "At checkout, choose your preferred payment method (UPI/Card/COD if enabled), then confirm your order."

    if any(word in msg for word in ['currency', 'convert', 'conversion', 'usd', 'inr', 'eur']):
        return "Use the currency converter widget to convert prices. If conversion fails, ensure the Java currency server is running on port 8080."

    if any(word in msg for word in ['order', 'delivery', 'shipping', 'status', 'track']):
        return "Order tracking isn't connected yet, but after checkout you can view your cart status and confirmation on screen."

    if any(word in msg for word in ['refund', 'return', 'cancel']):
        return "For returns/refunds, contact support with your order details. I can help you draft a return request message if you want."

    if any(word in msg for word in ['help', 'support', 'problem', 'issue']):
        return "I'm here to help. Please tell me your exact issue (login, cart, payment, conversion, or product search), and I'll guide you step-by-step."

    if re.search(r'\b(thank you|thanks|thx)\b', msg):
        return "You're welcome! 😊 Anything else you'd like help with?"

    return "I didn't fully understand that yet. Try asking about login, signup, products, cart, payment, conversion, or orders."

@app.route('/chatbot', methods=['POST'])
def chatbot_reply():
    payload = request.get_json(silent=True) or {}
    user_message = payload.get('message', '')
    reply = generate_chatbot_reply(user_message)
    return jsonify({'reply': reply})

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_page'))

@app.route('/products')
def product_page():
    return render_template('products.html', user=session.get('user_name'))

@app.route('/cart')
def card_page():
    return render_template('cart.html', user=session.get('user_name'))

if __name__ == '__main__':
    app.run(debug=True)
