# eye_break_reminder/main.py

import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QSlider,
    QSystemTrayIcon, QMenu, QAction, QPushButton, QLineEdit,
    QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import QTimer, Qt, QSettings, QTranslator, QLocale, QEvent
from PyQt5.QtGui import QIcon
import threading
import pygame

def resource_path(relative_path):
    # Получает абсолютный путь к ресурсам, работает для dev и для PyInstaller 
    if getattr(sys, '_MEIPASS', False):
            # Если запущено из PyInstaller
        base_path = sys._MEIPASS
    else:
            # Если запущено в режиме разработки
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class EyeBreakReminder(QWidget):
    def __init__(self):
        super().__init__()

        # Define path to log file in AppData
        app_data_dir = os.getenv('APPDATA')
        log_dir = os.path.join(app_data_dir, 'EyeBreakReminder')
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, 'eye_break_reminder.log')

        # Initialize logging
        try:
            logging.basicConfig(filename=log_file_path, level=logging.INFO,
                format='%(asctime)s:%(levelname)s:%(message)s')
        except Exception as e:
            print(f"Failed to initialize logging: {e}")
            logging.basicConfig(level=logging.INFO,
                format='%(asctime)s:%(levelname)s:%(message)s')

        logging.info("Application is starting.")

        # Use QSettings to save user preferences
        self.settings = QSettings('MyCompany', 'EyeBreakReminder')

        # Set up translator for multilingual support
        
        self.translator = QTranslator()
        locale = QLocale.system().name()
        print(f"System locale: {locale}")
        translations_path = resource_path('translations')
        translation_loaded = self.translator.load(f'app_{locale}', translations_path)
        if translation_loaded:
            QApplication.instance().installTranslator(self.translator)
            logging.info(f"Loaded translation for locale '{locale}'")
        else:
            logging.warning(f"Could not load translation for locale '{locale}' from '{translations_path}'")



        # Define base directory
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        
        # Paths to assets
        self.sound_path = resource_path('assets/sound.mp3')
        self.sound_path_end = resource_path('assets/sound_end.mp3')
        self.icon_path = resource_path('assets/icon.png')



        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr('Eye Reminder'))
        self.setGeometry(100, 100, 400, 400)  # Increased window size

        # Set window icon (to display in taskbar)
        self.setWindowIcon(QIcon(self.icon_path))

        layout = QVBoxLayout()

        # Countdown timer label
        self.timer_label = QLabel('20:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet('font-size: 36px;')
        layout.addWidget(self.timer_label)

        # Time settings layout
        time_settings_layout = QHBoxLayout()

        # Label and input for work interval
        work_interval_label = QLabel(self.tr('Reminder every X minutes:'), self)
        time_settings_layout.addWidget(work_interval_label)

        self.work_interval_input = QLineEdit(self)
        self.work_interval_input.setFixedWidth(50)
        self.work_interval_input.setText(self.settings.value('work_interval', '20'))
        time_settings_layout.addWidget(self.work_interval_input)

        layout.addLayout(time_settings_layout)

        # Label and input for break duration
        break_duration_layout = QHBoxLayout()

        break_duration_label = QLabel(self.tr('Reminder duration (sec):'), self)
        break_duration_layout.addWidget(break_duration_label)

        self.break_duration_input = QLineEdit(self)
        self.break_duration_input.setFixedWidth(50)
        self.break_duration_input.setText(self.settings.value('break_duration', '20'))
        break_duration_layout.addWidget(self.break_duration_input)

        layout.addLayout(break_duration_layout)

        # Volume label and slider
        self.volume_label = QLabel(self.tr('Volume: ') + self.settings.value('volume', '50'), self)
        layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.settings.value('volume', '50')))
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        layout.addWidget(self.volume_slider)

        # Checkbox for full-screen or windowed notification
        self.fullscreen_checkbox = QCheckBox(self.tr('Use full-screen notification'), self)
        self.fullscreen_checkbox.setChecked(self.settings.value('fullscreen', 'true') == 'true')
        layout.addWidget(self.fullscreen_checkbox)

        # Checkbox for minimize to tray
        self.minimize_to_tray_checkbox = QCheckBox(self.tr('Minimize to tray'), self)
        self.minimize_to_tray_checkbox.setChecked(self.settings.value('minimize_to_tray', 'true') == 'true')
        layout.addWidget(self.minimize_to_tray_checkbox)

        # Checkbox for autostart
        self.autostart_checkbox = QCheckBox(self.tr('Add to autostart'), self)
        self.autostart_checkbox.setChecked(self.settings.value('autostart', 'false') == 'true')
        layout.addWidget(self.autostart_checkbox)

        # Save settings button
        save_settings_button = QPushButton(self.tr('Save settings'), self)
        save_settings_button.clicked.connect(self.save_settings)
        layout.addWidget(save_settings_button)

        self.setLayout(layout)

        self.create_tray_icon()

        # Set remaining time
        self.set_remaining_time()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Timer updates every second

        # Apply CSS styles for better UI
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
            }
        """)

        self.show()

        # Set up autostart based on saved settings
        if self.autostart_checkbox.isChecked():
            self.setup_autostart()
        else:
            self.remove_autostart()

    def tr(self, text):
        # Method for translating text
        return QApplication.translate("EyeBreakReminder", text)

    def set_remaining_time(self):
        try:
            self.remaining_time = int(float(self.work_interval_input.text()) * 60)
            self.update_timer_label()
        except ValueError:
            self.remaining_time = 20 * 60  # Default to 20 minutes
            self.work_interval_input.setText('20')

    def update_volume_label(self, value):
        self.volume_label.setText(self.tr('Volume: ') + str(value))

    def save_settings(self):
        # Save user settings
        self.settings.setValue('volume', str(self.volume_slider.value()))
        self.settings.setValue('work_interval', self.work_interval_input.text())
        self.settings.setValue('break_duration', self.break_duration_input.text())
        self.settings.setValue('fullscreen', 'true' if self.fullscreen_checkbox.isChecked() else 'false')
        self.settings.setValue('autostart', 'true' if self.autostart_checkbox.isChecked() else 'false')
        self.settings.setValue('minimize_to_tray', 'true' if self.minimize_to_tray_checkbox.isChecked() else 'false')
        self.set_remaining_time()
        logging.info("Settings saved.")

        # Set up or remove autostart based on checkbox
        if self.autostart_checkbox.isChecked():
            self.setup_autostart()
        else:
            self.remove_autostart()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1

            # Notification 10 seconds before break
            if self.remaining_time == 10:
                self.tray_icon.showMessage(
                    self.tr('Break is about to start'),
                    self.tr('Your break will start in 10 seconds.'),
                    QSystemTrayIcon.Information,
                    5000
                )
                logging.info("User notified of upcoming break.")

            self.update_timer_label()
        else:
            self.timer.stop()
            self.show_break_message()

    def update_timer_label(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f'{int(minutes):02d}:{int(seconds):02d}')

    def show_break_message(self):
        volume = self.volume_slider.value()
        threading.Thread(target=self.play_sound, args=(volume,)).start()

        # Choose between full-screen or windowed notification
        if self.fullscreen_checkbox.isChecked():
            self.break_window = QWidget()
            self.break_window.showFullScreen()
        else:
            self.break_window = QWidget()
            self.break_window.setWindowTitle(self.tr('Break Time'))
            self.break_window.setGeometry(100, 100, 400, 200)
            self.break_window.show()

        layout = QVBoxLayout()

        label = QLabel(self.tr("Time to take a break!"), self.break_window)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 24px;')
        layout.addWidget(label)

        close_button = QPushButton(self.tr("Close"), self.break_window)
        close_button.clicked.connect(self.end_break)
        layout.addWidget(close_button)

        self.break_window.setLayout(layout)

        # Use customizable break duration
        try:
            break_duration = int(float(self.break_duration_input.text()) * 1000)
        except ValueError:
            break_duration = 20 * 1000  # Default to 20 seconds
            self.break_duration_input.setText('20')

        
        QTimer.singleShot(break_duration, self.end_break)  # Close after specified time

    def end_break(self):
        # Close break window

        volume = self.volume_slider.value()
        threading.Thread(target=self.play_sound_end, args=(volume,)).start()

        if hasattr(self, 'break_window'):
            self.break_window.close()
            logging.info("Break ended.")

        # Reset timer and start again
        self.set_remaining_time()
        self.timer.start(1000)

    def play_sound(self, volume):
        try:
            # Play notification sound
            pygame.mixer.init()
            pygame.mixer.music.set_volume(volume / 100)
            pygame.mixer.music.load(self.sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            logging.error(f"Error playing sound: {e}")

    def play_sound_end(self, volume):
        try:
            # Play notification sound
            pygame.mixer.init()
            pygame.mixer.music.set_volume(volume / 100)
            pygame.mixer.music.load(self.sound_path_end)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            logging.error(f"Error playing sound: {e}")



    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon(self.icon_path), self)

        tray_menu = QMenu()
        restore_action = QAction(self.tr('Restore'), self)
        restore_action.triggered.connect(self.showNormal)
        restore_action.setIcon(QIcon(self.icon_path))
        tray_menu.addAction(restore_action)

        quit_action = QAction(self.tr('Exit'), self)
        quit_action.triggered.connect(QApplication.instance().quit)
        quit_action.setIcon(QIcon(self.icon_path))
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


    def closeEvent(self, event):
        # Always close the application when the window is closed
        logging.info("Application is closing.")
        self.tray_icon.hide()
        event.accept()

    def changeEvent(self, event):
        logging.info(f"Event type: {event.type()}")
        # Handle minimize to tray if the checkbox is checked
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                if self.minimize_to_tray_checkbox.isChecked():
                    QTimer.singleShot(0, self.hide)
                    self.tray_icon.showMessage(
                        self.tr('Eye Reminder'),
                        self.tr('Application minimized to tray.'),
                        QSystemTrayIcon.Information,
                        2000
                    )
                    logging.info("Application minimized to tray.")
        super(EyeBreakReminder, self).changeEvent(event)

    def setup_autostart(self):
        # Add application to autostart (Windows)
        if sys.platform.startswith('win'):
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Run",
                                     0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, 'EyeBreakReminder', 0, winreg.REG_SZ, f'"{sys.executable}"')
                key.Close()
                logging.info("Application added to autostart.")
            except Exception as e:
                logging.error(f"Error adding to autostart: {e}")

    def remove_autostart(self):
        # Remove application from autostart (Windows)
        if sys.platform.startswith('win'):
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Run",
                                     0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key, 'EyeBreakReminder')
                key.Close()
                logging.info("Application removed from autostart.")
            except FileNotFoundError:
                logging.info("Application was not in autostart.")
            except Exception as e:
                logging.error(f"Error removing from autostart: {e}")

def main():
    app = QApplication(sys.argv)
    reminder = EyeBreakReminder()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
