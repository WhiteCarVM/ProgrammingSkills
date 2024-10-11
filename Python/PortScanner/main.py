from PyQt5.QtWidgets import QApplication

import sys

import interface

if __name__ == "__main__":
    """
        Функция запуска приложения.
    """
    app = QApplication(sys.argv)
    scanner = interface.PortScannerInterFace()
    scanner.show()
    sys.exit(app.exec_())