from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QScrollArea, QSlider
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import subprocess

class ButtonActions:
    def __init__(self, parent):
        self.parent = parent

    def play_game(self):
        subprocess.Popen(["python", "Code/Game.py"]) 
        self.parent.close()

    def open_settings(self):
        self.parent.open_settings_dialog()

    def exit_room(self):
        subprocess.Popen(["python", "Code/Create.py"])
        self.parent.close()

class PlayerDisplay:
    def __init__(self, parent, layout):
        self.parent = parent
        self.layout = layout
        self.player_labels = []

    def update_display(self, player_count):
        try:
            with open("../player_count.txt", "r") as file:
                player_count = int(file.read().strip())
        except FileNotFoundError:
            print("Không tìm thấy file player_count.txt. Hãy chọn số lượng người chơi trước.")
            return
        except ValueError:
            print("File player_count.txt chứa dữ liệu không hợp lệ.")
            return
            
        for label in self.player_labels:
            self.layout.removeWidget(label)
            label.deleteLater()

        self.player_labels.clear()

        for i in range(player_count):
            label = QLabel(f"Player {i + 1}")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                background: rgba(255, 255, 255, 0.3);
                border: 2px solid #4CAF50;
                font-size: 16px;
                color: black;
                padding: 10px;
                margin: 5px;
            """)
            self.layout.addWidget(label)
            self.player_labels.append(label)

class ChatDisplay:
    def __init__(self, parent, layout):
        self.parent = parent
        self.layout = layout
        self.create_chat_box()

    def create_chat_box(self):
        self.chat_area = QScrollArea()
        self.chat_area.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.chat_area.setFixedHeight(150)

        self.chat_widget = QLabel("")
        self.chat_widget.setStyleSheet("font-size: 14px; padding: 5px;")
        self.chat_widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.chat_area.setWidget(self.chat_widget)
        self.chat_area.setWidgetResizable(True)
        self.layout.addWidget(self.chat_area)

        self.message_entry = QLineEdit()
        self.message_entry.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)
        self.message_entry.setFixedHeight(30)
        self.layout.addWidget(self.message_entry)

        self.message_entry.returnPressed.connect(self.send_message)

    def send_message(self):
        message = self.message_entry.text().strip()
        if message:
            current_text = self.chat_widget.text()
            new_text = current_text + ("" if not current_text else "\n") + message
            self.chat_widget.setText(new_text)
            self.message_entry.clear()

class SettingsPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 0.95); 
            border-radius: 15px; 
            padding: 20px;
            border: 2px solid #4CAF50;
        """)
        self.setFixedSize(600, 400)
        self.setLayout(self.create_settings_layout())

    def create_settings_layout(self):
        layout = QVBoxLayout()

        # Tiêu đề Settings
        title_label = QLabel("Settings")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 20px;
            text-align: center;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Volume Slider
        volume_label = QLabel("Volume:")
        volume_label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(volume_label)

        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        layout.addWidget(volume_slider)

        # Exit Button
        exit_button = QPushButton("Exit Room")
        exit_button.setStyleSheet("""
            font-size: 16px; 
            background-color: red; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        exit_button.clicked.connect(self.parent.button_actions.exit_room)
        layout.addWidget(exit_button)

        # Close Button
        close_button = QPushButton("X")
        close_button.setStyleSheet("""
            font-size: 16px; 
            background-color: gray; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        close_button.clicked.connect(self.close_panel)
        layout.addWidget(close_button)

        return layout

    def close_panel(self):
        self.parent.toggle_settings_panel(False)

class WaitingRoom(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waiting Room")
        self.showFullScreen()

        self.button_actions = ButtonActions(self)

        self.set_background_image("Pics/6.1.jpeg")

        # Main Layout
        self.main_layout = QVBoxLayout(self)

        # Player Display
        self.player_layout = QVBoxLayout()
        self.player_display = PlayerDisplay(self, self.player_layout)
        self.player_display.update_display(1)
        self.main_layout.addLayout(self.player_layout)

        # Chat Display
        chat_layout = QVBoxLayout()
        ChatDisplay(self, chat_layout)
        self.main_layout.addLayout(chat_layout)

        # Buttons
        button_layout = QHBoxLayout()

        settings_button = QPushButton("Settings")
        settings_button.setStyleSheet("""
            font-size: 16px; 
            background-color: #4CAF50; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        settings_button.clicked.connect(lambda: self.toggle_settings_panel(True))
        button_layout.addWidget(settings_button)

        play_button = QPushButton("Play")
        play_button.setStyleSheet("""
            font-size: 16px; 
            background-color: blue; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        play_button.clicked.connect(self.button_actions.play_game)
        button_layout.addWidget(play_button)

        self.main_layout.addLayout(button_layout)

        # Settings Panel (Initially Hidden)
        self.settings_panel = SettingsPanel(self)
        self.settings_panel.setParent(self)
        self.settings_panel.hide()

        self.setLayout(self.main_layout)

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Error: Image not found or unable to load.")
        else:
            pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)

    def toggle_settings_panel(self, show):
        if show:
            # Đặt bảng SettingsPanel ở chính giữa màn hình
            self.settings_panel.setGeometry(
                (self.width() - self.settings_panel.width()) // 2,
                (self.height() - self.settings_panel.height()) // 2,
                self.settings_panel.width(),
                self.settings_panel.height()
            )
            self.settings_panel.show()
        else:
            self.settings_panel.hide()

if __name__ == "__main__":
    app = QApplication([])
    window = WaitingRoom()
    window.show()
    app.exec_()