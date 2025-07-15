import tkinter as tk
from tkinter import messagebox, ttk
import data
from data import save_to_file, save_to_excel, refresh_dependencies, add_new_person_with_context, remove_person_and_rebalance, reload_current_data, get_available_years, load_year_data, get_current_year
from schedule import show_schedule
import datetime

# Create the GUI
root = tk.Tk()
root.title("Gießplan Generator")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

# Configure style
style = ttk.Style()
style.theme_use('clam')
style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
style.configure('Success.TLabel', foreground='green')
style.configure('Error.TLabel', foreground='red')

# Create main container with tabs
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure grid weights
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)

# Year selection frame
year_frame = ttk.LabelFrame(main_frame, text="Year Selection", padding="10")
year_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
year_frame.columnconfigure(1, weight=1)

# Year selection widgets
ttk.Label(year_frame, text="Select Year:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

year_var = tk.StringVar()
year_combobox = ttk.Combobox(year_frame, textvariable=year_var, state="readonly", width=10)
year_combobox.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))

def refresh_years():
    """Refresh the list of available years"""
    available_years = get_available_years()
    year_combobox['values'] = available_years
    current_year = get_current_year()
    if current_year in available_years:
        year_var.set(current_year)
    update_status()

def on_year_changed(event=None):
    """Handle year selection change"""
    selected_year = int(year_var.get())
    if load_year_data(selected_year):
        update_all_displays()
        update_status()
        messagebox.showinfo("Success", f"Switched to year {selected_year}")
    else:
        messagebox.showerror("Error", f"Failed to load data for year {selected_year}")

year_combobox.bind('<<ComboboxSelected>>', on_year_changed)

# Refresh years button
refresh_years_btn = ttk.Button(year_frame, text="Refresh Years", command=refresh_years)
refresh_years_btn.grid(row=0, column=2, padx=(10, 0))

# Current year info
current_year_label = ttk.Label(year_frame, text="", font=('Arial', 10, 'italic'))
current_year_label.grid(row=0, column=3, padx=(20, 0))

# Status bar
status_var = tk.StringVar()
status_bar = ttk.Label(main_frame, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 10))

def update_status():
    """Update the status bar with current information"""
    current_year = get_current_year()
    status_var.set(f"Current file: {data.FILE_PATH} | Year: {current_year} | People: {len(data.PEOPLE)}")
    current_year_label.config(text=f"Working on: {current_year}")

# Create notebook for tabs
notebook = ttk.Notebook(main_frame)
notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

# Update status bar
def update_status():
    current_file = data.FILE_PATH.split('\\')[-1]
    current_year = datetime.date.today().year
    status_var.set(f"Current file: {current_file} | Year: {current_year} | People: {len(data.PEOPLE)}")

# Title
title_label = ttk.Label(main_frame, text="Gießplan Generator", style='Title.TLabel')
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Tab 1: People Management
people_frame = ttk.Frame(notebook, padding="10")
notebook.add(people_frame, text="👥 People Management")

# Left side - Add/Remove people
people_left = ttk.Frame(people_frame)
people_left.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

ttk.Label(people_left, text="Manage People", style='Heading.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))

ttk.Label(people_left, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
name_entry = ttk.Entry(people_left, width=20)
name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))

# Buttons frame
button_frame = ttk.Frame(people_left)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

add_button = ttk.Button(button_frame, text="➕ Add Person", command=lambda: add_person())
add_button.grid(row=0, column=0, padx=(0, 5))

delete_button = ttk.Button(button_frame, text="➖ Remove Person", command=lambda: delete_person())
delete_button.grid(row=0, column=1, padx=(5, 0))

# Right side - People list with details
people_right = ttk.Frame(people_frame)
people_right.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(people_right, text="Current People & Statistics", style='Heading.TLabel').grid(row=0, column=0, pady=(0, 10))

# Create treeview for people list
people_tree = ttk.Treeview(people_right, columns=('Name', 'Watering Count', 'Weight'), show='headings', height=10)
people_tree.heading('Name', text='Name')
people_tree.heading('Watering Count', text='Times Watered')
people_tree.heading('Weight', text='Current Weight')
people_tree.column('Name', width=150)
people_tree.column('Watering Count', width=100)
people_tree.column('Weight', width=100)
people_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Scrollbar for treeview
people_scrollbar = ttk.Scrollbar(people_right, orient=tk.VERTICAL, command=people_tree.yview)
people_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
people_tree.configure(yscrollcommand=people_scrollbar.set)

