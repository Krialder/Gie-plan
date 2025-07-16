import json
import os
import datetime
from tkinter import messagebox

FILE_PATH = "people.json"

# Global variables for people data
PEOPLE = []
WEIGHTS = []
EXTRA_WEIGHTS = []
watering_history = {}
experience_overrides = {}  # Manual experience level overrides

# Function to migrate data from people.json to people_YEAR.json format
def migrate_people_json_to_year_specific():
    """Migrate data from people.json to people_YEAR.json format"""
    current_year = datetime.date.today().year
    
    # If people.json exists and people_YEAR.json doesn't exist, migrate it
    if os.path.exists("people.json") and not os.path.exists(f"people_{current_year}.json"):
        try:
            # Read the current people.json
            with open("people.json", "r") as file:
                data = json.load(file)
            
            # Save it as people_YEAR.json
            with open(f"people_{current_year}.json", "w") as file:
                json.dump(data, file, indent=2)
            
            print(f"Migrated people.json to people_{current_year}.json")
            return True
        except Exception as e:
            print(f"Error migrating people.json: {e}")
            return False
    return False

def ensure_year_specific_files():
    """Ensure all data is in year-specific file format"""
    current_year = datetime.date.today().year
    
    # Migrate people.json to year-specific format
    if migrate_people_json_to_year_specific():
        print(f"Successfully migrated people.json to people_{current_year}.json")
    
    # Update FILE_PATH to use current year file
    global FILE_PATH
    FILE_PATH = f"people_{current_year}.json"

# Function to get all available year files
def get_available_years():
    """Get all available years from existing data files"""
    years = []
    current_year = datetime.date.today().year
    
    # Check for default file (current year)
    if os.path.exists("people.json"):
        years.append(current_year)
    
    # Check for year-specific files
    for year in range(current_year - 5, current_year + 10):  # Check wide range
        year_file = f"people_{year}.json"
        if os.path.exists(year_file):
            years.append(year)
    
    # Remove duplicates and sort
    years = sorted(list(set(years)))
    return years

# Function to load data from specific year
def load_year_data(year):
    """Load data from a specific year file"""
    global FILE_PATH, PEOPLE, WEIGHTS, watering_history, experience_overrides
    
    current_year = datetime.date.today().year
    
    # First, migrate people.json to year-specific format if needed
    if year == current_year:
        migrate_people_json_to_year_specific()
    
    # Always use year-specific file format
    target_file = f"people_{year}.json"
    
    # Try to load the file
    if os.path.exists(target_file):
        try:
            with open(target_file, "r") as file:
                data = json.load(file)
                PEOPLE.clear()
                PEOPLE.extend(data.get("PEOPLE", []))
                WEIGHTS.clear()
                WEIGHTS.extend(data.get("WEIGHTS", []))
                EXTRA_WEIGHTS.clear()
                EXTRA_WEIGHTS.extend(data.get("EXTRA_WEIGHTS", [1] * len(PEOPLE)))
                watering_history.clear()
                watering_history.update(data.get("WATERING_HISTORY", {}))
                experience_overrides.clear()
                experience_overrides.update(data.get("EXPERIENCE_OVERRIDES", {}))
                FILE_PATH = target_file
                return True
        except json.JSONDecodeError:
            return False
    else:
        # File doesn't exist, create it only if switching to current year
        if year == current_year:
            # Create default file for current year
            PEOPLE.clear()
            PEOPLE.extend(["Jan", "Jeff", "Antonia", "Melissa", "Rosa", "Alexander"])
            WEIGHTS.clear()
            WEIGHTS.extend([5, 5, 5, 5, 5, 5])  # Balanced initial weights
            EXTRA_WEIGHTS.clear()
            EXTRA_WEIGHTS.extend([3, 3, 3, 3, 3, 3])  # Balanced initial extra weights
            watering_history.clear()
            watering_history.update({person: [] for person in PEOPLE})
            experience_overrides.clear()
            FILE_PATH = target_file
            
            try:
                with open(target_file, "w") as file:
                    json.dump({
                        "PEOPLE": PEOPLE, 
                        "WEIGHTS": WEIGHTS, 
                        "EXTRA_WEIGHTS": EXTRA_WEIGHTS,
                        "WATERING_HISTORY": watering_history,
                        "EXPERIENCE_OVERRIDES": experience_overrides
                    }, file, indent=2)
                return True
            except PermissionError:
                print(f"Permission error writing to {target_file} - file may be open in another application")
                return False
            except Exception as e:
                print(f"Error writing to {target_file}: {str(e)}")
                return False
        else:
            # Don't create files for other years automatically
            return False

