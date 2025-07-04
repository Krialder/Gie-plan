# Gießplan

This project is a Python script to manage a watering schedule for plants.

## How to Run

1. Make sure you have Python installed.
2. Run the script using the command:

```bash
python main.py
```

## Features

- Simple and intuitive interface.
- Manage watering schedules for multiple plants.

## Future Enhancements

- Add a database to store plant information.
- Implement notifications for watering reminders.

## Installing Dependencies

To use this project, ensure you have Python installed on your system. Additionally, install the required libraries:

1. Install `tkinter` for GUI functionality:
   - On most systems, `tkinter` is included with Python by default. If not, you can install it using your package manager.
   - For Debian-based systems (e.g., Ubuntu), run:
     ```bash
     sudo apt-get install python3-tk
     ```
   - For Red Hat-based systems (e.g., Fedora), run:
     ```bash
     sudo dnf install python3-tkinter
     ```

2. Install `openpyxl` for Excel interaction:
   ```bash
   pip install openpyxl
   ```

## How the Code Works

The project consists of a single script:

1. **`main.py`**:
   - Provides a GUI for managing the watering schedule.
   - Generates a 6-week schedule and saves it to an Excel file (`Gießplan.xlsx`).

## Running the Code

1. Navigate to the project directory:
   ```bash
   cd g:\Gießplan
   ```

2. Run the script using your system's Python:
   ```bash
   python main.py
   ```