# Configure grid weights for people frame
people_frame.columnconfigure(0, weight=1)
people_frame.columnconfigure(1, weight=2)
people_frame.rowconfigure(0, weight=1)
people_left.columnconfigure(1, weight=1)
people_right.columnconfigure(0, weight=1)
people_right.rowconfigure(1, weight=1)

def add_person():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return
    
    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name should contain only letters.")
        return
        
    if name in data.PEOPLE:
        messagebox.showerror("Error", "Person already exists.")
        return
        
    if add_new_person_with_context(name):
        update_people_list()
        refresh_dependencies()
        name_entry.delete(0, tk.END)
        update_status()
        messagebox.showinfo("Success", f"Added {name} with context-appropriate weight.")
    else:
        messagebox.showerror("Error", "Failed to add person.")

def delete_person():
    name = name_entry.get().strip()
    if not name:
        # Try to get selection from treeview
        selection = people_tree.selection()
        if selection:
            name = people_tree.item(selection[0])['values'][0]
        else:
            messagebox.showerror("Error", "Please enter a name or select from the list.")
            return
    
    if name not in data.PEOPLE:
        messagebox.showerror("Error", "Person not found.")
        return
        
    # Confirmation dialog
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove {name}?"):
        if remove_person_and_rebalance(name):
            update_people_list()
            refresh_dependencies()
            name_entry.delete(0, tk.END)
            update_status()
            messagebox.showinfo("Success", f"Removed {name} and rebalanced system.")
        else:
            messagebox.showerror("Error", "Failed to remove person.")

def update_people_list():
    # Clear existing items
    for item in people_tree.get_children():
        people_tree.delete(item)
    
    # Ensure watering history is up to date
    for person in data.PEOPLE:
        if person not in data.watering_history:
            data.watering_history[person] = []
    for person in list(data.watering_history.keys()):
        if person not in data.PEOPLE:
            del data.watering_history[person]
    
    # Add people to treeview
    for i, person in enumerate(data.PEOPLE):
        watering_count = len(data.watering_history.get(person, []))
        weight = data.WEIGHTS[i] if i < len(data.WEIGHTS) else 1
        people_tree.insert('', 'end', values=(person, watering_count, weight))

# Tab 2: Schedule Generation
schedule_frame = ttk.Frame(notebook, padding="10")
notebook.add(schedule_frame, text="📅 Schedule Generation")

# Schedule generation section
schedule_gen_frame = ttk.LabelFrame(schedule_frame, text="Generate New Schedule", padding="10")
schedule_gen_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

# Schedule controls frame
schedule_controls = ttk.Frame(schedule_gen_frame)
schedule_controls.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

ttk.Label(schedule_controls, text="Schedule Options:").grid(row=0, column=0, padx=(0, 10))

# Dropdown for schedule type
schedule_type_var = tk.StringVar(value="Complete Year")
schedule_type_combo = ttk.Combobox(schedule_controls, textvariable=schedule_type_var, 
                                  values=["Complete Year", "Next 6 Weeks", "Remaining Weeks"], 
                                  state="readonly", width=15)
schedule_type_combo.grid(row=0, column=1, padx=(0, 10))

generate_button = ttk.Button(schedule_controls, text="🔄 Generate Schedule", command=lambda: generate_and_show_schedule())
generate_button.grid(row=0, column=2, padx=(10, 0))

refresh_button = ttk.Button(schedule_controls, text="🔄 Refresh Display", command=lambda: update_schedule_display())
refresh_button.grid(row=0, column=3, padx=(5, 0))

# Schedule display
schedule_display_frame = ttk.LabelFrame(schedule_frame, text="Current Schedule", padding="10")
schedule_display_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

