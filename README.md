# Eye Break Reminder

![Logo](./icon.png)

## Description

**Eye Break Reminder** is a convenient desktop application developed in Python using PyQt5. It helps you monitor your computer usage time and reminds you to take eye breaks every 20 minutes. During a break, the application plays a sound and displays a full-screen message encouraging you to look 6 meters into the distance for 20 seconds.

## Features

- **Timer**: Counts down 20 minutes of active work.
- **Break Reminders**: After the timer ends, a break mode is activated with a message and sound alert.
- **Volume Control**: Ability to adjust the notification volume.
- **System Tray**: The application minimizes to the system tray with options to quickly restore or exit.
- **Full-Screen Notification**: For maximum effectiveness of break reminders.

## Screenshots

![Main Window](path/to/screenshot_main.png)
*Main application window with timer and volume control.*

![Break Window](path/to/screenshot_break.png)
*Full-screen message prompting you to take a break.*

## Installation

### Prerequisites

- **Python 3.6+**
- **pip** — Python package manager

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/EyeBreakReminder.git
   cd EyeBreakReminder
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add necessary resources:**

   Ensure that the `sound.mp3` and `icon.png` files are present in the project directory.

## Usage

Run the application with the following command:

```bash
python main.py
```

Upon launch, a window with a timer and volume slider will appear. The timer will start counting down from 20 minutes. When the time is up, you will receive a notification to take a break.

### System Tray

- **Restore Window**: Right-click the application icon in the system tray and select "Restore".
- **Exit Application**: Choose "Exit" from the tray context menu.

## Dependencies

- [PyQt5](https://pypi.org/project/PyQt5/) — Library for creating graphical user interfaces.
- [pygame](https://pypi.org/project/pygame/) — Library for handling sound.

## Contribution

Welcome to the project! You can contribute in the following ways:

1. **Fork** the repository.
2. Create your own branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

## Contact

If you have any questions or suggestions, contact us via email: [your.email@example.com](mailto:your.email@example.com)

---

*Thank you for using Eye Break Reminder! Take care of your vision!*