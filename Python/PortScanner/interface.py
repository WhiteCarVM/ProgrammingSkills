import datetime
import logging
import re
import scanner
import socket
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from collections import defaultdict

class PortScannerInterFace(QMainWindow):
    '''
        Этот класс отвечает за пользовательский интерфейс: создание кнопок, окон, надписей, вывод результатов.
    '''

    def __init__(self):
        super().__init__()

        self.setup_logging()
        self.background = "708090"
        self.color = "#FFFF33"
        self.results = {}

        self.target_ports = []
        self.progress = None
        self.initUI()

# Следующий фрагмент кода отвечает за логированние
    def setup_logging(self):
        logging.basicConfig(
            filename='port_scanner.log',
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logging.info("Logging initialized.")

# Следующий фрагмент кода отвечает за интерфейс
    def initUI(self):
        '''
            Создание главного окна со всем меню
        '''
        self.setWindowTitle("PortScanner")
        self.setGeometry(360, 170, 1200, 800)

        self.createMenus()
        targetData = self.initTargetAndStart()
        optionsData = self.initOptions()
        save, start, close, output = self.createButtons()
        self.progress = QProgressBar(self)

        mainLayout = QGridLayout()
        mainLayout.addLayout(targetData, 0, 1, 1, 2)
        mainLayout.addLayout(optionsData, 0, 3, 1, 2)
        mainLayout.addWidget(save, 1, 0, 1, 1)
        mainLayout.addWidget(start, 1, 2, 1, 2)
        mainLayout.addWidget(close, 1, 5, 1, 1)
        mainLayout.addWidget(output, 2, 0, 1, 6)
        mainLayout.addWidget(self.progress, 3, 0, 1, 6) 

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)    

    def createMenus(self):
        """
            Создание меню. ДОПИСАТЬ ЕЩЕ ПАРУ ДЕЙСВИЙ!!!
        """
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet("color: red; background-color: '#FFFFFF'")
        programmMenu = mainMenu.addMenu("&Program")

        newAction = QAction("&New scan", self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("Start new scan")
        newAction.triggered.connect(self.newActionFunction)

        saveAction = QAction("Save to file", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save scanning results")
        saveAction.triggered.connect(self.saveToFile)

        exitAction = QAction("Exit from app", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit from application")
        exitAction.triggered.connect(self.exitApp)

        programmMenu.addAction(newAction)
        programmMenu.addAction(saveAction)
        programmMenu.addAction(exitAction)

        helpMenu = mainMenu.addMenu("&Help")

        helpAction = QAction("Read manual", self)
        helpAction.setShortcut("Ctrl+M")
        helpAction.setStatusTip("Read about this tool")
        helpAction.triggered.connect(self.helpActionFunction)

        helpMenu.addAction(helpAction)

        aboutMenu = mainMenu.addMenu("&About")

        aboutAction = QAction("About developer", self)
        aboutAction.setShortcut("Ctrl+I")
        aboutAction.setStatusTip("Read about developer this tool")
        aboutAction.triggered.connect(self.aboutActionFunction)

        aboutMenu.addAction(aboutAction)

    def initOptions(self):
        """
            Функция выбора некоторых опций. Задается TCP или UDP сканирование. ДОПИСАТЬ ПАРУ ФУНКЦИЙ!!!
        """
        optionsLayout = QGridLayout()

        tcpScan = QRadioButton("TCP scanning")
        tcpScan.clicked.connect(self.tcp_scan)

        udpScan = QRadioButton("UDP scanning")
        udpScan.clicked.connect(self.udp_scan)

        max_workers_label = QLabel("Threads:")
        max_workers_label.setFont(QFont("Times", 15))
        max_workers_label.setStyleSheet(f"color: {self.color};")
        max_workers_label.setAlignment(Qt.AlignLeft)

        self.max_workers = QLineEdit()
        self.max_workers.setStyleSheet(f"background-color: white; color: black;")
        self.max_workers.setPlaceholderText("Example: 10")
        self.max_workers.setMaximumWidth(200)

        optionsVLayout = QGridLayout()
        optionsVLayout.addWidget(tcpScan, 0, 0, 1, 1)
        optionsVLayout.addWidget(udpScan, 0, 1, 1, 1)
        optionsVLayout.addWidget(max_workers_label, 2, 0, 1, 1)
        optionsVLayout.addWidget(self.max_workers, 2, 1, 1, 1)

        optionsFrame = QFrame()
        optionsFrame.setFrameShape(QFrame.Box)
        optionsFrame.setFrameShadow(QFrame.Raised)
        optionsFrame.setLineWidth(3)
        optionsFrame.setStyleSheet(f"color: {self.color}; border: 2px solid {self.color}; border-radius: 5px;")
        optionsFrame.setLayout(optionsVLayout)

        optionsLayout.addWidget(optionsFrame, 0, 0, 1, 2)

        return optionsLayout

    def start_scan(self):
        # Запуск сканирования в потоке
        logging.info("Scan started.")
        self.progress.setValue(0)
        
        # Стандартный список портов для примера. Укажите ваши порты
        self.target_ports = list(range(1, 1024))  # Измените по необходимости

        self.worker_thread = threading.Thread(target=self.scan_ports)
        self.worker_thread.start()

    def scan_ports(self):
        total_ports = len(self.target_ports)
        for i, port in enumerate(self.target_ports):
            # Здесь разместите код для сканирования порта
            logging.info(f"Scanning port {port}...")

            # Логика сканирования порта
            # Например, socket соединение

            # Обновление индикатора прогресса
            progress_value = int((i + 1) / total_ports * 100)
            self.update_progress(progress_value)
        
        logging.info("Scan completed.")

    def update_progress(self, value):
        # Обновление прогресса в главном потоке
        QtCore.QMetaObject.invokeMethod(self.progress, "setValue", QtCore.Qt.QueuedConnection, QtCore.QVariant(value))

    def createButtons(self):
        """
            Создание главных кнопок. Все три кнопки работают!!!
        """
        saveButton = QPushButton("Save to file")
        saveButton.setFont(QFont("Times", 15))
        saveButton.setStyleSheet(f"background-color: '#776699'; color: {self.color}")
        saveButton.clicked.connect(self.saveToFile)

        scanningButton = QPushButton("Start scanning")
        scanningButton.setFont(QFont("Times", 15))
        scanningButton.setStyleSheet(f"background-color: '#776699'; color: {self.color};")
        scanningButton.clicked.connect(self.scanningResults)
        scanningButton.setShortcut("Ctrl+B")

        exitButton = QPushButton("Exit")
        exitButton.setFont(QFont("Times", 15))
        exitButton.setStyleSheet(f"background-color: '#776699'; color: {self.color}")
        exitButton.clicked.connect(self.exitApp)

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setStyleSheet("background-color:white; color: black;")

        return saveButton, scanningButton, exitButton, self.outputText

#Следующий фрагмент кода отвечает за типы сканирования

    def tcp_scan(self):
        """
            Функция, подключащая TCP сканирование
        """
        try:
            if (self.is_valid_ports(self.targetPortEdit.text()) and self.targetPortEdit.text() != "") and \
                (self.is_valid_ip(self.targetEdit.text()) and self.targetEdit.text() != ""):
                self.results = scanner.TCPscan(self.targetEdit.text(), self.targetPortEdit.text())
            else:
                pass
        except Exception as ex:
            logging.error(f"Error during TCP scanning: {ex}")
            self.outputText.append(f"<h4><b style='color: red;'>Error during TCP scan: {ex}</b></h4> \n")

    def udp_scan(self):
        """
            Функция, подключащая UDP сканирование
        """
        try:
            if (self.is_valid_ports(self.targetPortEdit.text()) and self.targetPortEdit.text() != "") and \
                (self.is_valid_ip(self.targetEdit.text()) and self.targetEdit.text() != ""):
                self.results = scanner.UDPscan(self.targetEdit.text(), self.targetPortEdit.text()) 
            else:
                pass
        except Exception as ex:
            logging.error(f"Error during UDP scanning: {ex}")
            self.outputText.append(f"<h4><b style='color: red;'>Error during UDP scan: {ex}</b></h4> \n")

#Следующий фрагмент кода отвечает за функции меню

    def newActionFunction(self):
        """
            Функция начала нового сканирования
        """
        self.targetEdit.clear()
        self.targetPortEdit.clear()
        self.max_workers.clear()
        self.outputText.clear()
        self.results.clear()

    def helpActionFunction(self):
        """
            Функция для объяснения прииложения
        """
        msg = QMessageBox()
        msg.setWindowTitle("Manual")
        msg.setText("The information about tool and manual you can read <a href='https://github.com/WhiteCarVM/ProgrammingSkills/tree/main/Python/PortScanner'>here</a>")
        msg.setTextFormat(Qt.RichText)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def aboutActionFunction(self):
        """
            Функция для представления разработчика
        """
        message_box = QMessageBox()
        message_box.setWindowTitle("About developer")
        message_box.setText("The information about developer you can read <a href='https://github.com/WhiteCarVM/ProgrammingSkills/tree/main/Python/PortScanner'>here</a>.")
        message_box.setTextFormat(Qt.RichText)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()

    def saveToFile(self):
        """
            Функция сохранения в файл. ИЗМЕНИТЬ ФОРМАТ ЗАПИСИ!!!
        """
        try:
            filename, _ =QFileDialog.getSaveFileName(self, "Save file", "./", "Text file(*.txt);;All files(*.*)")

            if filename:
                with open(filename, "w") as file:
                    file.write("\tInformation about scanning:\n")
                    if self.is_valid_ip(self.targetEdit.text()):
                        file.write(f"1. IP address: {self.targetEdit.text()}\n")
                    else:
                        file.write(f"1. IP address: invalid range of IP\n")
                    if self.is_valid_ports(self.targetPortEdit.text()):
                        file.write(f"2. Ports: {self.targetPortEdit.text()}\n")
                    else:
                        file.write(f"1. IP address: invalid range of ports\n")
                    file.write(f"4. Scanning starts at {datetime.datetime.now()}")
                    for key, value in self.results.items():
                        file.write(f"\n\n\tResults of scanning {key}:")
                        file.write("\n---------------------------------------------------------------------\n")
                        file.write("|\tPort\t|\tStatus\t    |\tService\t    |\tVersion\t    |")
                        file.write("\n---------------------------------------------------------------------\n")

                        for result in value:
                            file.write("|               |                   |               |               |\n")
                            file.write(f"|\t{result[0]}\t|\t{result[1]}\t    |\t{result[2]}\t    |\tNone\t    |\n")
                            file.write("|               |                   |               |               |\n")
                            file.write("---------------------------------------------------------------------\n")
        except Exception as ex:
            logging.error(f"Error saving to file: {ex}")
            self.outputText.append(f"<h4><b style='color: red;'>Error saving to file: {ex}</b></h4> \n")

    def exitApp(self):
        """
            Функция закрытия приложения
        """
        exitBox = QMessageBox()
        exitBox.setWindowTitle("Exit")
        exitBox.setText("Are you really want to exit the application?")
        exitBox.setGeometry(750, 450, 400, 300)
        exitBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        exitBox.setDefaultButton(QMessageBox.Yes)

        result = exitBox.exec_()
        if result == QMessageBox.Yes:
            sys.exit(0)

    def scanningResults(self):
        """
            Функция вывода информации на главный экран.
        """
        try:
            self.outputText.clear()
            if self.is_valid_ip(self.targetEdit.text()):
                self.outputText.append(f"<h4><b>IP address: </b><b style='color: green;'>{self.targetEdit.text()}</b></h4>")
            else:
                self.outputText.append(f"<h4><b>IP address: </b><b style='color: red;'>invalid range of IP</b></h4>")
            if self.is_valid_ports(self.targetPortEdit.text()):
                self.outputText.append(f"<h4><b>Ports: </b><b style='color: green;'>{self.targetPortEdit.text()}</b></h4>")
            else:
                self.outputText.append(f"<h4><b>Ports: </b><b style='color: red;'>invalid range of ports</b></h4>")
            self.outputText.append(f"<h4><b>Scanning starts at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</b></h4> \n")

            headers = ["Port\t", "Status\t", "Service\t", "Version\t"]

            if not self.results:
                self.outputText.append(f"\n\t<h4><b style='color: red'>No results to display</b></h4>\n")
                return

            try:
                for key, value in self.results.items():
                    self.outputText.append(f"\n\n\t<h4><b>Results of scanning {key}</b></h4> \n")
                    self.cursor = QTextCursor()
                    self.cursor = self.outputText.textCursor()
                    self.cursor.insertTable(len(value)+1, len(headers))


                    for header in headers:
                        self.cursor.insertText(header)
                        self.cursor.movePosition(QTextCursor.NextCell)

                    for i in range(len(value)):
                        self.cursor.insertText(str(value[i][0]))
                        self.cursor.movePosition(QTextCursor.NextCell)
                        self.cursor.insertText(value[i][1])
                        self.cursor.movePosition(QTextCursor.NextCell)
                        self.cursor.insertText(value[i][2])
                        self.cursor.movePosition(QTextCursor.NextCell)
                        self.cursor.movePosition(QTextCursor.NextCell)
            except:
                self.outputText.append(f"\n\t<h4><b style='color: red'>Please choose the type of scanning</b></h4>\n")
        except Exception as ex:
            logging.error(f"Error displaying scanning results: {ex}")
            self.outputText.append(f"<h4><b style='color: red;'>Error displaying scaning results: {ex}</b></h4> \n")

#Следующий код отвечает за фильтрацию результатов 

    def initTargetAndStart(self):
        """
            Фильтрация пользовательского ввода. Инициализация цели и портов для сканирования.
        """
        targetLayout = QGridLayout()
        targetLayout.setSpacing(20)

        targetLabel = QLabel("IP address:")
        targetLabel.setFont(QFont("Times", 15))
        targetLabel.setStyleSheet(f"color: {self.color};")
        targetLabel.setAlignment(Qt.AlignLeft)

        self.targetEdit = QLineEdit()
        self.targetEdit.setStyleSheet(f"background-color: white; color: black;")
        self.targetEdit.setPlaceholderText("Example: 8.8.8.8")
        self.targetEdit.setMaximumWidth(200)

        targetPortLabel = QLabel("Ports:")
        targetPortLabel.setFont(QFont("Times", 15))
        targetPortLabel.setStyleSheet(f"color: {self.color};")

        try:
            self.targetPortEdit = QLineEdit()
            self.targetPortEdit.setStyleSheet("background-color: white; color: black;")
            self.targetPortEdit.setPlaceholderText("Example: 1-1024 or 22")
            self.targetPortEdit.setMaximumWidth(200)
        except Exception as ex:
            print(f"Error: {ex}")

        targetVLayout = QGridLayout()
        targetVLayout.addWidget(targetLabel, 0, 0)
        targetVLayout.addWidget(self.targetEdit, 0, 1, 1, 2)
        targetVLayout.addWidget(targetPortLabel, 1, 0)
        targetVLayout.addWidget(self.targetPortEdit, 1, 1, 1, 2)

        targetFrame = QFrame()
        targetFrame.setFrameShape(QFrame.Box)
        targetFrame.setFrameShadow(QFrame.Raised)
        targetFrame.setLineWidth(3)
        targetFrame.setStyleSheet(f"color: {self.color}; border: 2px solid {self.color}; border-radius: 5px;")
        targetFrame.setLayout(targetVLayout)

        targetLayout.addWidget(targetFrame, 0, 0, 1, 2)

        return targetLayout

    def is_valid_ports(self, ports):
        """
            Функция проверки правильности введенных портов.
        """
        if "-" in ports:
            start_port, end_port = ports.split("-")
            if start_port.isdigit() and end_port.isdigit():
                start_port, end_port = int(start_port), int(end_port)
                return 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port
        elif "," in ports:
            ports = ports.split(",")
            for port in ports:
                if not (port.isdigit() and 1 <= int(port) <= 65535):
                    return False
            return True
        else:
            return ports.isdigit() and 1 <= int(ports) <= 65535
        return False

    def is_valid_ip(self, ip):
        """
            Функция проверки правильности введенного IP адреса или CIDR.
        """
        ip_pattern = re.compile(
            r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        )
        cidr_pattern = re.compile(
            r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$'
        )
        range_pattern = re.compile(
            r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}-(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        )

        list_pattern = re.compile(
            r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:,(?:[0-9]{1,3}\.){3}[0-9]{1,3})*$'
        )

        if ip_pattern.match(ip):
            return all(0 <= int(part) <= 255 for part in ip.split('.'))
        elif cidr_pattern.match(ip):
            address, subnet = ip.split('/')
            if not all(0 <= int(part) <= 255 for part in address.split('.')):
                return False
            return 0 <= int(subnet) <= 32
        elif range_pattern.match(ip):
            start_ip, end_ip = ip.split('-')
            return all(0 <= int(part) <= 255 for part in start_ip.split('.')) and \
               all(0 <= int(part) <= 255 for part in end_ip.split('.'))
        elif list_pattern.match(ip):
            ip_addresses = ip.split(',')
            return all(self.is_valid_ip(addr) for addr in ip_addresses)

        return False

    def closeEvent(self, event):
        """ 
        Обработка события закрытия окна 
        """
        reply = QMessageBox.question(
            self,
            'Exit Application',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()