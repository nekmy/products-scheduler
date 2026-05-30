import sys
from PySide6.QtWidgets import QApplication

from product_scheduler.app.main_window import MainWindow


def main():
    app = QApplication()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
