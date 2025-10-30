from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QComboBox, QDateEdit,
                             QMessageBox, QTabWidget, QFormLayout,
                             QGroupBox, QTextEdit, QHeaderView)
from PyQt5.QtCore import QDate, Qt
from datetime import datetime

class LoginWindow(QWidget):
    def __init__(self, db, on_login_success):
        super().__init__()
        self.db = db
        self.on_login_success = on_login_success
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login - Financial App')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Financial App Login')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 24px; font-weight: bold; color: white; margin-bottom: 30px;')
        
        # Form
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)
        
        # Login Button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.login)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(login_btn)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill all fields!')
            return
        
        user = self.db.fetch_one('SELECT * FROM users WHERE username = ? AND password = ?', 
                               (username, password))
        
        if user:
            self.on_login_success(user)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password!')

class DashboardWindow(QWidget):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel(f'Dashboard - Welcome {self.user[1]} ({self.user[3]})')
        header.setStyleSheet('font-size: 18px; font-weight: bold; margin: 10px;')
        
        # Tabs
        tabs = QTabWidget()
        
        # Employee Tab
        employee_tab = EmployeeTab(self.db)
        tabs.addTab(employee_tab, "Karyawan")
        
        # Product Tab
        product_tab = ProductTab(self.db)
        tabs.addTab(product_tab, "Product")
        
        # Stock Tab
        stock_tab = StockTab(self.db)
        tabs.addTab(stock_tab, "Stock Barang")
        
        # Incoming Goods Tab
        incoming_tab = IncomingGoodsTab(self.db)
        tabs.addTab(incoming_tab, "Barang Masuk")
        
        # Outgoing Goods Tab
        outgoing_tab = OutgoingGoodsTab(self.db)
        tabs.addTab(outgoing_tab, "Barang Keluar")
        
        # Report Tab
        report_tab = ReportTab(self.db)
        tabs.addTab(report_tab, "Laporan")
        
        layout.addWidget(header)
        layout.addWidget(tabs)
        
        self.setLayout(layout)

class EmployeeTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Form
        form_group = QGroupBox("Tambah Karyawan")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.position_input = QLineEdit()
        self.salary_input = QLineEdit()
        self.hire_date_input = QDateEdit()
        self.hire_date_input.setDate(QDate.currentDate())
        self.hire_date_input.setCalendarPopup(True)
        
        form_layout.addRow("Nama:", self.name_input)
        form_layout.addRow("Posisi:", self.position_input)
        form_layout.addRow("Gaji:", self.salary_input)
        form_layout.addRow("Tanggal Masuk:", self.hire_date_input)
        
        add_btn = QPushButton("Tambah Karyawan")
        add_btn.clicked.connect(self.add_employee)
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px;")
        
        form_layout.addRow(add_btn)
        form_group.setLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Nama', 'Posisi', 'Gaji', 'Tanggal Masuk'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(form_group)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def add_employee(self):
        name = self.name_input.text()
        position = self.position_input.text()
        salary = self.salary_input.text()
        hire_date = self.hire_date_input.date().toString("yyyy-MM-dd")
        
        if not name or not position or not salary:
            QMessageBox.warning(self, 'Error', 'Please fill all fields!')
            return
        
        try:
            salary = float(salary)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Salary must be a number!')
            return
        
        self.db.execute_query('''
            INSERT INTO employees (name, position, salary, hire_date)
            VALUES (?, ?, ?, ?)
        ''', (name, position, salary, hire_date))
        
        QMessageBox.information(self, 'Success', 'Employee added successfully!')
        self.clear_form()
        self.load_data()
    
    def clear_form(self):
        self.name_input.clear()
        self.position_input.clear()
        self.salary_input.clear()
        self.hire_date_input.setDate(QDate.currentDate())
    
    def load_data(self):
        employees = self.db.fetch_all('SELECT * FROM employees ORDER BY id DESC')
        self.table.setRowCount(len(employees))
        
        for row, employee in enumerate(employees):
            for col, data in enumerate(employee):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

class ProductTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Form
        form_group = QGroupBox("Tambah Product")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.price_input = QLineEdit()
        
        form_layout.addRow("Nama Product:", self.name_input)
        form_layout.addRow("Kategori:", self.category_input)
        form_layout.addRow("Harga:", self.price_input)
        
        add_btn = QPushButton("Tambah Product")
        add_btn.clicked.connect(self.add_product)
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px;")
        
        form_layout.addRow(add_btn)
        form_group.setLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Nama', 'Kategori', 'Harga'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(form_group)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def add_product(self):
        name = self.name_input.text()
        category = self.category_input.text()
        price = self.price_input.text()
        
        if not name or not category or not price:
            QMessageBox.warning(self, 'Error', 'Please fill all fields!')
            return
        
        try:
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Price must be a number!')
            return
        
        self.db.execute_query('''
            INSERT INTO products (name, category, price)
            VALUES (?, ?, ?)
        ''', (name, category, price))
        
        QMessageBox.information(self, 'Success', 'Product added successfully!')
        self.clear_form()
        self.load_data()
    
    def clear_form(self):
        self.name_input.clear()
        self.category_input.clear()
        self.price_input.clear()
    
    def load_data(self):
        products = self.db.fetch_all('SELECT * FROM products ORDER BY id DESC')
        self.table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            for col, data in enumerate(product):
                if col == 3:  # Format harga
                    self.table.setItem(row, col, QTableWidgetItem(f"Rp {data:,.2f}"))
                else:
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))

class StockTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        refresh_btn = QPushButton("Refresh Stock")
        refresh_btn.clicked.connect(self.load_data)
        refresh_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; margin: 5px;")
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Product', 'Quantity', 'Min Stock', 'Status'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(refresh_btn)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_data(self):
        stock_data = self.db.fetch_all('''
            SELECT s.id, p.name, s.quantity, s.min_stock 
            FROM stock s 
            JOIN products p ON s.product_id = p.id
            ORDER BY s.id DESC
        ''')
        
        self.table.setRowCount(len(stock_data))
        
        for row, data in enumerate(stock_data):
            for col, value in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Determine status
            quantity = data[2]
            min_stock = data[3]
            status = "Aman" if quantity >= min_stock else "Perlu Restock"
            
            status_item = QTableWidgetItem(status)
            if status == "Perlu Restock":
                status_item.setBackground(Qt.red)
                status_item.setForeground(Qt.white)
            else:
                status_item.setBackground(Qt.green)
                status_item.setForeground(Qt.white)
                
            self.table.setItem(row, 4, status_item)

class IncomingGoodsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_products()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Form
        form_group = QGroupBox("Barang Masuk")
        form_layout = QFormLayout()
        
        self.product_combo = QComboBox()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        self.supplier_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        
        form_layout.addRow("Product:", self.product_combo)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Harga:", self.price_input)
        form_layout.addRow("Supplier:", self.supplier_input)
        form_layout.addRow("Tanggal:", self.date_input)
        
        add_btn = QPushButton("Tambah Barang Masuk")
        add_btn.clicked.connect(self.add_incoming)
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px;")
        
        form_layout.addRow(add_btn)
        form_group.setLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Product', 'Quantity', 'Harga', 'Supplier', 'Tanggal', 'Total'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(form_group)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_products(self):
        products = self.db.fetch_all('SELECT id, name FROM products')
        self.product_combo.clear()
        for product in products:
            self.product_combo.addItem(f"{product[1]}", product[0])
    
    def add_incoming(self):
        product_id = self.product_combo.currentData()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        supplier = self.supplier_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        
        if not product_id or not quantity or not price or not supplier:
            QMessageBox.warning(self, 'Error', 'Please fill all fields!')
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Quantity and Price must be numbers!')
            return
        
        # Add to incoming goods
        self.db.execute_query('''
            INSERT INTO incoming_goods (product_id, quantity, price, supplier, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, quantity, price, supplier, date))
        
        # Update stock
        current_stock = self.db.fetch_one('SELECT quantity FROM stock WHERE product_id = ?', (product_id,))
        if current_stock:
            new_quantity = current_stock[0] + quantity
            self.db.execute_query('UPDATE stock SET quantity = ? WHERE product_id = ?', (new_quantity, product_id))
        else:
            self.db.execute_query('INSERT INTO stock (product_id, quantity, min_stock) VALUES (?, ?, ?)', 
                                (product_id, quantity, 10))
        
        QMessageBox.information(self, 'Success', 'Incoming goods recorded successfully!')
        self.clear_form()
        self.load_data()
    
    def clear_form(self):
        self.quantity_input.clear()
        self.price_input.clear()
        self.supplier_input.clear()
        self.date_input.setDate(QDate.currentDate())
    
    def load_data(self):
        incoming_data = self.db.fetch_all('''
            SELECT ig.id, p.name, ig.quantity, ig.price, ig.supplier, ig.date 
            FROM incoming_goods ig 
            JOIN products p ON ig.product_id = p.id 
            ORDER BY ig.id DESC
        ''')
        
        self.table.setRowCount(len(incoming_data))
        
        for row, data in enumerate(incoming_data):
            for col, value in enumerate(data):
                if col == 3:  # Format harga
                    self.table.setItem(row, col, QTableWidgetItem(f"Rp {value:,.2f}"))
                else:
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Calculate total
            quantity = data[2]
            price = data[3]
            total = quantity * price
            self.table.setItem(row, 6, QTableWidgetItem(f"Rp {total:,.2f}"))

class OutgoingGoodsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_products()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Form
        form_group = QGroupBox("Barang Keluar")
        form_layout = QFormLayout()
        
        self.product_combo = QComboBox()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        self.customer_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        
        form_layout.addRow("Product:", self.product_combo)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Harga:", self.price_input)
        form_layout.addRow("Customer:", self.customer_input)
        form_layout.addRow("Tanggal:", self.date_input)
        
        add_btn = QPushButton("Tambah Barang Keluar")
        add_btn.clicked.connect(self.add_outgoing)
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px;")
        
        form_layout.addRow(add_btn)
        form_group.setLayout(form_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Product', 'Quantity', 'Harga', 'Customer', 'Tanggal', 'Total'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(form_group)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_products(self):
        products = self.db.fetch_all('SELECT id, name FROM products')
        self.product_combo.clear()
        for product in products:
            self.product_combo.addItem(f"{product[1]}", product[0])
    
    def add_outgoing(self):
        product_id = self.product_combo.currentData()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        customer = self.customer_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        
        if not product_id or not quantity or not price or not customer:
            QMessageBox.warning(self, 'Error', 'Please fill all fields!')
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Quantity and Price must be numbers!')
            return
        
        # Check stock availability
        current_stock = self.db.fetch_one('SELECT quantity FROM stock WHERE product_id = ?', (product_id,))
        if not current_stock or current_stock[0] < quantity:
            QMessageBox.warning(self, 'Error', 'Insufficient stock!')
            return
        
        # Add to outgoing goods
        self.db.execute_query('''
            INSERT INTO outgoing_goods (product_id, quantity, price, customer, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, quantity, price, customer, date))
        
        # Update stock
        new_quantity = current_stock[0] - quantity
        self.db.execute_query('UPDATE stock SET quantity = ? WHERE product_id = ?', (new_quantity, product_id))
        
        QMessageBox.information(self, 'Success', 'Outgoing goods recorded successfully!')
        self.clear_form()
        self.load_data()
    
    def clear_form(self):
        self.quantity_input.clear()
        self.price_input.clear()
        self.customer_input.clear()
        self.date_input.setDate(QDate.currentDate())
    
    def load_data(self):
        outgoing_data = self.db.fetch_all('''
            SELECT og.id, p.name, og.quantity, og.price, og.customer, og.date 
            FROM outgoing_goods og 
            JOIN products p ON og.product_id = p.id 
            ORDER BY og.id DESC
        ''')
        
        self.table.setRowCount(len(outgoing_data))
        
        for row, data in enumerate(outgoing_data):
            for col, value in enumerate(data):
                if col == 3:  # Format harga
                    self.table.setItem(row, col, QTableWidgetItem(f"Rp {value:,.2f}"))
                else:
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Calculate total
            quantity = data[2]
            price = data[3]
            total = quantity * price
            self.table.setItem(row, 6, QTableWidgetItem(f"Rp {total:,.2f}"))

class ReportTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.generate_report()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Controls
        controls_layout = QHBoxLayout()
        
        start_date_label = QLabel("Dari:")
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        
        end_date_label = QLabel("Sampai:")
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.generate_report)
        generate_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px;")
        
        controls_layout.addWidget(start_date_label)
        controls_layout.addWidget(self.start_date)
        controls_layout.addWidget(end_date_label)
        controls_layout.addWidget(self.end_date)
        controls_layout.addWidget(generate_btn)
        controls_layout.addStretch()
        
        # Report Display
        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        
        layout.addLayout(controls_layout)
        layout.addWidget(self.report_display)
        
        self.setLayout(layout)
    
    def generate_report(self):
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        # Get incoming goods total
        incoming_total = self.db.fetch_one('''
            SELECT SUM(quantity * price) FROM incoming_goods 
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        # Get outgoing goods total
        outgoing_total = self.db.fetch_one('''
            SELECT SUM(quantity * price) FROM outgoing_goods 
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        incoming_total = incoming_total[0] if incoming_total[0] else 0
        outgoing_total = outgoing_total[0] if outgoing_total[0] else 0
        profit = outgoing_total - incoming_total
        
        report_text = f"LAPORAN KEUANGAN\n"
        report_text += f"Periode: {start_date} sampai {end_date}\n"
        report_text += "=" * 50 + "\n\n"
        report_text += f"Total Pengeluaran (Barang Masuk): Rp {incoming_total:,.2f}\n"
        report_text += f"Total Pemasukan (Barang Keluar):  Rp {outgoing_total:,.2f}\n"
        report_text += "-" * 50 + "\n"
        report_text += f"Laba/Rugi:                        Rp {profit:,.2f}\n\n"
        
        # Add detail incoming goods
        report_text += "DETAIL BARANG MASUK:\n"
        incoming_details = self.db.fetch_all('''
            SELECT p.name, ig.quantity, ig.price, ig.supplier, ig.date 
            FROM incoming_goods ig 
            JOIN products p ON ig.product_id = p.id 
            WHERE ig.date BETWEEN ? AND ?
            ORDER BY ig.date
        ''', (start_date, end_date))
        
        for item in incoming_details:
            total = item[1] * item[2]
            report_text += f"  {item[4]} - {item[0]} ({item[1]} x Rp {item[2]:,.2f}) = Rp {total:,.2f} - {item[3]}\n"
        
        report_text += "\nDETAIL BARANG KELUAR:\n"
        outgoing_details = self.db.fetch_all('''
            SELECT p.name, og.quantity, og.price, og.customer, og.date 
            FROM outgoing_goods og 
            JOIN products p ON og.product_id = p.id 
            WHERE og.date BETWEEN ? AND ?
            ORDER BY og.date
        ''', (start_date, end_date))
        
        for item in outgoing_details:
            total = item[1] * item[2]
            report_text += f"  {item[4]} - {item[0]} ({item[1]} x Rp {item[2]:,.2f}) = Rp {total:,.2f} - {item[3]}\n"
        
        self.report_display.setText(report_text)