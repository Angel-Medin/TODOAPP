import sys
from PyQt5.QtWidgets import QApplication
from gui import ToDoApp
from database import DatabaseManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = ToDoApp(db_manager)
    window.show()
    sys.exit(app.exec_())
    