from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import subprocess
from PyQt5.QtCore import pyqtSignal, QObject

class ButtonActions:
    def __init__(self, parent):
        self.parent = parent

    def create_room(self):
        self.parent.go_to_room_screen()

    def go_back(self):
        self.parent.go_to_create_screen()

    def go_to_create_screen(self):
        subprocess.Popen(["python", "Code/Create.py"])
        self.parent.close()

    def go_to_room_screen(self):
        subprocess.Popen(["python", "Code/Waiting_room.py"])
        self.parent.close()

class PlayerSlots:
    def __init__(self, parent, layout):
        self.parent = parent
        self.layout = layout

    def update_slots(self, count):
        #Xóa tất cả các ô cũ
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        #Thêm các ô người chơi mới
        for i in range(count):
            label = QLabel(f"Player {i + 1}")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                background: rgba(255, 255, 255, 0.3);
                border: 2px solid #4CAF50;
                font-size: 16px;
                color: black;
                padding: 10px;
            """)
            self.layout.addWidget(label, i // 2, i % 2)

        with open("../player_count.txt", "w") as file:
            file.write(str(count))

class MapSelection:
    def __init__(self, parent, layout):
        self.parent = parent
        self.layout = layout
        self.create_buttons()

    def create_buttons(self):
        maps = ["Map 1", "Map 2", "Map 3"]
        self.buttons = []

        for i, map_name in enumerate(maps):
            button = QPushButton(map_name)
            button.setStyleSheet("""
                font-size: 14px; 
                background-color: #008CBA; 
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            """)

            button.setStyleSheet("""
                QPushButton:hover {
                    background-color: #005f73; 
                }
                QPushButton:pressed {
                    background-color: #003d4d; 
                }
                QPushButton:checked {
                    background-color: #007f7f;
                }
            """)

            button.setCheckable(True)
            button.clicked.connect(self.create_map_click_handler(i))

            self.layout.addWidget(button)
            self.buttons.append(button)

        self.buttons[0].setChecked(True)
        self.parent.change_map(0)
    
    def create_map_click_handler(self, map_num):
        def handler():
            self.select_map(map_num)
        return handler

    def select_map(self, map_num):
        for button in self.buttons:
            button.setChecked(False)

        self.buttons[map_num].setChecked(True)

        self.parent.change_map(map_num)

class PasswordEntry:
    def __init__(self, parent, layout):
        self.parent = parent
        self.layout = layout
        self.create_entry()

    def create_entry(self):
        label = QLabel("Password (optional):")
        label.setStyleSheet("font-size: 16px; color: white;")
        self.layout.addWidget(label)

        self.password_entry = QLineEdit()
        self.password_entry.setStyleSheet("""
            font-size: 14px; 
            padding: 10px; 
            border: 2px solid #4CAF50; 
            border-radius: 5px;
        """)
        self.layout.addWidget(self.password_entry)

class PlayerCountSelection:
    def __init__(self, parent, layout, update_slots_callback):
        self.parent = parent
        self.layout = layout
        self.update_slots_callback = update_slots_callback
        self.create_buttons()

    def create_buttons(self):
        label = QLabel("Select Player Count:")
        label.setStyleSheet("font-size: 16px; color: white;")
        self.layout.addWidget(label)
        self.buttons = []

        for i in range(1, 5):
            button = QPushButton(str(i))
            button.setStyleSheet("""
                font-size: 14px; 
                background-color: #008CBA; 
                color: white; 
                border-radius: 5px; 
                padding: 10px;
            """)

            button.setStyleSheet("""
                QPushButton:hover {
                    background-color: #005f73; 
                }
                QPushButton:pressed {
                    background-color: #003d4d; 
                }
                QPushButton:checked {
                    background-color: #007f7f;
                }
            """)

            button.setCheckable(True)
            button.clicked.connect(self.create_player_count_click_handler(i))

            self.layout.addWidget(button)
            self.buttons.append(button)

        self.buttons[0].setChecked(True)

    def create_player_count_click_handler(self, count):
        def handler():
            self.select_player_count(count)
        return handler

    def select_player_count(self, count):
        for button in self.buttons:
            button.setChecked(False)

        self.buttons[count - 1].setChecked(True)

        self.update_slots_callback(count)

class CreateRoom(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Room")
        self.showFullScreen()

        self.button_actions = ButtonActions(self)

        main_layout = QVBoxLayout(self)

        #Players
        self.player_layout = QGridLayout()
        player_slots = PlayerSlots(self, self.player_layout)
        player_slots.update_slots(1)  #Mặc định chọn 1 player
        main_layout.addLayout(self.player_layout)

        #Maps
        map_layout = QHBoxLayout()
        MapSelection(self, map_layout)
        main_layout.addLayout(map_layout)

        #Password
        password_layout = QHBoxLayout()
        PasswordEntry(self, password_layout)
        main_layout.addLayout(password_layout)

        #Cnt_Players
        player_count_layout = QHBoxLayout()
        PlayerCountSelection(self, player_count_layout, player_slots.update_slots)
        main_layout.addLayout(player_count_layout)

        # Buttons
        button_layout = QHBoxLayout()
        back_button = QPushButton("Cancel")
        back_button.setStyleSheet("""
            font-size: 16px; 
            background-color: red; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        back_button.clicked.connect(self.button_actions.go_back)
        button_layout.addWidget(back_button)

        create_button = QPushButton("Create")
        create_button.setStyleSheet("""
            font-size: 16px; 
            background-color: green; 
            color: white; 
            padding: 10px; 
            border-radius: 5px;
        """)
        create_button.clicked.connect(self.button_actions.create_room)
        button_layout.addWidget(create_button)

        main_layout.addLayout(button_layout)


    def change_map(self, map_index):
        map_images = ["Pics/5.1.jpeg", "Pics/5.2.jpg", "Pics/5.3.jpg"]
        selected_map_image = map_images[map_index]

        pixmap = QPixmap(selected_map_image)
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(p)

    def go_to_room_screen(self):
        subprocess.Popen(["python", "Code/Waiting_room.py"])
        self.parent.close()
    
    def go_to_create_screen(self):
        subprocess.Popen(["python", "Code/Create.py"])
        self.parent.close()

if __name__ == "__main__":
    app = QApplication([])
    window = CreateRoom()
    window.show()
    app.exec_()