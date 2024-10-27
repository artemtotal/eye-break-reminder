# run.py

import sys
from PyQt5.QtWidgets import QApplication
from eye_break_reminder import EyeBreakReminder


def main():
    app = QApplication(sys.argv)
    reminder = EyeBreakReminder()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
