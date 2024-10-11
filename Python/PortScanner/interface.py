from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import socket
import datetime

import scanner

class PortScannerInterFace(QMainWindow):
    '''
        Этот класс отвечает за пользовательский интерфейс: создание кнопок, окон, надписей, вывод результатов.  
    '''

    def __init__(self):
        super().__init__()
        
        self.background = "708090"
        self.color = "#FFFF33"

        self.initUI()
        
    def initUI(self):
        '''
            Создание главного окна со всем меню, 
        '''
        self.setWindowTitle("PortScanner")
        self.setGeometry(360, 170, 1200, 800)

        self.createMenus()
        targetData = self.initTargetAndStart()
        optionsData = self.initOptions()
        save, start, close, output = self.createButtons()

        mainLayout = QGridLayout()
        mainLayout.addLayout(targetData, 0, 1, 1, 2)  
        mainLayout.addLayout(optionsData, 0, 3, 1, 2)   
        mainLayout.addWidget(save, 1, 0, 1, 1)
        mainLayout.addWidget(start, 1, 2, 1, 2)
        mainLayout.addWidget(close, 1, 5, 1, 1)
        mainLayout.addWidget(output, 2, 0, 1, 6)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def createMenus(self):
        """
            Создание меню (функциональность практически отсутствует). ДОПИСАТЬ!!!
        """
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet("color: red; background-color: #FFFFFF")
        fileMenu = mainMenu.addMenu("&File")

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

        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        helpMenu = mainMenu.addMenu("&Help")

        helpAction = QAction("Read manual", self)
        helpAction.setShortcut("Ctrl+M")
        helpAction.setStatusTip("Read about this tool")
        helpAction.triggered.connect(self.helpActionFunction)
        
        helpMenu.addAction(helpAction)

        aboutMenu = mainMenu.addMenu("&About")

        aboutAction = QAction("About developer", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutAction.setStatusTip("Read about developer this tool")
        aboutAction.triggered.connect(self.aboutActionFunction)

        aboutMenu.addAction(aboutAction)

    def newActionFunction(self):
        """
            Функция начала нового сканирования
        """
        self.targetEdit.clear()
        self.targetPortEdit.clear()
        self.outputText.clear()

    def helpActionFunction(self):
        """
            Функция для объяснения прииложения 
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Manual")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def aboutActionFunction(self):
        """
            Функция для представления разработчика
        """
        pass

    def initTargetAndStart(self):
        """
            Фильтрация пользовательского ввода. Инициализация цели и портов для сканирования.
        """
        targetLayout = QGridLayout()
        targetLayout.setSpacing(20)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegExp = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "(?:," + ipRange + "\\." + ipRange + "\\." 
        + ipRange + "\\." + ipRange + "|\\-" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "|/[0-9]?[0-9])?$")
        ipValidator = QRegExpValidator(ipRegExp, self)
        
        targetLabel = QLabel("IP address:")
        targetLabel.setFont(QFont("Times", 15))
        targetLabel.setStyleSheet(f"color: {self.color};")
        targetLabel.setAlignment(Qt.AlignLeft)
        
        self.targetEdit = QLineEdit()
        self.targetEdit.setStyleSheet(f"background-color: white; color: black;")
        self.targetEdit.setValidator(ipValidator)
        self.targetEdit.setPlaceholderText("Example: 8.8.8.8")
        self.targetEdit.setMaximumWidth(200)

        portRange = "([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-6][0-9][0-9][0-9][0-9])"
        portRegExp = QRegExp("^" + portRange + "-" + portRange + "$")
        portValidator = QRegExpValidator(portRegExp, self)
        
        targetPortLabel = QLabel("Ports:")
        targetPortLabel.setFont(QFont("Times", 15))
        targetPortLabel.setStyleSheet(f"color: {self.color};")

        self.targetPortEdit = QLineEdit()
        self.targetPortEdit.setStyleSheet("background-color: white; color: black;")
        self.targetPortEdit.setValidator(portValidator)
        self.targetPortEdit.setPlaceholderText("Example: 1-1024 or 22")
        self.targetPortEdit.setMaximumWidth(200)

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

    def initOptions(self):
        """ 
            Функция выбора некоторых опций. Задается TCP или UDP сканирование, но не работает. ДОПИСАТЬ ПАРУ ФУНКЦИЙ И ПЕРЕПИСАТЬ СУЩЕСТВУЮЩУЮ!!! 
        """
        optionsLayout = QGridLayout()

        timerLabel = QLabel("Timer")
        timerLabel.setFont(QFont("Times", 15))
        timerLabel.setStyleSheet(f"color: {self.color}")

        self.timerBox = QSpinBox()
        self.timerBox.setRange(5, 60)
        self.timerBox.setSingleStep(1)

        tcpScan = QRadioButton("TCP scanning")

        udpScan = QRadioButton("UDP scanning")

        optionsVLayout = QGridLayout()
        optionsVLayout.addWidget(timerLabel, 0, 0, 1, 1)
        optionsVLayout.addWidget(self.timerBox, 0, 1, 1, 1)
        optionsVLayout.addWidget(tcpScan, 2, 0, 1, 1)
        optionsVLayout.addWidget(udpScan, 2, 1, 1, 1)

        optionsFrame = QFrame()
        optionsFrame.setFrameShape(QFrame.Box)
        optionsFrame.setFrameShadow(QFrame.Raised)
        optionsFrame.setLineWidth(3)
        optionsFrame.setStyleSheet(f"color: {self.color}; border: 2px solid {self.color}; border-radius: 5px;")
        optionsFrame.setLayout(optionsVLayout)

        optionsLayout.addWidget(optionsFrame, 0, 0, 1, 2)

        return optionsLayout

    def createButtons(self):
        """
            Создание главных кнопок. Все три кнопки работают. ДОПИСАТЬ ПАРУ КНОПОК!!!
        """
        saveButton = QPushButton("Save to file")
        saveButton.setFont(QFont("Times", 15))
        saveButton.setStyleSheet(f"background-color: #FF00FF; color: {self.color}")
        saveButton.clicked.connect(self.saveToFile)

        scanningButton = QPushButton("Start scanning")
        scanningButton.setFont(QFont("Times", 15))
        scanningButton.setStyleSheet(f"background-color: #FF00FF; color: {self.color};")
        scanningButton.clicked.connect(self.scanningResults)
        scanningButton.setShortcut("Ctrl+B")    

        exitButton = QPushButton("Exit")
        exitButton.setFont(QFont("Times", 15))
        exitButton.setStyleSheet(f"background-color: #FF00FF; color: {self.color}")
        exitButton.clicked.connect(self.exitApp)

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setStyleSheet("background-color:white; color: black;")

        return saveButton, scanningButton, exitButton, self.outputText

    def saveToFile(self):
        """
            Функция сохранения в файл. ИЗМЕНИТЬ ФОРМАТ ЗАПИСИ!!!
        """
        filename, _ =QFileDialog.getSaveFileName(self, "Save file", "./", "Text file(*.txt);;All files(*.*)")
        
        if filename:
            with open(filename, "w") as file:
                file.write("\tInformation about scanning:\n")
                file.write(f"1. IP address: {self.targetEdit.text()}\n")
                file.write(f"2. Ports: {self.targetPortEdit.text()}\n")
                file.write(f"3. Timer: {self.timerBox.value()}\n")
                file.write(f"4. Scanning starts at {datetime.datetime.now()}")
                file.write("Port\tStatus\tService\tVersion")
                
                
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
        self.outputText.clear()
        self.outputText.append(f"<h4><b>IP address:</b> {self.targetEdit.text()}</h4>")
        self.outputText.append(f"<h4><b>Ports:</b> {self.targetPortEdit.text()}</h4>")
        self.outputText.append(f"<h4><b>Timer:</b> {self.timerBox.value()}</h4>")
        self.outputText.append(f"<h4><b>Scanning starts at {datetime.datetime.now()}</b></h4> \n")

        headers = ["Port\t", "Status\t", "Service\t", "Version\t"]
        results = scanner.PortScanner(self.targetEdit.text(), self.targetPortEdit.text())
        self.cursor = QTextCursor()
        self.cursor = self.outputText.textCursor()
        self.cursor.insertTable(len(results)+1, len(headers))

        for header in headers:
            self.cursor.insertText(header)
            self.cursor.movePosition(QTextCursor.NextCell)

        for i in range(len(results)):
            self.cursor.insertText(str(results[i][0]))
            self.cursor.movePosition(QTextCursor.NextCell)
            self.cursor.insertText(results[i][1])
            self.cursor.movePosition(QTextCursor.NextCell)
            self.cursor.insertText(results[i][2])
            self.cursor.movePosition(QTextCursor.NextCell)
            self.cursor.movePosition(QTextCursor.NextCell)