# Function to get the current year's people file
def get_current_people_file():
    current_year = datetime.date.today().year
    
    # First, try to get the current year's file
    current_year_file = f"people_{current_year}.json"
    if os.path.exists(current_year_file):
        return current_year_file
    
    # If current year file doesn't exist, check for people.json
    if os.path.exists("people.json"):
        return "people.json"
    
    # If neither exists, return the current year file path (will be created)
    return current_year_file

# Migrate people.json to year-specific format on startup
current_year = datetime.date.today().year
migrate_people_json_to_year_specific()

# Always start with the current year (2025)
FILE_PATH = f"people_{current_year}.json"

# Load names from file or use default ones
if os.path.exists(FILE_PATH):
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
            PEOPLE = data.get("PEOPLE", [])
            WEIGHTS = data.get("WEIGHTS", [])
            EXTRA_WEIGHTS = data.get("EXTRA_WEIGHTS", [1] * len(PEOPLE))  # Default extra weights
            watering_history = data.get("WATERING_HISTORY", {})
            experience_overrides = data.get("EXPERIENCE_OVERRIDES", {})
    except json.JSONDecodeError:
        PEOPLE = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        WEIGHTS = [5, 5, 5, 5, 5, 5]  # Balanced initial weights
        EXTRA_WEIGHTS = [3, 3, 3, 3, 3, 3]  # Balanced initial extra weights
        watering_history = {person: [] for person in PEOPLE}
        experience_overrides = {}
        with open(FILE_PATH, "w") as file:
            json.dump({
                "PEOPLE": PEOPLE, 
                "WEIGHTS": WEIGHTS, 
                "EXTRA_WEIGHTS": EXTRA_WEIGHTS, 
                "WATERING_HISTORY": watering_history,
                "EXPERIENCE_OVERRIDES": experience_overrides
            }, file)
else:
    PEOPLE = ["Jan", "Jeff", "Antonia", "Melissa", "Rosa", "Alexander"]
    WEIGHTS = [5, 5, 5, 5, 5, 5]  # Balanced initial weights
    EXTRA_WEIGHTS = [3, 3, 3, 3, 3, 3]  # Balanced initial extra weights
    watering_history = {person: [] for person in PEOPLE}
    experience_overrides = {}
    with open(FILE_PATH, "w") as file:
        json.dump({
            "PEOPLE": PEOPLE, 
            "WEIGHTS": WEIGHTS, 
            "EXTRA_WEIGHTS": EXTRA_WEIGHTS, 
            "WATERING_HISTORY": watering_history,
            "EXPERIENCE_OVERRIDES": experience_overrides
        }, file)

def get_current_year():
    """Get the year currently being worked on"""
    if FILE_PATH.endswith("people.json"):
        return datetime.date.today().year
    else:
        # Extract year from filename like "people_2026.json"
        import re
        match = re.search(r'people_(\d{4})\.json', FILE_PATH)
        return int(match.group(1)) if match else datetime.date.today().year

def reload_current_data():
    """Reload data from the currently selected file"""
    global FILE_PATH, PEOPLE, WEIGHTS, EXTRA_WEIGHTS, watering_history, experience_overrides
    
    # Use the current FILE_PATH instead of getting the most recent file
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                PEOPLE.clear()
                PEOPLE.extend(data.get("PEOPLE", []))
                WEIGHTS.clear()
                WEIGHTS.extend(data.get("WEIGHTS", []))
                EXTRA_WEIGHTS.clear()
                EXTRA_WEIGHTS.extend(data.get("EXTRA_WEIGHTS", [1] * len(PEOPLE)))
                watering_history.clear()
                watering_history.update(data.get("WATERING_HISTORY", {}))
                experience_overrides.clear()
                experience_overrides.update(data.get("EXPERIENCE_OVERRIDES", {}))
        except json.JSONDecodeError:
            pass  # Keep current data if file is corrupted

