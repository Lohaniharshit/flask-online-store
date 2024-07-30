from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_migrate import Migrate
from functools import wraps
import logging
from models import User, Cart, Item, db

app = Flask(__name__)
app.secret_key = '466df0ab2c7d8ae4c6697f5926c1f5ca36a598600aad865d'  # Change this to your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myusername:mypassword@localhost/mydatabase'
db.init_app(app)
migrate = Migrate(app, db)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/user_home')
@login_required
def user_home():
    return render_template('user_home.html')

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    if request.method == 'POST':
        cart_item = Cart.query.filter_by(user_id=g.user.id, item_id=item_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(user_id=g.user.id, item_id=item_id)
            db.session.add(cart_item)
        db.session.commit()
        flash('Item added to cart.', 'success')
        return redirect(url_for('shop'))

@app.route('/view_cart')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=g.user.id).all()
    items = [{'item': Item.query.get(cart_item.item_id), 'quantity': cart_item.quantity} for cart_item in cart_items]
    return render_template('view_cart.html', items=items)

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=g.user.id, item_id=item_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.', 'info')
    return redirect(url_for('view_cart'))

@app.route('/shop')
@login_required
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
    