# Create a frame to hold both the treeview and a visual calendar-like display
schedule_container = ttk.Frame(schedule_display_frame)
schedule_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Treeview for schedule display
schedule_tree = ttk.Treeview(schedule_container, columns=('Week', 'Date Range', 'Person 1', 'Person 2'), show='headings', height=10)
schedule_tree.heading('Week', text='Week')
schedule_tree.heading('Date Range', text='Date Range')
schedule_tree.heading('Person 1', text='Person 1')
schedule_tree.heading('Person 2', text='Person 2')
schedule_tree.column('Week', width=60)
schedule_tree.column('Date Range', width=120)
schedule_tree.column('Person 1', width=120)
schedule_tree.column('Person 2', width=120)
schedule_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

# Configure alternating row colors
schedule_tree.tag_configure('oddrow', background='#f0f0f0')
schedule_tree.tag_configure('evenrow', background='white')
schedule_tree.tag_configure('current_week', background='#e6f3ff', foreground='#0066cc')
schedule_tree.tag_configure('next_week', background='#fff2e6', foreground='#cc6600')

# Scrollbar for schedule treeview
schedule_tree_scrollbar = ttk.Scrollbar(schedule_container, orient=tk.VERTICAL, command=schedule_tree.yview)
schedule_tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
schedule_tree.configure(yscrollcommand=schedule_tree_scrollbar.set)

# Visual schedule summary frame
schedule_summary_frame = ttk.Frame(schedule_container)
schedule_summary_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

# Summary labels
summary_title = ttk.Label(schedule_summary_frame, text="Schedule Summary", style='Heading.TLabel')
summary_title.grid(row=0, column=0, pady=(0, 10))

# Create a canvas for visual schedule representation
schedule_canvas = tk.Canvas(schedule_summary_frame, width=300, height=400, bg='white', relief=tk.RIDGE, bd=1)
schedule_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Canvas scrollbar
canvas_scrollbar = ttk.Scrollbar(schedule_summary_frame, orient=tk.VERTICAL, command=schedule_canvas.yview)
canvas_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
schedule_canvas.configure(yscrollcommand=canvas_scrollbar.set)

# Configure grid weights for schedule display
schedule_display_frame.columnconfigure(0, weight=1)
schedule_display_frame.rowconfigure(0, weight=1)
schedule_container.columnconfigure(0, weight=2)
schedule_container.columnconfigure(2, weight=1)
schedule_container.rowconfigure(0, weight=1)
schedule_summary_frame.columnconfigure(0, weight=1)
schedule_summary_frame.rowconfigure(1, weight=1)

# Configure grid weights for schedule frame
schedule_frame.columnconfigure(0, weight=1)
schedule_frame.rowconfigure(1, weight=1)
schedule_display_frame.columnconfigure(0, weight=1)
schedule_display_frame.rowconfigure(0, weight=1)

