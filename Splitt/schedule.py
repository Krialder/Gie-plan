import random
import datetime
from data import save_to_file, save_to_excel, PEOPLE, WEIGHTS, watering_history
from tkinter import messagebox

def update_statistics():
    for person in PEOPLE:
        watering_count = len(watering_history.get(person, []))
        WEIGHTS[PEOPLE.index(person)] = max(1, 10 - watering_count)
    save_to_file()

def generate_schedule():
    update_statistics()
    schedule = []
    selection_count = {person: len(watering_history[person]) for person in PEOPLE}
    current_year = datetime.date.today().year
    current_week = datetime.date.today().isocalendar()[1]

    if any(entry.startswith("Week") for person in watering_history.values() for entry in person):
        last_week = max(
            [int(entry.split()[1]) for person in watering_history.values() for entry in person if entry.startswith("Week")]
        )
        start_week = last_week + 1
    else:
        start_week = current_week + 1

    max_week = 52
    week = start_week
    while len(schedule) < 6:
        if week > max_week:
            current_year += 1
            week = 1
            watering_history["last_year"] = current_year
            save_to_excel([], PEOPLE, watering_history, new_year=True)

        adjusted_weights = [WEIGHTS[i] / (1 + selection_count[PEOPLE[i]]) for i in range(len(PEOPLE))]
        selected = random.choices(PEOPLE, weights=adjusted_weights, k=2)

        for person in selected:
            selection_count[person] += 1
            watering_history[person].append(f"Week {week}")

        schedule.append(f"Week {week}: {selected[0]} and {selected[1]}")
        week += 1

        if week > max_week:
            save_to_excel(schedule, PEOPLE, watering_history)
            schedule = []

    save_to_file()
    return schedule

def show_schedule():
    schedule = generate_schedule()
    result = "\n".join(schedule)
    save_to_excel(
        schedule,
        PEOPLE,
        watering_history
    )
    messagebox.showinfo("Gießplan", result)
