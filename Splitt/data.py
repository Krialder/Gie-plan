
import json
import os
import openpyxl
import datetime
from tkinter import messagebox

FILE_PATH = "people.json"

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
    PEOPLE = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    WEIGHTS = [1, 2, 1, 1, 2, 1]
    watering_history = {person: [] for person in PEOPLE}
    with open(FILE_PATH, "w") as file:
        json.dump({"PEOPLE": PEOPLE, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": watering_history}, file)

def save_to_file():
    with open(FILE_PATH, "w") as file:
        json.dump({"PEOPLE": PEOPLE, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": watering_history}, file)

def save_to_excel(schedule, people, history, new_year=False):
    file_name = "Gießplan.xlsx"
    current_year = datetime.date.today().year
    file_exists = os.path.exists(file_name)

    if file_exists:
        workbook = openpyxl.load_workbook(file_name)
        if f"Schedule {current_year}" in workbook.sheetnames:
            sheet1 = workbook["Statistics"]
            sheet2 = workbook[f"Schedule {current_year}"]
        else:
            sheet2 = workbook.create_sheet(title=f"Schedule {current_year}")
            sheet2.append(["Week", "Person 1", "Person 2"])

        if new_year:
            next_year = current_year + 1
            if f"Schedule {next_year}" not in workbook.sheetnames:
                sheet2 = workbook.create_sheet(title=f"Schedule {next_year}")
                sheet2.append(["Week", "Person 1", "Person 2"])

            new_json_file = f"people_{next_year}.json"
            new_history = {person: [] for person in people}
            with open(new_json_file, "w") as file:
                json.dump({"PEOPLE": people, "WEIGHTS": WEIGHTS, "WATERING_HISTORY": new_history}, file)

            global FILE_PATH
            FILE_PATH = new_json_file

            global watering_history
            watering_history = new_history

    else:
        workbook = openpyxl.Workbook()
        sheet1 = workbook.active
        sheet1.title = "Statistics"
        sheet1.append(["Name", "Watering Count", "Weight"])
        sheet2 = workbook.create_sheet(title=f"Schedule {current_year}")
        sheet2.append(["Week", "Person 1", "Person 2"])

    for i, person in enumerate(people):
        watering_count = len(history.get(person, []))
        sheet1.append([person, watering_count, WEIGHTS[i]])

    for i, week in enumerate(schedule):
        try:
            week_number, people = week.split(": ")
            if " and " in people:
                person1, person2 = people.split(" and ")
                if int(week_number.split()[1]) > 52 and new_year:
                    next_year = current_year + 1
                    sheet2 = workbook[f"Schedule {next_year}"]
                sheet2.append([week_number, person1, person2])
            else:
                sheet2.append([week_number, "", ""])
        except ValueError:
            sheet2.append(["", "", ""])

    workbook.save(file_name)
    messagebox.showinfo("Success", f"Plan saved to Excel in sheet 'Schedule {current_year}' of '{file_name}'.")

def refresh_dependencies():

    for person in PEOPLE:
        if person not in watering_history:
            watering_history[person] = []
    for person in list(watering_history.keys()):
        if person not in PEOPLE:
            del watering_history[person]
    update_weights()
    save_to_file()


