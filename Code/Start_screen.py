import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame, QLabel, QSlider, QHBoxLayout, QStackedLayout
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QSize
from PIL import Image, ImageQt
import pygame
import subprocess

pygame.mixer.init()

class ButtonComponent(QPushButton):
    def __init__(self, text, command, color, file_to_open, hover_sound):
        super().__init__(text)
        self.color = color
        self.file_to_open = file_to_open
        self.clicked.connect(lambda: command(self.file_to_open))
        self.hover_sound = pygame.mixer.Sound(hover_sound)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color[0]}; 
                color: white; 
                font: bold 36px Arial; 
                height: 100px; 
                width: 400px;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {color[1]};
            }}
        """)
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        self.hover_sound.play()
        super().enterEvent(event)

class GearButtonComponent(QPushButton):
    def __init__(self, command):
        super().__init__()
        self.command = command

        gear_icon = QIcon("Pics/settings.png")
        self.setIcon(gear_icon)
        self.setIconSize(QSize(40, 40))

        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.5);
            }
        """)
        self.setFlat(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.command()
        super().mousePressEvent(event)

class SettingsPopup(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.5);
            border: 5px solid #ccc;
            border-radius: 20px;
            padding: 20px;
            position: relative;
        """)
        self.setGeometry(0, 0, 600, 400)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        #X
        top_layout = QHBoxLayout()
        close_button = QPushButton("X", self)
        close_button.setStyleSheet("""
            QPushButton {
                font: bold 20px Arial;
                color: white;
                background-color: transparent;
                border: none;
                border-radius: 15px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgb(255, 0, 0);
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgb(230, 0, 0);
            }
        """)
        close_button.clicked.connect(self.hide)
        top_layout.addWidget(close_button, alignment=Qt.AlignRight)
        layout.addLayout(top_layout)

        #Background
        background_layout = QHBoxLayout()
        background_label = QLabel("Background", self)
        background_label.setFont(QFont("Arial", 12, QFont.Bold))
        background_layout.addWidget(background_label)
        
        self.background_slider = QSlider(Qt.Horizontal, self)
        self.background_slider.setRange(0, 100)
        self.background_slider.setValue(50)
        self.background_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #555555;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: transparent;
                width: 32px;
                height: 32px;
                border-radius: 16px;
                background-image: url('planet.jpg');
                background-position: center;
                background-repeat: no-repeat;
            }
        """)
        background_label.setStyleSheet("""
            color: white;
            margin-right: 10px;
            min-width: 150px;
        """)
        background_label.setAlignment(Qt.AlignCenter)
        background_layout.addWidget(self.background_slider)
        layout.addLayout(background_layout)

        #Button sound
        button_sound_layout = QHBoxLayout()
        button_sound_label = QLabel("Button Sound", self)
        button_sound_label.setFont(QFont("Arial", 12, QFont.Bold))
        button_sound_layout.addWidget(button_sound_label)
        
        self.button_sound_slider = QSlider(Qt.Horizontal, self)
        self.button_sound_slider.setRange(0, 100)
        self.button_sound_slider.setValue(50)
        self.button_sound_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #555555;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: transparent;
                width: 32px;
                height: 32px;
                border-radius: 16px;
                background-image: url('planet.jpg');
                background-position: center;
                background-repeat: no-repeat;
            }
        """)
        button_sound_label.setStyleSheet("""
            color: white;
            margin-right: 10px;
            min-width: 150px;
        """)
        button_sound_label.setAlignment(Qt.AlignCenter)
        button_sound_layout.addWidget(self.button_sound_slider)
        layout.addLayout(button_sound_layout)

        #Exit
        exit_button = QPushButton("Exit", self)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font: bold 16px Arial;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b; 
            }
        """)
        exit_button.clicked.connect(self.parent().close)
        layout.addWidget(exit_button, alignment=Qt.AlignCenter)

    def set_background_volume(self, callback):
        self.background_slider.valueChanged.connect(callback)

    def set_button_volume(self, callback):
        self.button_sound_slider.valueChanged.connect(callback)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game")
        self.setWindowIcon(QIcon("Pics/icon.png"))
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")

        pygame.mixer.music.load("Sound/background.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)

        # Initialize background
        self.init_background()
        self.init_ui()

    def init_background(self):
        self.background_image = Image.open("Pics/1.1.png").resize((1920, 1080)).convert('RGB')
        background_image_qt = QImage(self.background_image.tobytes(), self.background_image.width, self.background_image.height, self.background_image.width * 3, QImage.Format_RGB888)
        self.background_photo = QPixmap.fromImage(background_image_qt)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_photo)
        self.background_label.setGeometry(0, 0, 1920, 1080)

    def init_ui(self):
        colors = [('tomato', 'darkred'), ('mediumseagreen', 'darkgreen'), ('khaki', 'goldenrod'), ('skyblue', 'dodgerblue')]

        self.layout = QVBoxLayout()

        self.btn1 = ButtonComponent("PLAY!", self.on_button_click, colors[0], 'Code/Create.py', 'Sound/Button_sound.mp3')
        self.layout.addWidget(self.btn1)
        self.btn2 = ButtonComponent("CHARACTERS", self.on_button_click, colors[1], 'Char.py', 'Sound/Button_sound.mp3')
        self.layout.addWidget(self.btn2)
        self.btn3 = ButtonComponent("SHOP", self.on_button_click, colors[2], 'Shop.py', 'Sound/Button_sound.mp3')
        self.layout.addWidget(self.btn3)
        self.btn4 = ButtonComponent("HOW TO PLAY", self.on_button_click, colors[3], 'H2p.py', 'Sound/Button_sound.mp3')
        self.layout.addWidget(self.btn4)

        # Settings
        self.gear_button = GearButtonComponent(self.toggle_popup)
        self.layout.addWidget(self.gear_button)
        self.gear_button.setGeometry(1800, 50, 55, 55)

        # Settings popup
        self.popup = SettingsPopup(self)
        self.popup.set_background_volume(self.update_background_music_volume)
        self.popup.set_button_volume(self.update_button_volume)
        self.center_popup()
        self.popup.hide()

        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def center_popup(self):
        window_width = self.width()
        window_height = self.height()
        popup_width = self.popup.width()
        popup_height = self.popup.height()
        popup_x = (window_width - popup_width) // 2
        popup_y = (window_height - popup_height) // 2
        self.popup.move(popup_x, popup_y)

    def toggle_popup(self):
        self.popup.setVisible(not self.popup.isVisible())
        self.popup.raise_()

    def on_button_click(self, file_to_open):
        if file_to_open:
            subprocess.Popen(['python', file_to_open])
            self.close()

    def update_background_music_volume(self):
        volume = self.popup.background_slider.value() / 100
        pygame.mixer.music.set_volume(volume)

    def update_button_volume(self):
        volume = self.popup.button_sound_slider.value() / 100
        for button in [self.btn1, self.btn2, self.btn3, self.btn4]:
            button.hover_sound.set_volume(volume)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = App()
    main_app.show()
    sys.exit(app.exec_())