def get_person_experience_level(person):
    """Get experience level of a person based on their watering history or manual override"""
    # Check if there's a manual override first
    if person in experience_overrides:
        return experience_overrides[person]
    
    # Default to automatic calculation based on watering history
    watering_count = len(watering_history.get(person, []))
    if watering_count == 0:
        return "new"
    elif watering_count <= 2:
        return "beginner"
    elif watering_count <= 8:
        return "learning"
    else:
        return "experienced"

def set_person_experience_level(person, level):
    """Manually set a person's experience level
    
    Args:
        person (str): The person's name
        level (str): Experience level - must be one of: "new", "beginner", "learning", "experienced"
    
    Returns:
        bool: True if successful, False if invalid level or person not found
    """
    valid_levels = ["new", "beginner", "learning", "experienced"]
    
    if level not in valid_levels:
        print(f"Invalid experience level '{level}'. Must be one of: {valid_levels}")
        return False
    
    if person not in PEOPLE:
        print(f"Person '{person}' not found in PEOPLE list")
        return False
    
    # Set the manual override
    experience_overrides[person] = level
    print(f"Set {person}'s experience level to '{level}'")
    
    # Save to file
    save_to_file()
    return True

def remove_person_experience_override(person):
    """Remove manual experience level override for a person
    
    Args:
        person (str): The person's name
    
    Returns:
        bool: True if override was removed, False if no override existed
    """
    if person in experience_overrides:
        del experience_overrides[person]
        print(f"Removed experience level override for {person}")
        save_to_file()
        return True
    else:
        print(f"No experience level override found for {person}")
        return False

def get_all_experience_levels():
    """Get experience levels for all people
    
    Returns:
        dict: Dictionary mapping person names to their experience levels
    """
    return {person: get_person_experience_level(person) for person in PEOPLE}

def get_experienced_people():
    """Get list of experienced people who can mentor newcomers"""
    experienced = []
    for person in PEOPLE:
        if get_person_experience_level(person) == "experienced":
            experienced.append(person)
    return experienced

def get_new_people():
    """Get list of new people who need mentoring"""
    new_people = []
    for person in PEOPLE:
        experience_level = get_person_experience_level(person)
        watering_count = len(watering_history.get(person, []))
        
        # Include people who are new, beginner, or learning with low watering counts
        if (experience_level in ["new", "beginner"] or 
            (experience_level == "learning" and watering_count <= 5)):
            new_people.append(person)
    return new_people

def save_to_file():
    global FILE_PATH
    # Don't change FILE_PATH here - use the current one
    try:
        with open(FILE_PATH, "w") as file:
            json.dump({
                "PEOPLE": PEOPLE, 
                "WEIGHTS": WEIGHTS, 
                "EXTRA_WEIGHTS": EXTRA_WEIGHTS, 
                "WATERING_HISTORY": watering_history,
                "EXPERIENCE_OVERRIDES": experience_overrides
            }, file, indent=2)
    except PermissionError:
        print(f"Permission error writing to {FILE_PATH} - file may be open in another application")
        raise PermissionError(f"Cannot write to {FILE_PATH} - file may be open in another application")
    except Exception as e:
        print(f"Error writing to {FILE_PATH}: {str(e)}")
        raise

