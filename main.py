import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from database import Database
from widgets import LoginWindow, DashboardWindow
from styles import STYLES

class FinancialApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_user = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Financial App - Laporan Keuangan Realtime')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(STYLES['main_window'])
        
        self.show_login()
    
    def show_login(self):
        self.login_window = LoginWindow(self.db, self.on_login_success)
        self.login_window.setStyleSheet(STYLES['login_window'])
        self.setCentralWidget(self.login_window)
    
    def on_login_success(self, user):
        self.current_user = user
        self.show_dashboard()
    
    def show_dashboard(self):
        self.dashboard = DashboardWindow(self.db, self.current_user)
        self.setCentralWidget(self.dashboard)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = FinancialApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()