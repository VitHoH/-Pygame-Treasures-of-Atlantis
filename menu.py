import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt6.QtGui import QFont, QFontDatabase
import pygame
from game import Game
import os
import sqlite3




class Menu(QMainWindow):
    def __init__(self):
        pygame.init()
        self.levels_music = pygame.mixer.Sound('levels_window.mp3')
        self.levels_music.play(-1)
        super().__init__()
        self.initUI()
        if not os.path.isfile('data/records.sqlite'):
            con = sqlite3.connect("data/records.sqlite")

            # Создание курсора
            cur = con.cursor()
            cur.execute("""CREATE TABLE records (
    one   INTEGER,
    two   INTEGER,
    three INTEGER,
    four  INTEGER,
    five  INTEGER
);""")
            cur.execute("""INSERT INTO records (one, two, three, four, five)
    VALUES (999999999999, 999999999999, 99999999999999999999999, 99999999999999999999, 9999999999999999999)""")
            con.commit()
            con.close()
        QFontDatabase.addApplicationFont('supermario286rusbylyajka.otf')
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.button1 = QPushButton('lEVEL 1', self)
        self.button1.resize(200, 50)
        self.button1.move(150, 200)
        self.button1.setFont(QFont('Super Mario 286(RUS BY LYAJKA)', 20))
        self.button1.setStyleSheet("background-color: rgb(255, 255, 102)")
        self.button3 = QPushButton('lEVEL 2', self)
        self.button3.resize(200, 50)
        self.button3.move(150, 260)
        self.button3.setFont(QFont('Super Mario 286(RUS BY LYAJKA)', 20))
        self.button3.setStyleSheet("background-color: rgb(255, 255, 102)")
        self.button2 = QPushButton('lEVEL 3', self)
        self.button2.resize(200, 50)
        self.button2.move(150, 320)
        self.button2.setStyleSheet("background-color: rgb(255, 255, 102)")
        self.button2.setFont(QFont('Super Mario 286(RUS BY LYAJKA)', 20))
        self.button4 = QPushButton('lEVEL 4', self)
        self.button4.resize(200, 50)
        self.button4.move(150, 380)
        self.button4.setFont(QFont('Super Mario 286(RUS BY LYAJKA)', 20))
        self.button4.setStyleSheet("background-color: rgb(255, 255, 102)")
        self.button5 = QPushButton('lEVEL 5', self)
        self.button5.resize(200, 50)
        self.button5.move(150, 440)
        self.button5.setFont(QFont('Super Mario 286(RUS BY LYAJKA)', 20))
        self.button5.setStyleSheet("background-color: rgb(255, 255, 102)")
        self.title = QLabel('УРОВНИ', self)
        self.title.resize(600, 90)
        self.title.move(130, 80)
        self.title.setFont(QFont('Super Mario 286(RUS BY LYAJKA)', 60))
        self.title.setStyleSheet("color: rgb(243, 98, 35)")
        self.button1.clicked.connect(lambda: self.start_game(0))
        self.button2.clicked.connect(lambda: self.start_game(1))
        self.button3.clicked.connect(lambda: self.start_game(2))
        self.button4.clicked.connect(lambda: self.start_game(3))
        self.button5.clicked.connect(lambda: self.start_game(4))
    def initUI(self):
        self.setGeometry(500, 200, 900, 600)
        self.setWindowTitle('Главное меню')


    def start_game(self, number_level):
        self.hide()
        self.levels_music.stop()
        pygame.init()
        game = Game(number_level)
        game.start_screen()
        game.run()
        pygame.quit()
        self.show()