def update_weights():
    """Update weights based on watering history to maintain balance - newcomer friendly"""
    # Calculate total weeks active in system - filter out non-list entries
    all_week_entries = []
    for entries in watering_history.values():
        if isinstance(entries, list):
            for entry in entries:
                if entry.startswith("Week") or "KW" in entry:
                    all_week_entries.append(entry)
    
    total_weeks_active = len(set(all_week_entries)) if all_week_entries else 1
    
    # Calculate average waterings per person
    total_waterings = sum(len(watering_history.get(person, [])) for person in PEOPLE)
    avg_waterings = total_waterings / len(PEOPLE) if PEOPLE else 0
    
    # Update regular weights - people who have watered less get higher weights
    for i, person in enumerate(PEOPLE):
        watering_count = len(watering_history.get(person, []))
        experience_level = get_person_experience_level(person)
        
        # Base weight calculation: fewer waterings = higher weight
        if experience_level == "new":
            # New people get high weights to integrate them
            WEIGHTS[i] = 10
        elif experience_level == "beginner":
            # Beginners get high weights to continue integration
            WEIGHTS[i] = 8
        else:
            # Experienced people get weights based on how much they've watered
            # compared to the average
            deviation = watering_count - avg_waterings
            
            # The more you've watered above average, the lower your weight
            if total_weeks_active <= 4:
                WEIGHTS[i] = max(1, min(10, int(8 - deviation * 0.8)))
            elif total_weeks_active <= 26:
                WEIGHTS[i] = max(1, min(10, int(8 - deviation * 0.6)))
            else:
                WEIGHTS[i] = max(1, min(10, int(8 - deviation * 0.4)))
    
    # Update extra weights (for ErsatzPersons) - should be more balanced
    for i, person in enumerate(PEOPLE):
        if i < len(EXTRA_WEIGHTS):
            experience_level = get_person_experience_level(person)
            watering_count = len(watering_history.get(person, []))
            
            if experience_level == "new":
                # New people get lower extra weight to avoid overwhelming
                EXTRA_WEIGHTS[i] = 2
            elif experience_level == "beginner":
                # Beginners get moderate extra weight
                EXTRA_WEIGHTS[i] = 3
            else:
                # Experienced people get extra weights based on their activity
                # People who have watered less get higher extra weights
                deviation = watering_count - avg_waterings
                EXTRA_WEIGHTS[i] = max(1, min(5, int(4 - deviation * 0.3)))
    
    # Ensure EXTRA_WEIGHTS has same length as PEOPLE
    while len(EXTRA_WEIGHTS) < len(PEOPLE):
        EXTRA_WEIGHTS.append(3)  # Default extra weight
    
    # Normalize weights if they become too extreme
    normalize_extreme_weights()
    
    save_to_file()

# Excel functions removed - using JSON-only data storage

def normalize_extreme_weights():
    """Normalize weights if they become too extreme to maintain system balance"""
    if not PEOPLE:
        return
    
    # Check if weights are too extreme
    max_weight = max(WEIGHTS)
    min_weight = min(WEIGHTS)
    weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
    
    # If weight ratio is too high, normalize
    if weight_ratio > 10:  # If max weight is more than 10x min weight
        # Calculate average weight
        avg_weight = sum(WEIGHTS) / len(WEIGHTS)
        
        # Normalize weights towards average while preserving relative differences
        for i in range(len(WEIGHTS)):
            # Reduce extreme weights towards average
            if WEIGHTS[i] > avg_weight * 2:
                WEIGHTS[i] = max(1, int(avg_weight * 1.5 + (WEIGHTS[i] - avg_weight * 2) * 0.5))
            elif WEIGHTS[i] < avg_weight * 0.5:
                WEIGHTS[i] = max(1, int(avg_weight * 0.7 + (WEIGHTS[i] - avg_weight * 0.5) * 0.5))
    
    # Same for extra weights
    if EXTRA_WEIGHTS:
        max_extra_weight = max(EXTRA_WEIGHTS)
        min_extra_weight = min(EXTRA_WEIGHTS)
        extra_weight_ratio = max_extra_weight / min_extra_weight if min_extra_weight > 0 else float('inf')
        
        if extra_weight_ratio > 8:  # Extra weights should be less extreme
            avg_extra_weight = sum(EXTRA_WEIGHTS) / len(EXTRA_WEIGHTS)
            
            for i in range(len(EXTRA_WEIGHTS)):
                if EXTRA_WEIGHTS[i] > avg_extra_weight * 2:
                    EXTRA_WEIGHTS[i] = max(1, int(avg_extra_weight * 1.3 + (EXTRA_WEIGHTS[i] - avg_extra_weight * 2) * 0.4))
                elif EXTRA_WEIGHTS[i] < avg_extra_weight * 0.5:
                    EXTRA_WEIGHTS[i] = max(1, int(avg_extra_weight * 0.8 + (EXTRA_WEIGHTS[i] - avg_extra_weight * 0.5) * 0.4))