def update_schedule_display():
    """Update the schedule display with current data"""
    import datetime
    import calendar
    
    # Clear existing items
    for item in schedule_tree.get_children():
        schedule_tree.delete(item)
    
    # Clear canvas
    schedule_canvas.delete("all")
    
    # Get current year from the selected data
    current_year = datetime.date.today().year
    if hasattr(data, 'FILE_PATH') and 'people_' in data.FILE_PATH:
        import re
        match = re.search(r'people_(\d{4})\.json', data.FILE_PATH)
        if match:
            current_year = int(match.group(1))
    
    # Collect all schedule entries from watering history
    schedule_entries = []
    week_assignments = {}  # week_number: [person1, person2]
    
    for person in data.PEOPLE:
        if person in data.watering_history:
            for entry in data.watering_history[person]:
                if entry.startswith("Week "):
                    try:
                        week_part = entry.split(":")[0]
                        week_num = int(week_part.split()[1])
                        
                        if week_num not in week_assignments:
                            week_assignments[week_num] = []
                        
                        if person not in week_assignments[week_num]:
                            week_assignments[week_num].append(person)
                    except (ValueError, IndexError):
                        continue
    
    # Sort weeks and create display entries
    sorted_weeks = sorted(week_assignments.keys())
    current_week = datetime.date.today().isocalendar()[1]
    
    canvas_y = 10
    for i, week_num in enumerate(sorted_weeks):
        # Calculate date range for the week
        try:
            jan_1 = datetime.date(current_year, 1, 1)
            week_start = jan_1 + datetime.timedelta(weeks=week_num-1)
            week_start = week_start - datetime.timedelta(days=week_start.weekday())
            week_end = week_start + datetime.timedelta(days=6)
            date_range = f"{week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}"
        except:
            date_range = "TBD"
        
        # Get people assigned to this week
        people = week_assignments[week_num]
        person1 = people[0] if len(people) > 0 else ""
        person2 = people[1] if len(people) > 1 else ""
        
        # Determine row styling
        if week_num == current_week:
            tag = 'current_week'
        elif week_num == current_week + 1:
            tag = 'next_week'
        else:
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
        
        # Insert into treeview
        schedule_tree.insert('', 'end', values=(f"Week {week_num}", date_range, person1, person2), tags=(tag,))
        
        # Draw on canvas
        color = '#e6f3ff' if week_num == current_week else '#fff2e6' if week_num == current_week + 1 else '#f8f8f8'
        
        # Week block
        schedule_canvas.create_rectangle(10, canvas_y, 280, canvas_y + 40, fill=color, outline='gray')
        
        # Week number
        schedule_canvas.create_text(25, canvas_y + 20, text=f"W{week_num}", font=('Arial', 10, 'bold'), anchor='w')
        
        # Date range
        schedule_canvas.create_text(60, canvas_y + 20, text=date_range, font=('Arial', 9), anchor='w')
        
        # People assigned
        if person1 and person2:
            schedule_canvas.create_text(150, canvas_y + 20, text=f"{person1} & {person2}", font=('Arial', 9), anchor='w')
        elif person1:
            schedule_canvas.create_text(150, canvas_y + 20, text=person1, font=('Arial', 9), anchor='w')
        
        # Current week indicator
        if week_num == current_week:
            schedule_canvas.create_text(270, canvas_y + 20, text="◄ NOW", font=('Arial', 8, 'bold'), fill='blue', anchor='e')
        elif week_num == current_week + 1:
            schedule_canvas.create_text(270, canvas_y + 20, text="◄ NEXT", font=('Arial', 8, 'bold'), fill='orange', anchor='e')
        
        canvas_y += 45
    
    # Update scroll region
    schedule_canvas.configure(scrollregion=schedule_canvas.bbox("all"))
    
    # Add summary statistics
    total_weeks = len(sorted_weeks)
    weeks_remaining = len([w for w in sorted_weeks if w >= current_week])
    
    # Update title with statistics
    summary_title.config(text=f"Schedule Summary\n({total_weeks} weeks total, {weeks_remaining} remaining)")
    
    # If no schedule exists, show message
    if not sorted_weeks:
        schedule_canvas.create_text(150, 50, text="No schedule data available\nClick 'Generate Schedule' to create", 
                                  font=('Arial', 12), anchor='center', fill='gray')

def generate_complete_year_schedule():
    """Generate a complete year schedule instead of just 6 weeks"""
    import datetime
    from schedule import generate_schedule, select_people_weighted_mean
    
    # Get current year and week
    current_year = datetime.date.today().year
    current_week = datetime.date.today().isocalendar()[1]
    
    # Determine which year we're working with
    if hasattr(data, 'FILE_PATH') and 'people_' in data.FILE_PATH:
        import re
        match = re.search(r'people_(\d{4})\.json', data.FILE_PATH)
        if match:
            current_year = int(match.group(1))
    
    # Find the last week in existing schedule
    existing_weeks = []
    for person in data.watering_history.values():
        if isinstance(person, list):
            for entry in person:
                if entry.startswith("Week "):
                    try:
                        week_num = int(entry.split(":")[0].split()[1])
                        existing_weeks.append(week_num)
                    except:
                        continue
    
    # Determine starting week
    if existing_weeks:
        start_week = max(existing_weeks) + 1
    else:
        start_week = current_week
    
    # Generate schedule for remaining weeks in the year
    selection_count = {person: len(data.watering_history.get(person, [])) for person in data.PEOPLE}
    new_schedule = []
    
    for week in range(start_week, 53):  # Go to end of year
        # Use the same selection algorithm as the original
        selected = select_people_weighted_mean(selection_count)
        
        if len(selected) >= 2:
            # Update selection count
            for person in selected:
                selection_count[person] += 1
                data.watering_history[person].append(f"Week {week}")
            
            week_entry = f"Week {week}: {selected[0]} and {selected[1]}"
            new_schedule.append(week_entry)
    
    # Save the updated data
    data.save_to_file()
    
    # Save to Excel
    if new_schedule:
        data.save_new_weeks_to_excel(new_schedule, data.PEOPLE, data.watering_history, target_year=current_year)
    
    return new_schedule

