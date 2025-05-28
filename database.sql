
-- database.sql - MySQL Database Schema
--BACKEND--

CREATE DATABASE IF NOT EXISTS quickbite_db;
USE quickbite_db;

-- Students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    cancellation_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Menu items table
CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    image_url VARCHAR(255),
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('placed', 'in_progress', 'ready', 'completed', 'cancelled') DEFAULT 'placed',
    cancellation_reason TEXT,
    estimated_time INT DEFAULT 15, -- in minutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Insert sample menu items
INSERT INTO menu_items (name, description, price, category, image_url) VALUES
('Classic Burger', 'Juicy beef patty with fresh lettuce, tomato, and special sauce', 8.99, 'Main Course', '/static/images/burger.jpg'),
('Margherita Pizza', 'Fresh mozzarella, basil, and tomato sauce on crispy crust', 12.99, 'Main Course', '/static/images/pizza.jpg'),
('Caesar Salad', 'Crisp romaine lettuce with parmesan and croutons', 6.99, 'Salad', '/static/images/salad.jpg'),
('Chicken Wrap', 'Grilled chicken with vegetables in a soft tortilla', 7.99, 'Main Course', '/static/images/wrap.jpg'),
('French Fries', 'Golden crispy potato fries with seasoning', 3.99, 'Sides', '/static/images/fries.jpg'),
('Chocolate Shake', 'Rich chocolate milkshake topped with whipped cream', 4.99, 'Beverages', '/static/images/shake.jpg'),
('Fish Tacos', 'Fresh fish with cabbage slaw in corn tortillas', 9.99, 'Main Course', '/static/images/tacos.jpg'),
('Veggie Burger', 'Plant-based patty with all the classic fixings', 8.49, 'Main Course', '/static/images/veggie_burger.jpg');

-- Insert sample student (password is 'password123' hashed)
INSERT INTO students (name, student_id, email, password) VALUES
('John Doe', 'STU123456', 'john.doe@university.edu', 'scrypt:32768:8:1$XYZ...');

-- Create indexes for better performance
CREATE INDEX idx_orders_student_id ON orders(student_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_student_id ON students(student_id);