def refresh_dependencies():
    for person in PEOPLE:
        if person not in watering_history:
            watering_history[person] = []
    for person in list(watering_history.keys()):
        if person not in PEOPLE:
            del watering_history[person]
    
    # Clean up experience overrides for removed people
    for person in list(experience_overrides.keys()):
        if person not in PEOPLE:
            del experience_overrides[person]
    
    # Ensure EXTRA_WEIGHTS has correct length
    while len(EXTRA_WEIGHTS) < len(PEOPLE):
        EXTRA_WEIGHTS.append(3)
    while len(EXTRA_WEIGHTS) > len(PEOPLE):
        EXTRA_WEIGHTS.pop()
    
    update_weights()
    normalize_extreme_weights()
    save_to_file()

def add_new_person_with_context(name, join_week=None):
    """Add a new person with balanced weight - newcomer friendly approach"""
    if name in PEOPLE:
        return False
    
    # New people get balanced, standard weights - no overwhelming catch-up
    # They should integrate naturally without being penalized for missing past weeks
    initial_weight = 5  # Standard balanced weight
    initial_extra_weight = 2  # Lower extra weight to avoid overwhelming newcomers
    
    PEOPLE.append(name)
    WEIGHTS.append(initial_weight)
    EXTRA_WEIGHTS.append(initial_extra_weight)
    watering_history[name] = []
    
    # Update all weights to maintain system balance
    update_weights()
    save_to_file()
    return True

def remove_person_and_rebalance(name):
    """Remove a person and rebalance the system"""
    if name not in PEOPLE:
        return False
    
    # Store the person's watering history before removal
    leaving_person_waterings = len(watering_history.get(name, []))
    
    # Calculate total weeks and expected waterings for system balance
    all_week_entries = []
    for entries in watering_history.values():
        if isinstance(entries, list):
            for entry in entries:
                if entry.startswith("Week") or "KW" in entry:
                    all_week_entries.append(entry)
    
    total_weeks_active = len(set(all_week_entries)) if all_week_entries else 1
    
    # Remove the person
    index = PEOPLE.index(name)
    PEOPLE.pop(index)
    WEIGHTS.pop(index)
    if index < len(EXTRA_WEIGHTS):
        EXTRA_WEIGHTS.pop(index)
    watering_history.pop(name, None)
    experience_overrides.pop(name, None)  # Remove experience override if it exists
    
    # Recalculate weights based on new system balance
    # The system should naturally rebalance through the normal weight update process
    update_weights()
    save_to_file()
    return True

def get_week_data(year, week):
    """Find the two people assigned for a given year and week."""
    target_file = f"people_{year}.json"
    if os.path.exists(target_file):
        with open(target_file, "r") as file:
            data = json.load(file)
        wh = data.get("WATERING_HISTORY", {})
        week_str = f"{year} KW {week}:"
        for entries in wh.values():
            for entry in entries:
                if entry.startswith(week_str):
                    # Example entry: "2025 KW 30: Jan and Jeff"
                    try:
                        people_part = entry.split(":")[1].strip()
                        person1, _, person2 = people_part.partition(" and ")
                        return [person1.strip(), person2.strip()]
                    except Exception:
                        continue
    return ["", ""]

def get_week_data_with_ersatz(year, week):
    """Find all four people assigned for a given year and week (main persons and ErsatzPersons)."""
    target_file = f"people_{year}.json"
    if os.path.exists(target_file):
        with open(target_file, "r") as file:
            data = json.load(file)
        wh = data.get("WATERING_HISTORY", {})
        week_str = f"{year} KW {week}:"
        for entries in wh.values():
            for entry in entries:
                if entry.startswith(week_str):
                    # Example entry: "2025 KW 30: Jan and Jeff (ErsatzPersons: Rosa and Alexander)"
                    try:
                        # Split the entry to get main part and ersatz part
                        if "(ErsatzPersons:" in entry:
                            main_part = entry.split("(ErsatzPersons:")[0].strip()
                            ersatz_part = entry.split("(ErsatzPersons:")[1].strip().rstrip(")")
                            
                            # Extract main persons
                            people_part = main_part.split(":")[1].strip()
                            person1, _, person2 = people_part.partition(" and ")
                            
                            # Extract ersatz persons
                            ersatz_person1, _, ersatz_person2 = ersatz_part.partition(" and ")
                            
                            return [person1.strip(), person2.strip(), ersatz_person1.strip(), ersatz_person2.strip()]
                        else:
                            # Old format without ErsatzPersons
                            people_part = entry.split(":")[1].strip()
                            person1, _, person2 = people_part.partition(" and ")
                            return [person1.strip(), person2.strip(), "", ""]
                    except Exception:
                        continue
    return ["", "", "", ""]

