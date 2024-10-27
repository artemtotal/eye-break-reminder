# eye_break_reminder/main.py

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QSlider,
    QSystemTrayIcon, QMenu, QAction, QPushButton
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
import threading
import pygame


class EyeBreakReminder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Reminder for Eyes')
        self.setGeometry(100, 100, 300, 200)  # Window position and size

        layout = QVBoxLayout()

        self.timer_label = QLabel('20:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet('font-size: 36px;')
        layout.addWidget(self.timer_label)

        self.volume_label = QLabel('Volume: 50', self)
        layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        layout.addWidget(self.volume_slider)

        self.setLayout(layout)

        self.remaining_time = 20 * 60  # 20 minutes in seconds

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Timer updates every second

        # Define the base directory
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Paths to assets
        self.sound_path = os.path.join(BASE_DIR, '..', 'assets', 'sound.mp3')
        self.icon_path = os.path.join(BASE_DIR, '..', 'assets', 'icon.png')

        self.create_tray_icon()

        self.show()
    
    def update_volume_label(self, value):
        self.volume_label.setText(f'Volume: {value}')


    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.setText(f'{int(minutes):02d}:{int(seconds):02d}')
        else:
            self.remaining_time = 20 * 60
            self.show_break_message()

    def show_break_message(self):
        volume = self.volume_slider.value()
        threading.Thread(target=self.play_sound, args=(volume,)).start()

        self.break_window = QWidget()
        self.break_window.showFullScreen()

        layout = QVBoxLayout()

        label = QLabel("It's time to look 6 meters into the distance for 20 seconds", self.break_window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 48px;')
        layout.addWidget(label)

        close_button = QPushButton("Close", self.break_window)
        close_button.clicked.connect(self.break_window.close)
        layout.addWidget(close_button)

        self.break_window.setLayout(layout)

        QTimer.singleShot(20000, self.break_window.close)  # Close after 20 seconds

    def play_sound(self, volume):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume / 100)
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def create_tray_icon(self):
        
        if getattr(sys, 'frozen', False): 
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        
        icon_path = os.path.join(base_path, 'assets', 'icon.png')
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)

        # self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_path))

        tray_menu = QMenu()
        restore_action = QAction('Restore', self)
        restore_action.triggered.connect(self.showNormal)
        tray_menu.addAction(restore_action)

        quit_action = QAction('Exit', self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            'Reminder for Eyes',
            'Application minimized to tray.',
            QSystemTrayIcon.Information,
            2000
        )


def main():
    app = QApplication(sys.argv)
    reminder = EyeBreakReminder()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
