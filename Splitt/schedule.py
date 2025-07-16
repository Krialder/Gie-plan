import random
import datetime
import json
import os
import re
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
        total_weeks_active = max(1, len([entry for entries in data.watering_history.values() for entry in entries if "KW" in entry]) // len(data.PEOPLE))
    
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
                if "KW" in entry:
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

def generate_schedule(schedule_type="Next 6 Weeks"):
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
        match = re.search(r'people_(\d{4})\.json', data.FILE_PATH)
        schedule_year = int(match.group(1)) if match else current_year

    # Filter out non-list entries when checking for week entries
    week_entries_found = []
    for person in data.watering_history.values():
        if isinstance(person, list):
            for entry in person:
                if "KW" in entry:
                    week_entries_found.append(entry)
    
    if week_entries_found:
        # Extract week numbers from KW entries (e.g., "2025 KW 15: ..." -> 15)
        week_numbers = []
        for entry in week_entries_found:
            if "KW" in entry:
                try:
                    # Find KW pattern and extract number
                    match = re.search(r'KW (\d+)', entry)
                    if match:
                        week_numbers.append(int(match.group(1)))
                except:
                    pass
        
        if week_numbers:
            last_week = max(week_numbers)
            # If last week is 52 or higher, start from week 1 of next year
            if last_week >= 52:
                if schedule_type == "Next 6 Weeks":
                    # Ask user if they want to create a new year
                    response = messagebox.askyesno("Year Complete", 
                                                f"Year {schedule_year} is complete (week {last_week} was the last week).\n\n"
                                                f"Do you want to create a new year {schedule_year + 1} and generate 6 weeks there?")
                    if response:
                        start_week = 1
                        schedule_year = schedule_year + 1
                        
                        # Create the new year file if it doesn't exist
                        new_year_file = f"people_{schedule_year}.json"
                        if not os.path.exists(new_year_file):
                            try:
                                # Create new year file with current people but empty watering history
                                new_year_data = {
                                    "PEOPLE": data.PEOPLE[:],  # Copy current people
                                    "WEIGHTS": data.WEIGHTS[:],  # Copy current weights
                                    "WATERING_HISTORY": {person: [] for person in data.PEOPLE}  # Empty history for new year
                                }
                                
                                # Try to write the file with better error handling
                                try:
                                    with open(new_year_file, "w") as file:
                                        json.dump(new_year_data, file, indent=2)
                                except PermissionError:
                                    messagebox.showerror("File Permission Error", 
                                                       f"Cannot create {new_year_file} - file may be open in another application.\n\n"
                                                       f"Please close any Excel files or other applications using this file and try again.")
                                    return []
                                except Exception as file_error:
                                    messagebox.showerror("File Creation Error", 
                                                       f"Failed to create {new_year_file}: {str(file_error)}")
                                    return []
                                    
                                print(f"Created new year file: {new_year_file}")
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to create new year file: {str(e)}")
                                return []
                        
                        # Load the new year data
                        if not data.load_year_data(schedule_year):
                            messagebox.showerror("Error", f"Failed to load new year data for {schedule_year}")
                            return []
                    else:
                        # User cancelled, return empty schedule
                        return []
                else:
                    # For "Remaining Weeks", if we're already at week 52, there are no remaining weeks
                    start_week = 53  # This will result in 0 weeks to generate
            else:
                start_week = last_week + 1
        else:
            start_week = current_week + 1
    else:
        start_week = current_week + 1

    max_week = 52
    week = start_week
    year_transition_occurred = False  # Initialize for both schedule types
    
    # Calculate number of weeks to generate based on schedule type
    if schedule_type == "Remaining Weeks":
        # Calculate remaining weeks in current year
        if week <= max_week:
            weeks_to_generate = max_week - week + 1
        else:
            weeks_to_generate = 0  # No remaining weeks if we're already past week 52
            messagebox.showinfo("Year Complete", f"Year {schedule_year} is already complete. No remaining weeks to generate.")
            return []
        
        # Generate schedule for the calculated number of weeks
        for _ in range(weeks_to_generate):
            # Handle year transition
            if week > max_week:
                year_transition_occurred = True
                
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
                data.watering_history[person].append(f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}")

            week_entry = f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}"
            new_weeks_only.append(week_entry)
            full_schedule.append(week_entry)
            week += 1
    
    else:  # "Next 6 Weeks"
        weeks_to_generate = 6
        
        # Check if we'll cross a year boundary within the next 6 weeks
        weeks_remaining_in_year = max_week - week + 1
        
        # If we're already at or past week 52, or if we need to cross year boundary
        if weeks_remaining_in_year <= 0 or weeks_remaining_in_year < weeks_to_generate:
            year_transition_occurred = True
            
            # If we're already past week 52, skip to new year directly
            if weeks_remaining_in_year <= 0:
                year_transition_message = f"Year transition detected:\n\n"
                year_transition_message += f"Current year {schedule_year - 1} is already complete.\n"
                year_transition_message += f"Starting new year {schedule_year} with 6 weeks...\n"
                
                # We should already be in the new year due to the logic above
                # Generate all 6 weeks for the new year
                for _ in range(weeks_to_generate):
                    # Use weighted arithmetic mean selection
                    selected = select_people_weighted_mean(selection_count)

                    for person in selected:
                        selection_count[person] += 1
                        data.watering_history[person].append(f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}")

                    week_entry = f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}"
                    new_weeks_only.append(week_entry)
                    full_schedule.append(week_entry)
                    week += 1
                
                year_transition_message += f"✓ Generated 6 weeks for new year {schedule_year} (KW 1-6)\n"
                messagebox.showinfo("Year Transition Complete", year_transition_message)
                
            else:
                # We need to finish current year first, then start new year
                year_transition_message = f"Year transition detected:\n\n"
                year_transition_message += f"Step 1: Completing current year {schedule_year} with {weeks_remaining_in_year} weeks remaining...\n"
                
                current_year_weeks = []  # Track weeks for current year
                current_year_start_week = week  # Remember the starting week for this year
                
                # Generate ALL remaining weeks for the current year
                for _ in range(weeks_remaining_in_year):
                    # Use weighted arithmetic mean selection
                    selected = select_people_weighted_mean(selection_count)

                    for person in selected:
                        selection_count[person] += 1
                        data.watering_history[person].append(f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}")

                    week_entry = f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}"
                    current_year_weeks.append(week_entry)
                    full_schedule.append(week_entry)
                    week += 1
                
                # IMMEDIATELY save the completed year's schedule and data
                if current_year_weeks:
                    save_new_weeks_to_excel(current_year_weeks, data.PEOPLE, data.watering_history, target_year=schedule_year)
                    save_to_file()  # Save current year's data to JSON immediately
                current_year_end_week = week - 1
                if current_year_start_week == current_year_end_week:
                    year_transition_message += f"✓ Completed and saved 1 week for year {schedule_year} (KW {current_year_start_week})\n"
                else:
                    year_transition_message += f"✓ Completed and saved {len(current_year_weeks)} weeks for year {schedule_year} (KW {current_year_start_week}-{current_year_end_week})\n"
            
            year_transition_message += f"✓ Year {schedule_year} is now complete and saved.\n"
            
            # Step 2: NOW transition to new year
            original_schedule_year = schedule_year
            schedule_year = schedule_year + 1
            week = 1
            
            year_transition_message += f"\nStep 2: Now transitioning to new year {schedule_year}...\n"
            
            # Create new year data file and reset history
            new_json_file = f"people_{schedule_year}.json"
            new_history = {person: [] for person in data.PEOPLE}
            
            # Save new year file
            with open(new_json_file, "w") as file:
                json.dump({"PEOPLE": data.PEOPLE, "WEIGHTS": data.WEIGHTS, "WATERING_HISTORY": new_history}, file)
            
            # Update global variables in data module
            data.FILE_PATH = new_json_file
            data.watering_history = new_history
            
            # Reset selection count for new year
            selection_count = {person: 0 for person in data.PEOPLE}
            
            # Create new year Excel sheet
            save_to_excel([], data.PEOPLE, data.watering_history, new_year=True, target_year=schedule_year)
            
            # Step 3: Generate remaining weeks for the new year
            remaining_weeks_needed = weeks_to_generate - weeks_remaining_in_year
            year_transition_message += f"✓ Created new year file: people_{schedule_year}.json\n"
            year_transition_message += f"\nStep 3: Generating {remaining_weeks_needed} weeks for new year {schedule_year}...\n"
            
            new_year_weeks = []  # Track weeks for new year
            new_year_start_week = week  # Should be 1 for new year
            
            for _ in range(remaining_weeks_needed):
                # Use weighted arithmetic mean selection
                selected = select_people_weighted_mean(selection_count)

                for person in selected:
                    selection_count[person] += 1
                    data.watering_history[person].append(f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}")

                week_entry = f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}"
                new_year_weeks.append(week_entry)
                full_schedule.append(week_entry)
                week += 1
            
            # Save the new year's schedule
            if new_year_weeks:
                save_new_weeks_to_excel(new_year_weeks, data.PEOPLE, data.watering_history, target_year=schedule_year)
                save_to_file()  # Save new year's data to JSON
                new_year_end_week = week - 1
                if new_year_start_week == new_year_end_week:
                    year_transition_message += f"✓ Generated and saved 1 week for new year {schedule_year} (KW {new_year_start_week})\n"
                else:
                    year_transition_message += f"✓ Generated and saved {len(new_year_weeks)} weeks for new year {schedule_year} (KW {new_year_start_week}-{new_year_end_week})\n"
            
            # Combine all weeks for the final list
            new_weeks_only = current_year_weeks + new_year_weeks
            
            year_transition_message += f"\nYear transition completed successfully!"
            
            # Create summary of all generated weeks
            total_weeks_summary = f"Total weeks generated: {len(new_weeks_only)}\n"
            if current_year_weeks:
                current_year_start = current_year_start_week
                current_year_end = current_year_start + len(current_year_weeks) - 1
                if len(current_year_weeks) == 1:
                    total_weeks_summary += f"• {original_schedule_year}: 1 week (KW {current_year_start})\n"
                else:
                    total_weeks_summary += f"• {original_schedule_year}: {len(current_year_weeks)} weeks (KW {current_year_start}-{current_year_end})\n"
            
            if new_year_weeks:
                if len(new_year_weeks) == 1:
                    total_weeks_summary += f"• {schedule_year}: 1 week (KW {new_year_start_week})\n"
                else:
                    total_weeks_summary += f"• {schedule_year}: {len(new_year_weeks)} weeks (KW {new_year_start_week}-{new_year_end_week})\n"
            
            year_transition_message += f"\n{total_weeks_summary}"
            
            # Show the transition summary
            messagebox.showinfo("Year Transition Complete", year_transition_message)
        
        else:
            # No year boundary crossing, generate normally
            year_transition_occurred = False
            start_week_for_message = week
            
            for _ in range(weeks_to_generate):
                # Use weighted arithmetic mean selection
                selected = select_people_weighted_mean(selection_count)

                for person in selected:
                    selection_count[person] += 1
                    data.watering_history[person].append(f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}")

                week_entry = f"{schedule_year} KW {week}: {selected[0]} and {selected[1]}"
                new_weeks_only.append(week_entry)
                full_schedule.append(week_entry)
                week += 1

    # Only save if we didn't already save during year transition
    if not year_transition_occurred:
        save_to_file()
    
    # Save only the newly generated weeks to Excel (only if not already saved during year transition)
    if new_weeks_only and not year_transition_occurred:
        save_new_weeks_to_excel(new_weeks_only, data.PEOPLE, data.watering_history, target_year=schedule_year)
    
    return full_schedule

def show_schedule(schedule_type="Next 6 Weeks"):
    # Reload current data before generating schedule
    reload_current_data()
    schedule = generate_schedule(schedule_type)
    result = "\n".join(schedule)
    messagebox.showinfo("Gießplan", result)
