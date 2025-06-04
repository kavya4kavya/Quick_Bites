# QuickBite - A Flask-based Food Ordering System
import os
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791e9ef8bb805f710810088e09c076af385138b90526fc9859270b51e68cbaf'

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kavya',
    'database': 'quickbite_db',
    'autocommit': True
}

# Database Connection Helper
def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a query and return results if fetch=True"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
            
        connection.commit()
        return result
    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute_single_query(query, params=None):
    """Execute a query and return single result"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        connection.commit()
        return result
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Database Initialization
def create_tables():
    """Create database tables if they don't exist"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                cancellation_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create menu_item table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                emoji VARCHAR(10),
                available BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `order` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(20) DEFAULT 'Placed',
                payment_method VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estimated_time INT DEFAULT 15,
                FOREIGN KEY (student_id) REFERENCES student(id)
            )
        """)
        
        # Create order_item table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                menu_item_id INT NOT NULL,
                quantity INT DEFAULT 1,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES `order`(id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
            )
        """)
        
        connection.commit()
        
        # Add sample menu items if they don't exist
        cursor.execute("SELECT COUNT(*) as count FROM menu_item")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_items = [
                ('Classic Burger', 'Juicy beef patty with fresh lettuce, tomato, and special sauce', 8.99, '🍔'),
                ('Margherita Pizza', 'Fresh mozzarella, basil, and tomato sauce on crispy crust', 12.99, '🍕'),
                ('Caesar Salad', 'Crisp romaine lettuce with parmesan and croutons', 6.99, '🥗'),
                ('Chicken Wrap', 'Grilled chicken with vegetables in a soft tortilla', 7.99, '🌯'),
            ]
            
            for item in sample_items:
                cursor.execute("""
                    INSERT INTO menu_item (name, description, price, emoji) 
                    VALUES (%s, %s, %s, %s)
                """, item)
            
            connection.commit()
        
        return True
    except Error as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        student = execute_single_query(
            "SELECT * FROM student WHERE email = %s", (email,)
        )
        
        if student and check_password_hash(student['password_hash'], password):
            session['student_id'] = student['id']
            session['student_name'] = student['full_name']
            flash('Login successful!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        student_id = request.form['student_id']
        email = request.form['email']
        password = request.form['password']
        
        # Check if student already exists
        existing_email = execute_single_query(
            "SELECT id FROM student WHERE email = %s", (email,)
        )
        if existing_email:
            flash('Email already registered!', 'error')
            return render_template('login.html')
        
        existing_student_id = execute_single_query(
            "SELECT id FROM student WHERE student_id = %s", (student_id,)
        )
        if existing_student_id:
            flash('Student ID already registered!', 'error')
            return render_template('login.html')
        
        # Create new student
        password_hash = generate_password_hash(password)
        result = execute_query("""
            INSERT INTO student (student_id, full_name, email, password_hash) 
            VALUES (%s, %s, %s, %s)
        """, (student_id, full_name, email, password_hash))
        
        if result:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/menu')
def menu():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    menu_items = execute_query(
        "SELECT * FROM menu_item WHERE available = TRUE", fetch=True
    )
    return render_template('menu.html', menu_items=menu_items or [])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    item_id = request.json['item_id']
    quantity = request.json.get('quantity', 1)
    
    # Get or create cart in session
    if 'cart' not in session:
        session['cart'] = []
    
    # Add item to cart
    cart = session['cart']
    item_found = False
    
    for item in cart:
        if item['item_id'] == item_id:
            item['quantity'] += quantity
            item_found = True
            break
    
    if not item_found:
        menu_item = execute_single_query(
            "SELECT * FROM menu_item WHERE id = %s", (item_id,)
        )
        if menu_item:
            cart.append({
                'item_id': item_id,
                'name': menu_item['name'],
                'price': float(menu_item['price']),
                'quantity': quantity
            })
    
    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': len(cart)})

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'student_id' not in session or 'cart' not in session:
        return redirect(url_for('checkout'))
    
    cart = session['cart']
    if not cart:
        flash('Cart is empty!', 'error')
        return redirect(url_for('menu'))
    
    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    connection = get_db_connection()
    if not connection:
        flash('Database error. Please try again.', 'error')
        return redirect(url_for('menu'))
    
    try:
        cursor = connection.cursor()
        
        # Create order
        cursor.execute("""
            INSERT INTO `order` (student_id, total_amount, payment_method) 
            VALUES (%s, %s, %s)
        """, (session['student_id'], total, 'Credit Card'))
        
        order_id = cursor.lastrowid
        
        # Add order items
        for item in cart:
            cursor.execute("""
                INSERT INTO order_item (order_id, menu_item_id, quantity, price) 
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['item_id'], item['quantity'], item['price']))
        
        connection.commit()
        
        # Get the created order
        cursor.execute("SELECT * FROM `order` WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        
        # Clear cart
        session.pop('cart', None)
        
        return render_template('payment_success.html', order={'id': order_id, 'total_amount': total})
        
    except Error as e:
        connection.rollback()
        flash('Order creation failed. Please try again.', 'error')
        return redirect(url_for('menu'))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/orders')
def orders():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    student_orders = execute_query("""
        SELECT * FROM `order` WHERE student_id = %s ORDER BY created_at DESC
    """, (session['student_id'],), fetch=True)
    
    return render_template('orders.html', orders=student_orders or [])

@app.route('/order_status/<int:order_id>')
def order_status(order_id):
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    order = execute_single_query("""
        SELECT * FROM `order` WHERE id = %s AND student_id = %s
    """, (order_id, session['student_id']))
    
    if not order:
        flash('Order not found!', 'error')
        return redirect(url_for('orders'))
    
    return render_template('order_status.html', order=order)

@app.route('/cancel_order/<int:order_id>', methods=['GET', 'POST'])
def cancel_order(order_id):
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    order = execute_single_query("""
        SELECT * FROM `order` WHERE id = %s AND student_id = %s
    """, (order_id, session['student_id']))
    
    if not order:
        flash('Order not found!', 'error')
        return redirect(url_for('orders'))
    
    student = execute_single_query(
        "SELECT * FROM student WHERE id = %s", (session['student_id'],)
    )
    
    if request.method == 'POST':
        if student['cancellation_count'] >= 2:
            flash('Maximum cancellations reached!', 'error')
            return redirect(url_for('orders'))
        
        if order['status'] not in ['Placed', 'In Progress']:
            flash('Cannot cancel this order!', 'error')
            return redirect(url_for('orders'))
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE `order` SET status = 'Cancelled' WHERE id = %s
                """, (order_id,))
                cursor.execute("""
                    UPDATE student SET cancellation_count = cancellation_count + 1 
                    WHERE id = %s
                """, (session['student_id'],))
                connection.commit()
                flash('Order cancelled successfully!', 'success')
            except Error as e:
                connection.rollback()
                flash('Cancellation failed. Please try again.', 'error')
            finally:
                cursor.close()
                connection.close()
        
        return redirect(url_for('orders'))
    
    return render_template('cancel_order.html', order=order, student=student)

@app.route('/profile')
def profile():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    
    student = execute_single_query(
        "SELECT * FROM student WHERE id = %s", (session['student_id'],)
    )
    orders = execute_query(
        "SELECT * FROM `order` WHERE student_id = %s", (session['student_id'],), fetch=True
    )
    
    if not orders:
        orders = []
    
    # Calculate statistics
    total_orders = len(orders)
    completed_orders = len([o for o in orders if o['status'] == 'Completed'])
    total_spent = sum(float(o['total_amount']) for o in orders if o['status'] != 'Cancelled')
    
    return render_template('profile.html', student=student, orders=orders, 
                         total_orders=total_orders, completed_orders=completed_orders, 
                         total_spent=total_spent)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# API endpoint for live order tracking
@app.route('/api/order_status/<int:order_id>')
def api_order_status(order_id):
    if 'student_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    order = execute_single_query("""
        SELECT * FROM `order` WHERE id = %s AND student_id = %s
    """, (order_id, session['student_id']))
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify({
        'status': order['status'],
        'estimated_time': order['estimated_time'],
        'created_at': order['created_at'].isoformat()
    })

"""# Initialize database
@app.before_first_request
def initialize_database():
    create_tables()"""

if __name__ == '__main__':
    # Create tables on startup
    create_tables()
    app.run(debug=True)