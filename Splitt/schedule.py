import random
import datetime
import data
from data import save_to_file, save_to_excel, reload_current_data, save_new_weeks_to_excel
from tkinter import messagebox

def update_statistics():
    for person in data.PEOPLE:
        watering_count = len(data.watering_history.get(person, []))
        data.WEIGHTS[data.PEOPLE.index(person)] = max(1, 10 - watering_count)
    save_to_file()

def calculate_weighted_score(person_index, selection_count, total_weeks_active=None):
    """Calculate weighted arithmetic mean score for a person"""
    person = data.PEOPLE[person_index]
    base_weight = data.WEIGHTS[person_index]
    watering_count = len(data.watering_history.get(person, []))
    recent_selections = selection_count.get(person, 0)
    
    # Calculate how long this person has been in the system
    if total_weeks_active is None:
        total_weeks_active = max(1, len([entry for entries in data.watering_history.values() for entry in entries if entry.startswith("Week")]) // len(data.PEOPLE))
    
    # Normalize watering count based on time active
    # For short-term people (< 4 weeks), give higher initial priority
    # For long-term people (> 52 weeks), use balanced approach
    if total_weeks_active <= 4:
        # Short-term: prioritize new people heavily
        fairness_factor = max(1, 5 - watering_count)
        time_factor = 2.0  # Boost for short-term people
    elif total_weeks_active <= 52:
        # Medium-term: balanced approach
        expected_waterings = total_weeks_active * 2 / len(data.PEOPLE)  # 2 people per week
        fairness_factor = max(0.5, expected_waterings - watering_count + 1)
        time_factor = 1.0
    else:
        # Long-term: focus on recent balance
        expected_waterings = total_weeks_active * 2 / len(data.PEOPLE)
        fairness_factor = max(0.5, expected_waterings - watering_count + 1)
        time_factor = 0.8  # Slight reduction for very long-term
    
    # Recent selection penalty (avoid consecutive selections)
    recent_penalty = max(0.1, 1.0 - (recent_selections * 0.3))
    
    # Weighted arithmetic mean calculation
    # Components: base_weight, fairness_factor, time_factor, recent_penalty
    score = (base_weight * 0.3) + (fairness_factor * 0.4) + (time_factor * 0.2) + (recent_penalty * 0.1)
    
    return max(0.1, score)  # Ensure minimum score

def select_people_weighted_mean(selection_count):
    """Select 2 people using weighted arithmetic mean approach"""
    # Calculate total weeks active in system - filter out non-list entries
    all_week_entries = []
    for entries in data.watering_history.values():
        if isinstance(entries, list):
            for entry in entries:
                if entry.startswith("Week"):
                    all_week_entries.append(entry)
    
    total_weeks_active = len(set(all_week_entries)) if all_week_entries else 1
    
    scores = []
    for i in range(len(data.PEOPLE)):
        score = calculate_weighted_score(i, selection_count, total_weeks_active)
        scores.append((data.PEOPLE[i], score))
    
    # Sort by score in descending order
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # For short-term scenarios (< 4 weeks), be more deterministic
    # For long-term scenarios, add controlled randomness to avoid staleness
    if total_weeks_active <= 4:
        # Short-term: pick top 2 directly with slight randomness
        top_candidates = scores[:min(3, len(scores))]
        candidates = [person for person, score in top_candidates]
        weights = [score for person, score in top_candidates]
        
        selected = []
        remaining_candidates = candidates.copy()
        remaining_weights = weights.copy()
        
        for _ in range(min(2, len(remaining_candidates))):
            if not remaining_candidates:
                break
            chosen = random.choices(remaining_candidates, weights=remaining_weights, k=1)[0]
            selected.append(chosen)
            idx = remaining_candidates.index(chosen)
            remaining_candidates.pop(idx)
            remaining_weights.pop(idx)
    else:
        # Long-term: use weighted selection from top candidates
        top_candidates = scores[:min(4, len(scores))]
        candidates = [person for person, score in top_candidates]
        weights = [score for person, score in top_candidates]
        
        selected = []
        remaining_candidates = candidates.copy()
        remaining_weights = weights.copy()
        
        for _ in range(min(2, len(remaining_candidates))):
            if not remaining_candidates:
                break
            chosen = random.choices(remaining_candidates, weights=remaining_weights, k=1)[0]
            selected.append(chosen)
            idx = remaining_candidates.index(chosen)
            remaining_candidates.pop(idx)
            remaining_weights.pop(idx)
    
    return selected

def generate_schedule():
    # Reload data to ensure we're using the most current file
    reload_current_data()
    
    update_statistics()
    full_schedule = []  # Keep track of all generated weeks
    new_weeks_only = []  # Only the newly generated weeks
    selection_count = {person: len(data.watering_history[person]) for person in data.PEOPLE}
    current_year = datetime.date.today().year
    current_week = datetime.date.today().isocalendar()[1]
    
    # Determine which year we're currently working in based on the data file
    if data.FILE_PATH.endswith("people.json"):
        schedule_year = current_year  # 2025
    else:
        # Extract year from filename like "people_2026.json"
        import re
        match = re.search(r'people_(\d{4})\.json', data.FILE_PATH)
        schedule_year = int(match.group(1)) if match else current_year

    # Filter out non-list entries when checking for week entries
    week_entries_found = []
    for person in data.watering_history.values():
        if isinstance(person, list):
            for entry in person:
                if entry.startswith("Week"):
                    week_entries_found.append(entry)
    
    if week_entries_found:
        last_week = max([int(entry.split()[1]) for entry in week_entries_found])
        start_week = last_week + 1
    else:
        start_week = current_week + 1

    max_week = 52
    week = start_week
    
    # Generate 6 weeks of schedule
    for _ in range(6):
        # Handle year transition
        if week > max_week:
            # Save only the new weeks generated in the current year
            if new_weeks_only:
                save_new_weeks_to_excel(new_weeks_only, data.PEOPLE, data.watering_history, target_year=schedule_year)
            
            # Transition to new year
            schedule_year = schedule_year + 1  # Increment from current year
            week = 1
            
            # Create new year data file and reset history
            new_json_file = f"people_{schedule_year}.json"
            new_history = {person: [] for person in data.PEOPLE}
            
            # Save new year file
            with open(new_json_file, "w") as file:
                import json
                json.dump({"PEOPLE": data.PEOPLE, "WEIGHTS": data.WEIGHTS, "WATERING_HISTORY": new_history}, file)
            
            # Update global variables in data module
            data.FILE_PATH = new_json_file
            data.watering_history = new_history
            
            # Reset selection count for new year
            selection_count = {person: 0 for person in data.PEOPLE}
            
            # Create new year Excel sheet
            save_to_excel([], data.PEOPLE, data.watering_history, new_year=True, target_year=schedule_year)
            new_weeks_only = []  # Reset new weeks for new year

        # Use weighted arithmetic mean selection
        selected = select_people_weighted_mean(selection_count)

        for person in selected:
            selection_count[person] += 1
            data.watering_history[person].append(f"Week {week}")

        week_entry = f"Week {week}: {selected[0]} and {selected[1]}"
        new_weeks_only.append(week_entry)
        full_schedule.append(week_entry)
        week += 1

    save_to_file()
    
    # Save only the newly generated weeks to Excel
    if new_weeks_only:
        save_new_weeks_to_excel(new_weeks_only, data.PEOPLE, data.watering_history, target_year=schedule_year)
    
    return full_schedule

def show_schedule():
    # Reload current data before generating schedule
    reload_current_data()
    schedule = generate_schedule()
    result = "\n".join(schedule)
    messagebox.showinfo("Gießplan", result)
