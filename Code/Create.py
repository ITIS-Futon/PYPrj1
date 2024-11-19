import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame, QLabel, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from PIL import Image
import subprocess

class Name(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter your name")
        self.setFixedHeight(60)
        self.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                border-radius: 20px;
                border: 2px solid #ccc;
                background-color: #f0f0f0;
            }
            QLineEdit:hover {
                border-color: #4CAF50;
                background-color: #e8f5e9;
            }
        """)

class BackBut(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Back", parent)
        self.setFixedSize(120, 50)
        self.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 16px;
                color: white;
                background-color: #333;
                border-radius: 8px;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.clicked.connect(self.go_to_start_screen)
        
    def go_to_start_screen(self):
        subprocess.Popen(["python", "Code/Start_screen.py"])
        self.parent().close()

class Host(QWidget):
    def __init__(self):
        super().__init__()

        # Label chứa avatar và text
        self.host_label = QLabel(self)
        self.host_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        """)
        self.host_label.setFixedSize(400, 200)

        full_layout = QHBoxLayout()

        # Avatar của Host
        self.avatar = QLabel(self.host_label)
        avatar_pixmap = QPixmap("Pics/2.2.png").scaled(180, 200, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.avatar.setPixmap(avatar_pixmap)
        self.avatar.setAlignment(Qt.AlignCenter)
        
        half_layout = QVBoxLayout()

        # Label "Host"
        self.host_text = QLabel("Host", self.host_label)
        self.host_text.setStyleSheet("""
            font-size: 24px;
            color: white;
        """)
        self.host_text.setAlignment(Qt.AlignCenter)
        half_layout.addWidget(self.host_text, alignment = Qt.AlignTop)

        # Nút Create Room
        self.create_room_button = QPushButton("Create Room", self.host_label)
        self.create_room_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        self.create_room_button.clicked.connect(self.go_to_create_room)
        half_layout.addWidget(self.create_room_button, alignment = Qt.AlignBottom)

        half_widget = QWidget()
        half_widget.setLayout(half_layout)

        full_layout.addWidget(self.avatar)
        full_layout.addWidget(half_widget)
        self.host_label.setLayout(full_layout)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.host_label)

    def go_to_create_room(self):
        subprocess.Popen(["python", "Code/Create_tab.py"])
        self.close()

class Join(QWidget):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.join_label = QLabel(self)
        self.join_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        """)
        self.join_label.setFixedSize(400, 200)

        full_layout = QHBoxLayout()

        # Avatar của Join
        self.avatar = QLabel(self.join_label)
        avatar_pixmap = QPixmap("Pics/2.3.png").scaled(180, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar.setPixmap(avatar_pixmap)
        self.avatar.setAlignment(Qt.AlignCenter)

        half_layout = QVBoxLayout()

        # Label "Join"
        self.join_text = QLabel("Join", self.join_label)
        self.join_text.setStyleSheet("""
            font-size: 24px;
            color: white;
        """)
        self.join_text.setAlignment(Qt.AlignCenter)
        half_layout.addWidget(self.join_text, alignment = Qt.AlignTop)

        # Nút Join Room
        self.join_room_button = QPushButton("Join Room", self.join_label)
        self.join_room_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        self.join_room_button.clicked.connect(self.show_join_dialog)
        half_layout.addWidget(self.join_room_button, alignment = Qt.AlignBottom)

        half_widget = QWidget()
        half_widget.setLayout(half_layout)

        full_layout.addWidget(self.avatar)
        full_layout.addWidget(half_widget)
        self.join_label.setLayout(full_layout)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.join_label)

    def show_join_dialog(self):
        self.join_dialog = QFrame(self)
        self.join_dialog.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border: 2px solid #333;
        """)

        layout = QVBoxLayout(self.join_dialog)
        header_layout = QHBoxLayout()

        #Tiêu đề
        header = QLabel("Join Room", self.join_dialog)
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: black;
            margin-right: auto;
        """)
        header_layout.addWidget(header)

        #X
        close_button = QPushButton("X", self.join_dialog)
        close_button.setStyleSheet("""
            QPushButton {
                font: bold 20px Arial;
                color: white;
                background-color: #000;
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
        close_button.clicked.connect(self.join_dialog.hide)
        header_layout.addWidget(close_button)
        layout.addLayout(header_layout)
        
        # Input mã phòng
        self.room_code_input = QLineEdit(self.join_dialog)
        self.room_code_input.setPlaceholderText("Enter room code")
        self.room_code_input.setStyleSheet("""
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        """)
        layout.addWidget(self.room_code_input)

        # Input mật khẩu
        self.password_input = QLineEdit(self.join_dialog)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        """)
        layout.addWidget(self.password_input)
        
        # Nút Join
        self.join_room_confirm_button = QPushButton("Join Room", self.join_dialog)
        self.join_room_confirm_button.setStyleSheet("""
            background-color: #FFA500;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            padding: 10px;
        """)
        self.join_room_confirm_button.clicked.connect(self.open_waiting_room)
        layout.addWidget(self.join_room_confirm_button, alignment = Qt.AlignCenter)
        
        self.join_dialog.resize(600, 400)

        self.join_dialog.setWindowModality(Qt.ApplicationModal)
        self.join_dialog.show()

    def open_waiting_room(self):
        from Waiting_room import WaitingRoom
        self.waiting_room = WaitingRoom()
        self.waiting_room.show()
        self.join_dialog.hide()

class CreateRoomApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game")
        self.setWindowIcon(QIcon("Pics/icon.png"))
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.init_background()
        self.add_black_frame()

    def init_background(self):
        self.background_image = QPixmap("Pics/1.1.png").scaled(1920, 1080, Qt.KeepAspectRatioByExpanding)
        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, 1920, 1080)

    def add_black_frame(self):
        # Xác định kích thước frame
        frame_width = int(1920 * 3 / 4)
        frame_height = int(1080 * 3 / 4)

        # Tạo QFrame cho phần nền
        self.frame = QFrame(self)
        self.frame.setGeometry((1920 - frame_width) // 2, (1080 - frame_height) // 2, frame_width, frame_height)
        self.frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.6); 
            border-radius: 10px;
            border: 3px solid white;
        """)

        #Layout
        layout = QVBoxLayout()

        #input tên
        self.name_input = Name(self.frame)
        layout.addWidget(self.name_input)

        #Host
        self.host_component = Host()
        layout.addWidget(self.host_component)
        
        #Join
        self.join_component = Join(self.frame)
        layout.addWidget(self.join_component)

        self.back_button = BackBut(self.frame)
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button, alignment = Qt.AlignLeft)
        layout.addLayout(back_layout)

        self.frame.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateRoomApp()
    window.show()
    sys.exit(app.exec_())