def update_week_data(year, week, person1, person2):
    """Update data for a specific week in a given year."""
    global watering_history, FILE_PATH
    
    target_file = f"people_{year}.json"
    if os.path.exists(target_file):
        with open(target_file, "r") as file:
            data = json.load(file)
    else:
        # Create a new file with the expected structure
        data = {
            "PEOPLE": PEOPLE.copy(),
            "WEIGHTS": WEIGHTS.copy(),
            "WATERING_HISTORY": {person: [] for person in PEOPLE}
        }

    # Get the watering history
    watering_history_data = data.get("WATERING_HISTORY", {})
    
    # Create the week entry
    week_entry = f"{year} KW {week}: {person1} and {person2}"
    
    # Remove any existing entries for this week
    week_str = f"{year} KW {week}:"
    for person in watering_history_data:
        if isinstance(watering_history_data[person], list):
            watering_history_data[person] = [entry for entry in watering_history_data[person] if not entry.startswith(week_str)]
    
    # Add the new entry to both people's history
    if person1 not in watering_history_data:
        watering_history_data[person1] = []
    if person2 not in watering_history_data:
        watering_history_data[person2] = []
    
    watering_history_data[person1].append(week_entry)
    watering_history_data[person2].append(week_entry)
    
    # Update the data structure
    data["WATERING_HISTORY"] = watering_history_data

    # Save back to the file
    with open(target_file, "w") as file:
        json.dump(data, file, indent=2)
    
    # If we're updating the current file, also update global variables
    if target_file == FILE_PATH:
        watering_history.clear()
        watering_history.update(watering_history_data)

def update_week_data_with_ersatz(year, week, person1, person2, ersatz_person1="", ersatz_person2=""):
    """Update data for a specific week in a given year, including ErsatzPersons."""
    global watering_history, FILE_PATH
    
    target_file = f"people_{year}.json"
    if os.path.exists(target_file):
        with open(target_file, "r") as file:
            data = json.load(file)
    else:
        # Create a new file with the expected structure
        data = {
            "PEOPLE": PEOPLE.copy(),
            "WEIGHTS": WEIGHTS.copy(),
            "EXTRA_WEIGHTS": EXTRA_WEIGHTS.copy(),
            "WATERING_HISTORY": {person: [] for person in PEOPLE}
        }

    # Get the watering history
    watering_history_data = data.get("WATERING_HISTORY", {})
    
    # Create the week entry with ErsatzPersons if provided
    if ersatz_person1 or ersatz_person2:
        week_entry = f"{year} KW {week}: {person1} and {person2} (ErsatzPersons: {ersatz_person1} and {ersatz_person2})"
    else:
        week_entry = f"{year} KW {week}: {person1} and {person2}"
    
    # Remove any existing entries for this week
    week_str = f"{year} KW {week}:"
    for person in watering_history_data:
        if isinstance(watering_history_data[person], list):
            watering_history_data[person] = [entry for entry in watering_history_data[person] if not entry.startswith(week_str)]
    
    # Add the new entry to all people's history (main persons and ErsatzPersons)
    people_to_update = [person1, person2]
    if ersatz_person1:
        people_to_update.append(ersatz_person1)
    if ersatz_person2:
        people_to_update.append(ersatz_person2)
    
    for person in people_to_update:
        if person not in watering_history_data:
            watering_history_data[person] = []
        watering_history_data[person].append(week_entry)
    
    # Update the data structure
    data["WATERING_HISTORY"] = watering_history_data

    # Save back to the file
    with open(target_file, "w") as file:
        json.dump(data, file, indent=2)
    
    # If we're updating the current file, also update global variables
    if target_file == FILE_PATH:
        watering_history.clear()
        watering_history.update(watering_history_data)

