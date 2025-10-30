from datetime import datetime

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    
    @staticmethod
    def authenticate(db, username, password):
        user = db.fetch_one('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password))
        return user

class Employee:
    def __init__(self, name, position, salary, hire_date):
        self.name = name
        self.position = position
        self.salary = salary
        self.hire_date = hire_date
    
    def save(self, db):
        db.execute_query('''
            INSERT INTO employees (name, position, salary, hire_date)
            VALUES (?, ?, ?, ?)
        ''', (self.name, self.position, self.salary, self.hire_date))

class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
    
    def save(self, db):
        db.execute_query('''
            INSERT INTO products (name, category, price)
            VALUES (?, ?, ?)
        ''', (self.name, self.category, self.price))

class IncomingGoods:
    def __init__(self, product_id, quantity, price, supplier, date):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        self.date = date
    
    def save(self, db):
        db.execute_query('''
            INSERT INTO incoming_goods (product_id, quantity, price, supplier, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.product_id, self.quantity, self.price, self.supplier, self.date))
        
        # Update stock
        current_stock = db.fetch_one('SELECT quantity FROM stock WHERE product_id = ?', 
                                   (self.product_id,))
        if current_stock:
            new_quantity = current_stock[0] + self.quantity
            db.execute_query('UPDATE stock SET quantity = ? WHERE product_id = ?',
                           (new_quantity, self.product_id))
        else:
            db.execute_query('INSERT INTO stock (product_id, quantity, min_stock) VALUES (?, ?, ?)',
                           (self.product_id, self.quantity, 10))

class OutgoingGoods:
    def __init__(self, product_id, quantity, price, customer, date):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.customer = customer
        self.date = date
    
    def save(self, db):
        db.execute_query('''
            INSERT INTO outgoing_goods (product_id, quantity, price, customer, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.product_id, self.quantity, self.price, self.customer, self.date))
        
        # Update stock
        current_stock = db.fetch_one('SELECT quantity FROM stock WHERE product_id = ?', 
                                   (self.product_id,))
        if current_stock:
            new_quantity = current_stock[0] - self.quantity
            db.execute_query('UPDATE stock SET quantity = ? WHERE product_id = ?',
                           (new_quantity, self.product_id))