Here’s a suggested `README.md` file for your "EyeBreakReminder" project:


# EyeBreakReminder

EyeBreakReminder is a desktop application that helps users take regular breaks for their eyes. This application reminds users to look away from their screens periodically, which can help reduce eye strain, especially during extended screen time.

## Features
- **Eye Break Timer**: Sets a countdown timer (default 20 minutes) that reminds users to take breaks.
- **Customizable Volume**: Allows users to adjust the notification sound volume.
- **System Tray Integration**: Minimizes to the system tray for unobtrusive reminders.
- **Full-Screen Break Reminder**: Prompts the user to look away for 20 seconds once the timer ends, displaying a full-screen message.

## Project Structure
- `assets/`:
  - `icon.png`: The icon used for the application in the system tray.
  - `sound.mp3`: The sound played during break reminders.
- `eye_break_reminder/`: Contains the main application code.
  - `__init__.py`: Initializes the module.
  - `main.py`: Defines the main functionality of the EyeBreakReminder class.
- `run.py`: The main script to launch the application.
- `setup.py`: Script for packaging and distributing the application.
- `.gitignore`: Specifies files and directories ignored by Git.
- `LICENSE`: The project license.
- `README.md`: Project documentation.
- `requirements.txt`: Lists the dependencies required for the project.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/EyeBreakReminder.git
   cd EyeBreakReminder
   ```

2. **Set Up the Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python run.py
   ```

## Usage

- Launch the application by running `python run.py`.
- The application will start a 20-minute timer. After the timer ends, it will prompt you to take a 20-second break.
- Control the volume of the reminder sound using the slider in the application window.
- Minimize the application to the system tray by closing the window. You can restore it by selecting "Restore" from the tray menu.

## Requirements

- Python 3.6 or higher
- [PyQt5](https://pypi.org/project/PyQt5/) (>=5.15.0)
- [pygame](https://pypi.org/project/pygame/) (>=2.0.0)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Artem Tarasiuk – [email](mailto:artemtotal@gmail.com)
```

This `README.md` includes an overview, installation instructions, and basic usage guidelines for the EyeBreakReminder project based on the code and structure provided.