def generate_and_show_schedule():
    try:
        schedule_type = schedule_type_var.get()
        
        if schedule_type == "Complete Year":
            new_schedule = generate_complete_year_schedule()
            if new_schedule:
                messagebox.showinfo("Success", f"Generated {len(new_schedule)} weeks of schedule for complete year")
            else:
                messagebox.showinfo("Info", "Year schedule is already complete")
        else:
            # Use original 6-week generation
            from schedule import generate_schedule
            new_schedule = generate_schedule()
            if new_schedule:
                messagebox.showinfo("Success", f"Generated {len(new_schedule)} weeks of schedule")
        
        # Update all displays
        update_schedule_display()
        update_people_list()
        update_person_combos()
        update_status()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate schedule: {str(e)}")

# Import the select_people_weighted_mean function if it doesn't exist
try:
    from schedule import select_people_weighted_mean
except ImportError:
    def select_people_weighted_mean(selection_count):
        # Simple fallback selection method
        import random
        available_people = [p for p in data.PEOPLE if selection_count.get(p, 0) < 10]
        if len(available_people) < 2:
            available_people = data.PEOPLE
        return random.sample(available_people, min(2, len(available_people)))
    for item in schedule_tree.get_children():
        schedule_tree.delete(item)
    
    # Clear canvas
    schedule_canvas.delete("all")
    
    # Get current week
    current_week = datetime.date.today().isocalendar()[1]
    current_year = datetime.date.today().year
    
    # Collect all schedule entries
    schedule_entries = []
    for person in data.PEOPLE:
        for entry in data.watering_history.get(person, []):
            if entry.startswith("Week"):
                parts = entry.split(": ")
                if len(parts) == 2:
                    week_part = parts[0]
                    people_part = parts[1]
                    week_num = int(week_part.split()[1])
                    if " and " in people_part:
                        person1, person2 = people_part.split(" and ")
                        schedule_entries.append((week_num, person1.strip(), person2.strip()))
    
    # Remove duplicates and sort by week
    unique_entries = list(set(schedule_entries))
    unique_entries.sort(key=lambda x: x[0])
    
    # Add entries to treeview
    for i, (week_num, person1, person2) in enumerate(unique_entries):
        # Calculate date range for the week
        try:
            # Get Monday of the week
            year = current_year
            if week_num > 52:  # Handle year overflow
                year += 1
                week_num = week_num - 52
            
            jan_1 = datetime.date(year, 1, 1)
            week_start = jan_1 + datetime.timedelta(weeks=week_num-1)
            week_start = week_start - datetime.timedelta(days=week_start.weekday())
            week_end = week_start + datetime.timedelta(days=6)
            
            date_range = f"{week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}"
        except:
            date_range = "TBD"
        
        # Determine row style
        if week_num == current_week:
            tag = 'current_week'
        elif week_num == current_week + 1:
            tag = 'next_week'
        elif i % 2 == 0:
            tag = 'evenrow'
        else:
            tag = 'oddrow'
        
        schedule_tree.insert('', 'end', values=(f"Week {week_num}", date_range, person1, person2), tags=(tag,))
    
    # Update canvas visualization
    draw_schedule_visualization(unique_entries, current_week)

