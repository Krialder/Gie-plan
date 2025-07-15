# Gießplan

This project is a Python application to manage a watering schedule for plants, automatically generating fair assignments for multiple people.

## How to Run

1. Make sure you have Python installed.
2. Install the required dependencies (see below).
3. Run the script using the command:

```bash
python main.py
```

## Features

- **GUI Interface**: Simple and intuitive tkinter-based interface
- **Fair Schedule Generation**: Automatically generates 6-week watering schedules using weighted selection
- **Multi-Person Management**: Add/remove people with automatic weight rebalancing
- **Year Transition Support**: Automatically handles year transitions with separate data files
- **Excel Export**: Saves schedules to Excel with separate sheets for each year
- **Persistent Data**: Stores people, weights, and watering history in JSON files
- **Manual Schedule Editing**: Add or remove specific dates/weeks manually

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

The project consists of four main Python modules:

1. **`main.py`**: Entry point that launches the GUI application
2. **`gui.py`**: Main GUI interface built with tkinter
   - Add/remove people from the watering schedule
   - Generate new schedules
   - Manually add/remove specific dates or weeks
3. **`data.py`**: Data management and file operations
   - Handles JSON file operations for people and history
   - Manages Excel export functionality
   - Automatic year file detection and creation
4. **`schedule.py`**: Schedule generation logic
   - Uses weighted arithmetic mean for fair person selection
   - Handles year transitions automatically
   - Generates 6-week schedules with balanced assignments

## Data Files

- `people.json`: Current year's people and watering history
- `people_YYYY.json`: Year-specific data files (auto-generated)
- `Gießplan.xlsx`: Excel output with Statistics and Schedule sheets

## Algorithm

The application uses a sophisticated weighted selection algorithm that:
- Balances workload fairly among all participants
- Adapts to system duration (short-term vs long-term)
- Prevents consecutive assignments for the same person
- Automatically adjusts when people join or leave

## Running the Code

1. Navigate to the project directory:
   ```bash
   cd i:\Gießplan
   ```

2. Run the script using your system's Python:
   ```bash
   python main.py
   ```

## Usage

1. **Adding People**: Enter a name and click "Add Person"
2. **Removing People**: Enter a name and click "Delete Person" 
3. **Generate Schedule**: Click "Generate Gießplan" to create a 6-week schedule
4. **Manual Entries**: Use the Date/Week fields to manually add or remove specific assignments
5. **Excel Export**: Schedules are automatically saved to `Gießplan.xlsx`

## File Structure

```
Gießplan/
├── main.py              # Application entry point
├── gui.py               # GUI interface
├── data.py              # Data management
├── schedule.py          # Schedule generation
├── people.json          # Current data
├── people_YYYY.json     # Year-specific data
├── Gießplan.xlsx        # Excel output
└── README.md           # This file
```

## Future Enhancements

- Database integration for better data persistence
- Email/SMS notifications for watering reminders
- Mobile app interface
- Advanced scheduling options (holidays, vacations)
- Historical analytics and reporting
