STYLES = {
    'main_window': """
        QMainWindow {
            background-color: #f0f0f0;
        }
    """,
    'login_window': """
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                      stop:0 #667eea, stop:1 #764ba2);
        }
        QLabel {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }
        QLineEdit {
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """,
    'button_primary': """
        QPushButton {
            background-color: #007bff;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
    """,
    'button_success': """
        QPushButton {
            background-color: #28a745;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #218838;
        }
    """,
    'button_danger': """
        QPushButton {
            background-color: #dc3545;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #c82333;
        }
    """,
    'table_widget': """
        QTableWidget {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        QHeaderView::section {
            background-color: #f8f9fa;
            padding: 8px;
            border: 1px solid #dee2e6;
            font-weight: bold;
        }
    """
}