def draw_schedule_visualization(entries, current_week):
    """Draw a visual representation of the schedule on the canvas"""
    canvas_width = 280
    canvas_height = max(400, len(entries) * 60 + 50)
    
    # Update canvas scroll region
    schedule_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
    
    # Colors for people (we'll cycle through these)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6', '#c4e17f']
    person_colors = {}
    
    # Assign colors to people
    color_index = 0
    for person in data.PEOPLE:
        person_colors[person] = colors[color_index % len(colors)]
        color_index += 1
    
    # Draw title
    schedule_canvas.create_text(canvas_width//2, 20, text="Visual Schedule", font=('Arial', 14, 'bold'))
    
    # Draw week blocks
    y_offset = 50
    block_height = 50
    block_width = 260
    
    for week_num, person1, person2 in entries:
        # Determine block color based on week status
        if week_num == current_week:
            border_color = '#0066cc'
            border_width = 3
        elif week_num == current_week + 1:
            border_color = '#cc6600'
            border_width = 2
        else:
            border_color = '#cccccc'
            border_width = 1
        
        # Draw main block
        schedule_canvas.create_rectangle(10, y_offset, 10 + block_width, y_offset + block_height, 
                                       outline=border_color, width=border_width, fill='white')
        
        # Draw week number
        schedule_canvas.create_text(30, y_offset + 15, text=f"Week {week_num}", 
                                  font=('Arial', 10, 'bold'), anchor='w')
        
        # Draw person 1 section
        person1_color = person_colors.get(person1, '#cccccc')
        schedule_canvas.create_rectangle(15, y_offset + 25, 135, y_offset + 45, 
                                       fill=person1_color, outline='black', width=1)
        schedule_canvas.create_text(75, y_offset + 35, text=person1, 
                                  font=('Arial', 9), anchor='center')
        
        # Draw person 2 section
        person2_color = person_colors.get(person2, '#cccccc')
        schedule_canvas.create_rectangle(140, y_offset + 25, 260, y_offset + 45, 
                                       fill=person2_color, outline='black', width=1)
        schedule_canvas.create_text(200, y_offset + 35, text=person2, 
                                  font=('Arial', 9), anchor='center')
        
        y_offset += block_height + 10
    
    # Draw legend
    legend_y = y_offset + 20
    schedule_canvas.create_text(15, legend_y, text="Legend:", font=('Arial', 10, 'bold'), anchor='w')
    
    # Current week indicator
    schedule_canvas.create_rectangle(15, legend_y + 15, 25, legend_y + 25, 
                                   outline='#0066cc', width=3, fill='white')
    schedule_canvas.create_text(30, legend_y + 20, text="Current Week", 
                              font=('Arial', 9), anchor='w')
    
    # Next week indicator
    schedule_canvas.create_rectangle(15, legend_y + 35, 25, legend_y + 45, 
                                   outline='#cc6600', width=2, fill='white')
    schedule_canvas.create_text(30, legend_y + 40, text="Next Week", 
                              font=('Arial', 9), anchor='w')

# Tab 3: Manual Schedule Management
manual_frame = ttk.Frame(notebook, padding="10")
notebook.add(manual_frame, text="✏️ Manual Management")

# Manual date/week management
manual_mgmt_frame = ttk.LabelFrame(manual_frame, text="Add/Remove Specific Dates or Weeks", padding="10")
manual_mgmt_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

ttk.Label(manual_mgmt_frame, text="Date/Week:").grid(row=0, column=0, sticky=tk.W, pady=2)
date_entry = ttk.Entry(manual_mgmt_frame, width=20)
date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))

ttk.Label(manual_mgmt_frame, text="Person 1:").grid(row=1, column=0, sticky=tk.W, pady=2)
person1_var = tk.StringVar()
person1_combo = ttk.Combobox(manual_mgmt_frame, textvariable=person1_var, width=18)
person1_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))

ttk.Label(manual_mgmt_frame, text="Person 2:").grid(row=2, column=0, sticky=tk.W, pady=2)
person2_var = tk.StringVar()
person2_combo = ttk.Combobox(manual_mgmt_frame, textvariable=person2_var, width=18)
person2_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))

manual_button_frame = ttk.Frame(manual_mgmt_frame)
manual_button_frame.grid(row=3, column=0, columnspan=2, pady=10)

add_date_button = ttk.Button(manual_button_frame, text="➕ Add Date/Week", command=lambda: add_date_or_week())
add_date_button.grid(row=0, column=0, padx=(0, 5))

delete_date_button = ttk.Button(manual_button_frame, text="➖ Delete Date/Week", command=lambda: delete_date_or_week())
delete_date_button.grid(row=0, column=1, padx=(5, 0))

# Configure grid weights for manual frame
manual_mgmt_frame.columnconfigure(1, weight=1)

