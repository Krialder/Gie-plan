import tkinter as tk
from tkinter import messagebox
from data import save_to_file, save_to_excel, refresh_dependencies, PEOPLE, WEIGHTS, watering_history
from schedule import show_schedule

# Create the GUI
root = tk.Tk()
root.title("Gießplan Generator")

# Widgets for adding and deleting people
name_label = tk.Label(root, text="Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

def add_person():
    name = name_entry.get()
    if name.isalpha() and name not in PEOPLE:
        PEOPLE.append(name)
        WEIGHTS.append(1)  # Default weight for new person
        watering_history[name] = []
        update_people_list()
        refresh_dependencies()
    else:
        messagebox.showerror("Error", "Invalid or duplicate name.")

def delete_person():
    name = name_entry.get()
    if name in PEOPLE:
        index = PEOPLE.index(name)
        PEOPLE.pop(index)
        WEIGHTS.pop(index)
        watering_history.pop(name, None)
        update_people_list()
        refresh_dependencies()
    else:
        messagebox.showerror("Error", "Name not found.")

add_button = tk.Button(root, text="Add Person", command=add_person)
add_button.pack(pady=5)
delete_button = tk.Button(root, text="Delete Person", command=delete_person)
delete_button.pack(pady=5)

# Listbox to display people and their watering history

people_list = tk.Listbox(root, width=50)
people_list.pack(pady=10)

def update_people_list():
    for person in PEOPLE:
        if person not in watering_history:
            watering_history[person] = []
    for person in list(watering_history.keys()):
        if person not in PEOPLE:
            del watering_history[person]
    people_list.delete(0, tk.END)
    for person in PEOPLE:
        people_list.insert(tk.END, person)

update_people_list()

# Button to generate the schedule
generate_button = tk.Button(root, text="Generate Gießplan", command=show_schedule)
generate_button.pack(pady=10)

# Additional GUI elements for adding/deleting specific dates or weeks
label_date = tk.Label(root, text="Date/Week:")
label_date.pack(pady=5)
date_entry = tk.Entry(root)
date_entry.pack(pady=5)

label_person1 = tk.Label(root, text="Person 1:")
label_person1.pack(pady=5)
person1_entry = tk.Entry(root)
person1_entry.pack(pady=5)

label_person2 = tk.Label(root, text="Person 2:")
label_person2.pack(pady=5)
person2_entry = tk.Entry(root)
person2_entry.pack(pady=5)

def add_date_or_week():
    date_or_week = date_entry.get()
    person1 = person1_entry.get()
    person2 = person2_entry.get()

    if date_or_week and person1 and person2:
        if date_or_week.startswith("Week"):
            week_number = date_or_week.split()[1]
            schedule_entry = f"Week {week_number}: {person1} and {person2}"
        else:
            schedule_entry = f"Date {date_or_week}: {person1} and {person2}"

        # Append to watering history
        watering_history[person1].append(schedule_entry)
        watering_history[person2].append(schedule_entry)

        # Save changes to JSON file
        save_to_file()

        # Save to Excel
        save_to_excel([schedule_entry], PEOPLE, watering_history)
        messagebox.showinfo("Success", "Date/Week added successfully.")
    else:
        messagebox.showerror("Error", "Invalid input. Please provide a date/week and two people.")

def delete_date_or_week():
    date_or_week = date_entry.get()

    if date_or_week:
        for person in PEOPLE:
            watering_history[person] = [entry for entry in watering_history[person] if not entry.startswith(date_or_week)]

        # Save changes to JSON file
        save_to_file()

        # Save updated history to Excel
        save_to_excel([], PEOPLE, watering_history)
        messagebox.showinfo("Success", "Date/Week deleted successfully.")
    else:
        messagebox.showerror("Error", "Invalid input. Please provide a date/week.")

add_date_button = tk.Button(root, text="Add Date/Week", command=add_date_or_week)
add_date_button.pack(pady=5)
delete_date_button = tk.Button(root, text="Delete Date/Week", command=delete_date_or_week)
delete_date_button.pack(pady=5)

root.mainloop()
