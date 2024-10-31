# EyeBreakReminder

EyeBreakReminder is a simple Python application designed to help you take regular breaks to rest your eyes, reminding you to look away from the screen every set interval.

## Description

The application displays a countdown timer and, at specified intervals, shows a notification (either fullscreen or windowed) prompting you to take a break and look into the distance. It also plays customizable sound notifications at the start and end of each break. You can adjust the work interval, break duration, volume, and choose whether the application minimizes to the system tray or starts automatically with your system. Multilingual support is included via translation files.

## Features

- **Customizable work intervals and break durations**
- **Option for fullscreen or windowed notifications**
- **Adjustable volume for sound notifications**
- **Minimize to system tray**
- **Autostart with system boot**
- **Multilingual support (using translation files)**
- **Event logging for troubleshooting**

## Installation

### Requirements

- Python 3.x
- Python libraries:
  - PyQt5
  - pygame

### Installing Dependencies

Install the required libraries using pip:

```bash
pip install PyQt5 pygame
```

### Project Structure

```
EyeBreakReminder/
├── assets/
│   ├── icon.png
│   ├── icon.ico
│   ├── sound.mp3
│   └── sound_end.mp3
├── translations/
│   └── app_ru.qm
├── eye_break_reminder/
│   ├── __init__.py
│   ├── main.py
│   └── setup.py
└── README.md
```

- `assets/` — Folder containing icons and sound files
- `translations/` — Folder containing translation files
- `eye_break_reminder/` — Main application module
  - `__init__.py` — Initialization file for the package
  - `main.py` — Main executable file of the application
  - `setup.py` — Setup script for the application
- `README.md` — Project description

## Usage

### Running the Application

Run the application using the following command:

```bash
python main.py
```

### Settings

- **Reminder every X minutes**: Set the interval (in minutes) after which the reminder will appear.
- **Reminder duration (sec)**: Set how long (in seconds) the reminder will be displayed.
- **Volume**: Adjust the volume of the sound notifications.
- **Use full-screen notification**: Choose whether the reminder should be displayed in fullscreen mode.
- **Minimize to tray**: If enabled, the application will minimize to the system tray instead of closing.
- **Add to autostart**: The application will start automatically when your system boots.
- **Save settings**: Save the current settings.

### Minimizing to Tray

If the **Minimize to tray** option is enabled, the application will hide in the system tray when minimized. To restore the window, click on the application's tray icon and select **Restore**.

## Compilation to Executable

You can compile the application into a single executable file using PyInstaller.

### Installing PyInstaller

Install PyInstaller using pip:

```bash
pip install pyinstaller
```

### Compilation

Run the following command in the root directory of the project:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico --name=EyeBreakReminder --add-data "assets;assets" --add-data "translations;translations" main.py
```

**Explanation of the command:**

- `--onefile` — Creates a single executable file.
- `--windowed` — The application runs without a console window.
- `--icon=assets/icon.ico` — Specifies the icon for the executable.
- `--name=EyeBreakReminder` — Sets the name of the executable file.
- `--add-data "assets;assets"` — Includes the `assets` folder in the build.
- `--add-data "translations;translations"` — Includes the `translations` folder in the build.
- `main.py` — The main file of the application.

After successful compilation, the executable file will be located in the `dist` folder.

### Running the Executable

Navigate to the `dist` folder and run the `EyeBreakReminder` executable:

```bash
cd dist
./EyeBreakReminder
```

## Project Files

### `main.py`

The main executable file of the application. It contains the `EyeBreakReminder` class, which implements all the functionality of the application.

### `__init__.py`

Initialization file for the `eye_break_reminder` package. It can be left empty.

### `setup.py`

A script for installing the application as a package. If you wish to install the application system-wide, you can use this file.

### `assets/`

Folder containing resources:

- `icon.png` and `icon.ico` — Icons for the application.
- `sound.mp3` — Sound notification for the start of the break.
- `sound_end.mp3` — Sound notification for the end of the break.

### `translations/`

Folder containing translation files. It includes translations to support multiple languages.

## Logging

The application saves logs in the `AppData/EyeBreakReminder/eye_break_reminder.log` file. Logs help you track the application's activity and diagnose potential issues.

## Autostart (Windows Only)

The application can be added to the system's autostart. To enable this, check the **Add to autostart** option in the application's settings.

## Multilingual Support

The application supports multiple languages using Qt's translation system. By default, it attempts to load a translation based on your system's language settings.

## Development

### Requirements

- Python 3.x
- PyQt5
- pygame
- PyInstaller (for compilation)
- Additional modules: `os`, `sys`, `logging`, `threading`

### Running in Development Mode

You can run and test the application directly using Python:

```bash
python main.py
```

### Creating Translations

To add a new language, create the corresponding translation file in the `translations` folder and ensure it is loaded in the code.

## Contributing

If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note:** Ensure that all files and folders (especially `assets` and `translations`) are in the correct locations relative to the main `main.py` file or the executable file after compilation.

**Important:** When using PyInstaller on different platforms, various issues may arise. Please refer to the [PyInstaller documentation](https://pyinstaller.readthedocs.io/en/stable/) for additional information.

# Quick Start Guide

1. **Clone the repository or download the code** to your desired directory.

2. **Install dependencies**:

   ```bash
   pip install PyQt5 pygame
   ```

3. **Run the application**:

   ```bash
   python main.py
   ```

4. **Compile to an executable (optional)**:

   ```bash
   pyinstaller --onefile --windowed --icon=assets/icon.ico --name=EyeBreakReminder --add-data "assets;assets" --add-data "translations;translations" main.py
   ```

5. **Run the compiled application** from the `dist` folder.

---

We hope this application helps you take care of your eye health!