def update_person_combos():
    """Update the combobox options with current people"""
    person1_combo['values'] = data.PEOPLE
    person2_combo['values'] = data.PEOPLE

def add_date_or_week():
    date_or_week = date_entry.get().strip()
    person1 = person1_var.get().strip()
    person2 = person2_var.get().strip()

    if not date_or_week or not person1 or not person2:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    if person1 == person2:
        messagebox.showerror("Error", "Please select two different people.")
        return
        
    if person1 not in data.PEOPLE or person2 not in data.PEOPLE:
        messagebox.showerror("Error", "Please select valid people from the list.")
        return

    if date_or_week.startswith("Week"):
        week_number = date_or_week.split()[1]
        schedule_entry = f"Week {week_number}: {person1} and {person2}"
    else:
        schedule_entry = f"Date {date_or_week}: {person1} and {person2}"

    # Append to watering history
    data.watering_history[person1].append(schedule_entry)
    data.watering_history[person2].append(schedule_entry)

    # Save changes to JSON file
    save_to_file()

    # Save to Excel
    save_to_excel([schedule_entry], data.PEOPLE, data.watering_history, new_year=False)
    
    # Clear entries
    date_entry.delete(0, tk.END)
    person1_var.set("")
    person2_var.set("")
    
    update_people_list()
    update_schedule_display()
    update_status()
    messagebox.showinfo("Success", "Date/Week added successfully.")

def delete_date_or_week():
    date_or_week = date_entry.get().strip()

    if not date_or_week:
        messagebox.showerror("Error", "Please provide a date/week to delete.")
        return
        
    # Count how many entries will be deleted
    entries_to_delete = 0
    for person in data.PEOPLE:
        entries_to_delete += len([entry for entry in data.watering_history[person] if entry.startswith(date_or_week)])
    
    if entries_to_delete == 0:
        messagebox.showinfo("Info", "No matching entries found to delete.")
        return
    
    # Confirmation dialog
    if messagebox.askyesno("Confirm Delete", f"This will delete {entries_to_delete} entries. Continue?"):
        for person in data.PEOPLE:
            data.watering_history[person] = [entry for entry in data.watering_history[person] if not entry.startswith(date_or_week)]

        # Save changes to JSON file
        save_to_file()

        # Save updated history to Excel
        save_to_excel([], data.PEOPLE, data.watering_history, new_year=False)
        
        date_entry.delete(0, tk.END)
        update_people_list()
        update_schedule_display()
        update_status()
        messagebox.showinfo("Success", "Date/Week deleted successfully.")

# Initialize the GUI
def update_all_displays():
    """Update all display elements when data changes"""
    update_people_list()
    update_person_combos()
    update_schedule_display()
    update_status()

def initialize_gui():
    update_all_displays()
    refresh_years()  # Initialize year selection
    
    # Bind double-click on treeview to populate name entry
    def on_tree_double_click(event):
        selection = people_tree.selection()
        if selection:
            name = people_tree.item(selection[0])['values'][0]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, name)
    
    people_tree.bind('<Double-1>', on_tree_double_click)
    
    # Bind Enter key to add person
    def on_enter_key(event):
        add_person()
    
    name_entry.bind('<Return>', on_enter_key)

# Keyboard shortcuts
def setup_keyboard_shortcuts():
    root.bind('<Control-g>', lambda e: generate_and_show_schedule())
    root.bind('<Control-n>', lambda e: name_entry.focus())
    root.bind('<F1>', lambda e: show_help())

def show_help():
    help_text = """
    Gießplan Generator Help
    
    Keyboard Shortcuts:
    • Ctrl+G: Generate schedule
    • Ctrl+N: Focus name entry
    • F1: Show this help
    • Enter: Add person (when name entry is focused)
    
    Usage:
    1. Add people in the People Management tab
    2. Generate schedules in the Schedule Generation tab
    3. Manually manage specific dates in Manual Management tab
    
    Tips:
    • Double-click a person in the list to select them
    • The system automatically balances workload
    • Excel files are saved automatically
    """
    messagebox.showinfo("Help", help_text)

# Initialize everything
initialize_gui()
setup_keyboard_shortcuts()

root.mainloop()