def analyze_watering_imbalance():
    """Analyze the watering history to identify imbalances and their causes"""
    if not PEOPLE:
        return None
    
    # Calculate watering counts
    counts = {}
    for person in PEOPLE:
        counts[person] = len(watering_history.get(person, []))
    
    total_waterings = sum(counts.values())
    average = total_waterings / len(PEOPLE)
    
    # Find people who are significantly under/over the average
    under_average = []
    over_average = []
    
    for person, count in counts.items():
        if count < average - 3:  # More than 3 below average
            under_average.append((person, count))
        elif count > average + 3:  # More than 3 above average
            over_average.append((person, count))
    
    # Sort by count
    under_average.sort(key=lambda x: x[1])
    over_average.sort(key=lambda x: x[1], reverse=True)
    
    analysis = {
        'total_waterings': total_waterings,
        'average': average,
        'counts': counts,
        'under_average': under_average,
        'over_average': over_average,
        'min_count': min(counts.values()),
        'max_count': max(counts.values()),
        'difference': max(counts.values()) - min(counts.values())
    }
    
    return analysis

def balance_watering_history(target_range=2):
    """Balance the watering history by redistributing entries"""
    analysis = analyze_watering_imbalance()
    if not analysis:
        return False, "No people data available"
    
    if analysis['difference'] <= target_range:
        return False, f"Watering counts are already balanced (difference: {analysis['difference']})"
    
    # Calculate target counts
    total_waterings = analysis['total_waterings']
    num_people = len(PEOPLE)
    base_count = total_waterings // num_people
    extra_count = total_waterings % num_people
    
    # Determine target counts for each person
    target_counts = {}
    for i, person in enumerate(PEOPLE):
        target_counts[person] = base_count + (1 if i < extra_count else 0)
    
    # Create a copy of watering history to modify
    new_history = {}
    for person in PEOPLE:
        new_history[person] = watering_history.get(person, []).copy()
    
    # Collect all entries to redistribute
    all_entries = []
    for person in PEOPLE:
        for entry in new_history[person]:
            all_entries.append(entry)
    
    # Clear all histories
    for person in PEOPLE:
        new_history[person] = []
    
    # Redistribute entries based on target counts
    person_index = 0
    for entry in all_entries:
        # Find the person with the lowest current count who hasn't reached their target
        candidates = []
        for person in PEOPLE:
            current_count = len(new_history[person])
            if current_count < target_counts[person]:
                candidates.append((person, current_count))
        
        if candidates:
            # Sort by current count (lowest first)
            candidates.sort(key=lambda x: x[1])
            chosen_person = candidates[0][0]
            new_history[chosen_person].append(entry)
    
    # Update global watering history
    watering_history.clear()
    watering_history.update(new_history)
    
    # Save to file
    save_to_file()
    
    # Update weights
    update_weights()
    
    return True, f"Successfully balanced watering history. New range: {max(len(h) for h in new_history.values()) - min(len(h) for h in new_history.values())}"

def get_watering_history_report():
    """Generate a detailed report of watering history"""
    analysis = analyze_watering_imbalance()
    if not analysis:
        return "No data available"
    
    report = []
    report.append("=== WATERING HISTORY ANALYSIS ===")
    report.append(f"Total waterings recorded: {analysis['total_waterings']}")
    report.append(f"Average per person: {analysis['average']:.1f}")
    report.append(f"Range: {analysis['min_count']} - {analysis['max_count']} (difference: {analysis['difference']})")
    report.append("")
    
    report.append("Current distribution:")
    for person in PEOPLE:
        count = analysis['counts'][person]
        diff = count - analysis['average']
        status = ""
        if diff > 3:
            status = " (HIGH)"
        elif diff < -3:
            status = " (LOW)"
        report.append(f"  {person}: {count} waterings ({diff:+.1f}){status}")
    
    if analysis['under_average']:
        report.append("")
        report.append("People significantly under average:")
        for person, count in analysis['under_average']:
            report.append(f"  {person}: {count} waterings")
    
    if analysis['over_average']:
        report.append("")
        report.append("People significantly over average:")
        for person, count in analysis['over_average']:
            report.append(f"  {person}: {count} waterings")
    
    return "\n".join(report)