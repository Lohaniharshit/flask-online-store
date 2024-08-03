from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_migrate import Migrate
from functools import wraps
import logging
from models import User, Item, db
 
# Database configuration
app = Flask(__name__)
app.secret_key = '466df0ab2c7d8ae4c6697f5926c1f5ca36a598600aad865d' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/shopping_app12345'
db.init_app(app)
migrate = Migrate(app, db)

 
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()
 
@app.route('/')
def home():
    return redirect(url_for('login'))
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            logging.debug(f"User {username} logged in successfully.")
            return redirect(url_for('user_home'))
        flash('Invalid credentials, please try again.', 'danger')
        logging.debug(f"Invalid login attempt for username {username}.")
        return redirect(url_for('login'))
    return render_template('login.html')
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
 
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        # If username does not exist, create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))
 
    return render_template('signup.html')
 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
 
@app.route('/user_home')
def user_home():
    return render_template('user_home.html')
 


@app.route('/shop')
def shop():
    items = Item.query.all()
    return render_template('shop.html', items=items)
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add some sample items to the database (if not already added)
        if Item.query.count() == 0:
            sample_items = [
                Item(name='Laptop 1', category='Laptop', price=1000.99),
                Item(name='Laptop 2', category='Laptop', price=1200.99),
                Item(name='TV 1', category='TV', price=800.99),
                Item(name='TV 2', category='TV', price=900.99),
                Item(name='Phone 1', category='Phone', price=500.99),
                Item(name='Phone 2', category='Phone', price=600.99)
            ]
            db.session.bulk_save_objects(sample_items)
            db.session.commit()
    app.run(debug=True)
 