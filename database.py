import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        # Buat folder data jika belum ada
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.conn = sqlite3.connect('data/financial_app.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabel User/Role
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Karyawan
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL,
                hire_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Product
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Stock Barang
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_stock INTEGER NOT NULL DEFAULT 10,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Tabel Barang Masuk
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incoming_goods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                supplier TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Tabel Barang Keluar
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outgoing_goods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                customer TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Insert default admin user
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, role) 
            VALUES (?, ?, ?)
        ''', ('admin', 'admin123', 'admin'))
        
        # Insert sample data untuk testing
        cursor.execute('''
            INSERT OR IGNORE INTO products (name, category, price) 
            VALUES (?, ?, ?)
        ''', ('Sample Product', 'General', 100000))
        
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def fetch_all(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def fetch_one(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def close(self):
        self.conn.close()