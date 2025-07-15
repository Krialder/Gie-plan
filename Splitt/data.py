import json
import os
import openpyxl
import datetime
from tkinter import messagebox

FILE_PATH = "people.json"

# Function to get the most recent people file
def get_current_people_file():
    current_year = datetime.date.today().year
    
    # Check for year-specific files, prioritizing the most recent
    # Check several years ahead (in case of multiple year transitions), then current, then previous years
    for year in range(current_year + 5, current_year - 3, -1):  # Check current+5 down to current-2
        year_file = f"people_{year}.json"
        if os.path.exists(year_file):
            return year_file
    
    # Fall back to default file
    return "people.json"

# Use the most recent people file
FILE_PATH = get_current_people_file()

# Load names from file or use default ones
if os.path.exists(FILE_PATH):
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
            PEOPLE = data.get("PEOPLE", [])
            WEIGHTS = data.get("WEIGHTS", [])
            watering_history = data.get("WATERING_HISTORY", {})
    except json.JSONDecodeError:
        PEOPLE = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        WEIGHTS = [1, 2, 1, 1, 2, 1]
        watering_history = {person: [] for person in PEOPLE}
        with open(FILE_PATH, "w") as file:
            json.dump({"PEOPLE": PEOPLE, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": watering_history}, file)
else:
    PEOPLE = ["Jan", "Jeff", "Antonia", "Melissa", "Rosa", "Alexander"]
    WEIGHTS = [1, 2, 1, 1, 2, 1]
    watering_history = {person: [] for person in PEOPLE}
    with open(FILE_PATH, "w") as file:
        json.dump({"PEOPLE": PEOPLE, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": watering_history}, file)

def reload_current_data():
    """Reload data from the most current file"""
    global FILE_PATH, PEOPLE, WEIGHTS, watering_history
    
    FILE_PATH = get_current_people_file()
    
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                PEOPLE = data.get("PEOPLE", [])
                WEIGHTS = data.get("WEIGHTS", [])
                watering_history = data.get("WATERING_HISTORY", {})
        except json.JSONDecodeError:
            pass  # Keep current data if file is corrupted

def save_to_file():
    global FILE_PATH
    # Don't change FILE_PATH here - use the current one
    with open(FILE_PATH, "w") as file:
        json.dump({"PEOPLE": PEOPLE, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": watering_history}, file)

def update_weights():
    """Update weights based on watering history to maintain balance"""
    # Calculate total weeks active in system - filter out non-list entries
    all_week_entries = []
    for entries in watering_history.values():
        if isinstance(entries, list):
            for entry in entries:
                if entry.startswith("Week"):
                    all_week_entries.append(entry)
    
    total_weeks_active = len(set(all_week_entries)) if all_week_entries else 1
    
    for i, person in enumerate(PEOPLE):
        watering_count = len(watering_history.get(person, []))
        
        # Adaptive weight calculation based on system duration
        if total_weeks_active <= 4:
            # Short-term: Higher weights for new people
            WEIGHTS[i] = max(1, 8 - watering_count)
        elif total_weeks_active <= 52:
            # Medium-term: Balanced approach
            expected_waterings = total_weeks_active * 2 / len(PEOPLE)
            WEIGHTS[i] = max(1, int(expected_waterings - watering_count + 5))
        else:
            # Long-term: Focus on recent balance, normalized weights
            expected_waterings = total_weeks_active * 2 / len(PEOPLE)
            deviation = expected_waterings - watering_count
            WEIGHTS[i] = max(1, int(5 + deviation))
    
    save_to_file()

def save_to_excel(schedule, people, history, new_year=False, target_year=None):
    file_name = "Gießplan.xlsx"
    current_year = datetime.date.today().year
    
    # Determine which year we're working with
    if target_year:
        schedule_year = target_year
    elif new_year:
        schedule_year = current_year + 1
    else:
        schedule_year = current_year
    
    file_exists = os.path.exists(file_name)

    if file_exists:
        workbook = openpyxl.load_workbook(file_name)
        
        # Ensure Statistics sheet exists
        if "Statistics" not in workbook.sheetnames:
            sheet1 = workbook.create_sheet(title="Statistics")
            sheet1.append(["Name", "Watering Count", "Weight"])
        else:
            sheet1 = workbook["Statistics"]
            # Clear existing statistics
            sheet1.delete_rows(2, sheet1.max_row)
        
        # Ensure target year schedule sheet exists
        if f"Schedule {schedule_year}" not in workbook.sheetnames:
            sheet2 = workbook.create_sheet(title=f"Schedule {schedule_year}")
            sheet2.append(["Week", "Person 1", "Person 2"])
        else:
            sheet2 = workbook[f"Schedule {schedule_year}"]
            # Always clear existing schedule entries when saving new data
            # This prevents accumulation of old entries
            if sheet2.max_row > 1:
                sheet2.delete_rows(2, sheet2.max_row)

        if new_year:
            # When creating a new year, create the new JSON file
            new_json_file = f"people_{schedule_year}.json"
            new_history = {person: [] for person in people}
            with open(new_json_file, "w") as file:
                json.dump({"PEOPLE": people, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": new_history}, file)

    else:
        workbook = openpyxl.Workbook()
        sheet1 = workbook.active
        sheet1.title = "Statistics"
        sheet1.append(["Name", "Watering Count", "Weight"])
        sheet2 = workbook.create_sheet(title=f"Schedule {schedule_year}")
        sheet2.append(["Week", "Person 1", "Person 2"])

    # Update statistics
    for i, person in enumerate(people):
        watering_count = len(history.get(person, []))
        if i < len(WEIGHTS):
            sheet1.append([person, watering_count, WEIGHTS[i]])
        else:
            sheet1.append([person, watering_count, 1])

    # Add schedule entries to the correct year's sheet
    for i, week in enumerate(schedule):
        try:
            week_number, people_str = week.split(": ")
            if " and " in people_str:
                person1, person2 = people_str.split(" and ")
                sheet2.append([week_number, person1, person2])
            else:
                sheet2.append([week_number, "", ""])
        except ValueError:
            sheet2.append(["", "", ""])

    workbook.save(file_name)
    if schedule:  # Only show success message if there are actual schedule entries
        messagebox.showinfo("Success", f"Plan saved to Excel in sheet 'Schedule {schedule_year}' of '{file_name}'.")

def save_new_weeks_to_excel(new_weeks, people, history, target_year=None):
    """Save only new weeks to Excel, appending to existing schedule"""
    file_name = "Gießplan.xlsx"
    current_year = datetime.date.today().year
    
    # Determine which year we're working with
    if target_year:
        schedule_year = target_year
    else:
        schedule_year = current_year
    
    file_exists = os.path.exists(file_name)

    if file_exists:
        workbook = openpyxl.load_workbook(file_name)
        
        # Ensure Statistics sheet exists
        if "Statistics" not in workbook.sheetnames:
            sheet1 = workbook.create_sheet(title="Statistics")
            sheet1.append(["Name", "Watering Count", "Weight"])
        else:
            sheet1 = workbook["Statistics"]
            # Clear existing statistics
            sheet1.delete_rows(2, sheet1.max_row)
        
        # Ensure target year schedule sheet exists
        if f"Schedule {schedule_year}" not in workbook.sheetnames:
            sheet2 = workbook.create_sheet(title=f"Schedule {schedule_year}")
            sheet2.append(["Week", "Person 1", "Person 2"])
        else:
            sheet2 = workbook[f"Schedule {schedule_year}"]
            # DO NOT clear existing schedule entries - we want to append

    else:
        workbook = openpyxl.Workbook()
        sheet1 = workbook.active
        sheet1.title = "Statistics"
        sheet1.append(["Name", "Watering Count", "Weight"])
        sheet2 = workbook.create_sheet(title=f"Schedule {schedule_year}")
        sheet2.append(["Week", "Person 1", "Person 2"])

    # Update statistics
    for i, person in enumerate(people):
        watering_count = len(history.get(person, []))
        if i < len(WEIGHTS):
            sheet1.append([person, watering_count, WEIGHTS[i]])
        else:
            sheet1.append([person, watering_count, 1])

    # Add only the new schedule entries to the correct year's sheet
    for i, week in enumerate(new_weeks):
        try:
            week_number, people_str = week.split(": ")
            if " and " in people_str:
                person1, person2 = people_str.split(" and ")
                sheet2.append([week_number, person1, person2])
            else:
                sheet2.append([week_number, "", ""])
        except ValueError:
            sheet2.append(["", "", ""])

    workbook.save(file_name)
    if new_weeks:  # Only show success message if there are actual new schedule entries
        messagebox.showinfo("Success", f"Plan saved to Excel in sheet 'Schedule {schedule_year}' of '{file_name}'.")

def refresh_dependencies():

    for person in PEOPLE:
        if person not in watering_history:
            watering_history[person] = []
    for person in list(watering_history.keys()):
        if person not in PEOPLE:
            del watering_history[person]
    update_weights()
    save_to_file()

def add_new_person_with_context(name, join_week=None):
    """Add a new person with context-appropriate initial weight"""
    if name in PEOPLE:
        return False
    
    # Calculate system context - filter out non-list entries
    all_week_entries = []
    for entries in watering_history.values():
        if isinstance(entries, list):
            for entry in entries:
                if entry.startswith("Week"):
                    all_week_entries.append(entry)
    
    total_weeks_active = len(set(all_week_entries)) if all_week_entries else 1
    
    # Calculate appropriate initial weight based on when they join
    if total_weeks_active <= 4:
        # Early in system: standard weight
        initial_weight = 5
    elif total_weeks_active <= 52:
        # Mid-system: higher weight to catch up
        list_histories = [history for history in watering_history.values() if isinstance(history, list)]
        average_waterings = sum(len(history) for history in list_histories) / len(PEOPLE) if PEOPLE else 0
        initial_weight = max(1, int(8 + average_waterings))
    else:
        # Late in system: significantly higher weight to catch up quickly
        list_histories = [history for history in watering_history.values() if isinstance(history, list)]
        average_waterings = sum(len(history) for history in list_histories) / len(PEOPLE) if PEOPLE else 0
        initial_weight = max(1, int(10 + average_waterings))
    
    PEOPLE.append(name)
    WEIGHTS.append(initial_weight)
    watering_history[name] = []
    save_to_file()
    return True

def remove_person_and_rebalance(name):
    """Remove a person and rebalance the system"""
    if name not in PEOPLE:
        return False
    
    # Store the person's watering history before removal
    leaving_person_waterings = len(watering_history.get(name, []))
    
    # Remove the person
    index = PEOPLE.index(name)
    PEOPLE.pop(index)
    WEIGHTS.pop(index)
    watering_history.pop(name, None)
    
    # Rebalance remaining people's weights
    # If someone was carrying more load, adjust others accordingly
    if leaving_person_waterings > 0 and len(PEOPLE) > 0:
        # Distribute some of the leaving person's "load" to others
        load_redistribution = max(1, leaving_person_waterings // len(PEOPLE))
        for i in range(len(PEOPLE)):
            WEIGHTS[i] = max(1, WEIGHTS[i] - load_redistribution)
    
    update_weights()
    save_to_file()
    return True


