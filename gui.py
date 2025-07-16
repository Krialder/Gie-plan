import tkinter as tk
from tkinter import messagebox, ttk
import data
from data import save_to_file, refresh_dependencies, add_new_person_with_context, remove_person_and_rebalance, reload_current_data, get_available_years, load_year_data, get_current_year, get_week_data, get_week_data_with_ersatz, update_week_data, update_week_data_with_ersatz, get_person_experience_level, set_person_experience_level, remove_person_experience_override, get_all_experience_levels, analyze_watering_imbalance, balance_watering_history, get_watering_history_report
from schedule import show_schedule
from tabelle_management import TabelleManager
import datetime
import re

# Try to import theme integration, fallback to basic styling if not available
try:
    from theme_integration import apply_rki_theme_to_app, RKIColors
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

# Create the GUI
root = tk.Tk()
root.title("Gießplan Generator - Rotkreuz-Institut BBW")
root.geometry("900x700")

# Apply theme
if THEME_AVAILABLE:
    # Apply Red Cross Institute theme
    theme, widgets = apply_rki_theme_to_app(root)
    colors = RKIColors()
else:
    # Fallback to basic styling
    theme = None
    root.configure(bg='#f0f0f0')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
    style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
    
    # Create basic widget factory
    widgets = {
        'frame': ttk.Frame,
        'labelframe': ttk.LabelFrame,
        'label': ttk.Label,
        'title_label': lambda parent, text: ttk.Label(parent, text=text, style='Title.TLabel'),
        'heading_label': lambda parent, text: ttk.Label(parent, text=text, style='Heading.TLabel'),
        'button': ttk.Button,
        'primary_button': ttk.Button,
        'success_button': ttk.Button,
        'entry': ttk.Entry,
        'combobox': ttk.Combobox,
        'treeview': ttk.Treeview,
        'notebook': ttk.Notebook,
        'scrollbar': ttk.Scrollbar
    }
    
    # Basic color scheme
    class BasicColors:
        RED_CROSS_WHITE = '#ffffff'
        LIGHT_GRAY = '#f0f0f0'
        DARK_GRAY = '#333333'
        PROFESSIONAL_BLUE = '#0066cc'
        PALE_BLUE = '#e6f3ff'
        WARM_ORANGE = '#ff8800'
        LIGHT_ORANGE = '#ffe6cc'
    
    colors = BasicColors()

# Create main container with tabs
main_frame = widgets['frame'](root, padding="15")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure grid weights
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(3, weight=1)

# Title
title_label = widgets['title_label'](main_frame, text="🌱 Gießplan Generator")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Year selection frame
year_frame = widgets['labelframe'](main_frame, text="📅 Year Selection", padding="10")
year_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
year_frame.columnconfigure(1, weight=1)

# Year selection widgets
widgets['label'](year_frame, text="Select Year:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

year_var = tk.StringVar()
year_combobox = widgets['combobox'](year_frame, textvariable=year_var, state="readonly", width=10)
year_combobox.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))

def refresh_years():
    """Refresh the list of available years"""
    available_years = get_available_years()
    year_combobox['values'] = available_years
    
    # Get the current year being worked on
    current_year = get_current_year()
    
    # Set the combobox to show the current year
    if current_year in available_years:
        year_var.set(current_year)
    elif available_years:
        # If current year not in available years, set to the most recent
        year_var.set(available_years[-1])
    
    update_status()

def on_year_changed(event=None):
    """Handle year selection change"""
    try:
        selected_year = int(year_var.get())
        if load_year_data(selected_year):
            # Update all displays with the new year data
            update_all_displays()
            update_status()
            # Update tabelle manager for new year
            if 'tabelle_manager' in globals():
                tabelle_manager.update_csv_file_path()
                tabelle_manager.update_displays()
            messagebox.showinfo("Success", f"Switched to year {selected_year}")
        else:
            messagebox.showerror("Error", f"No data file found for year {selected_year}")
            # Reset to current year if failed
            refresh_years()
    except ValueError:
        messagebox.showerror("Error", "Invalid year selected")
        refresh_years()

year_combobox.bind('<<ComboboxSelected>>', on_year_changed)

# Refresh years button
refresh_years_btn = widgets['button'](year_frame, text="🔄 Refresh Years", command=refresh_years)
refresh_years_btn.grid(row=0, column=2, padx=(10, 0))

# Current year info
current_year_label = widgets['label'](year_frame, text="")
current_year_label.grid(row=0, column=3, padx=(20, 0))

# Status bar
status_var = tk.StringVar()
status_bar = widgets['label'](main_frame, textvariable=status_var)
status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 10))

def update_status():
    """Update the status bar with current information"""
    current_year = get_current_year()
    current_file = data.FILE_PATH.split('\\')[-1] if '\\' in data.FILE_PATH else data.FILE_PATH
    status_var.set(f"Current file: {current_file} | Year: {current_year} | People: {len(data.PEOPLE)}")
    current_year_label.config(text=f"Working on: {current_year}")

# Create notebook for tabs
notebook = widgets['notebook'](main_frame)
notebook.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

# Initialize Tabelle Manager
tabelle_manager = TabelleManager(main_frame, widgets, colors, theme if THEME_AVAILABLE else None)

# Tab 1: People Management
people_frame = widgets['frame'](notebook, padding="15")
notebook.add(people_frame, text="👥 People Management")

# Left side - Add/Remove people
people_left = widgets['frame'](people_frame)
people_left.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))

widgets['heading_label'](people_left, text="👤 Manage People").grid(row=0, column=0, columnspan=2, pady=(0, 15))

widgets['label'](people_left, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
name_entry = widgets['entry'](people_left, width=20)
name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

# Buttons frame
button_frame = widgets['frame'](people_left)
button_frame.grid(row=2, column=0, columnspan=2, pady=15)

add_button = widgets['success_button'](button_frame, text="➕ Add Person", command=lambda: add_person())
add_button.grid(row=0, column=0, padx=(0, 10))

delete_button = widgets['button'](button_frame, text="➖ Remove Person", command=lambda: delete_person())
delete_button.grid(row=0, column=1, padx=(10, 0))

# Experience Level Management Section
exp_frame = widgets['labelframe'](people_left, text="🎯 Experience Level Management", padding="10")
exp_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))

widgets['label'](exp_frame, text="Person:").grid(row=0, column=0, sticky=tk.W, pady=5)
exp_person_var = tk.StringVar()
exp_person_combo = widgets['combobox'](exp_frame, textvariable=exp_person_var, state="readonly", width=18)
exp_person_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

widgets['label'](exp_frame, text="Experience Level:").grid(row=1, column=0, sticky=tk.W, pady=5)
exp_level_var = tk.StringVar()
exp_level_combo = widgets['combobox'](exp_frame, textvariable=exp_level_var, 
                                      values=["new", "beginner", "learning", "experienced"], 
                                      state="readonly", width=18)
exp_level_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

# Experience level buttons
exp_button_frame = widgets['frame'](exp_frame)
exp_button_frame.grid(row=2, column=0, columnspan=2, pady=10)

set_exp_button = widgets['primary_button'](exp_button_frame, text="🎯 Set Experience Level", command=lambda: set_experience_level())
set_exp_button.grid(row=0, column=0, padx=(0, 10))

remove_exp_button = widgets['button'](exp_button_frame, text="🔄 Reset to Automatic", command=lambda: remove_experience_override())
remove_exp_button.grid(row=0, column=1, padx=(10, 0))

# Configure grid weights for experience frame
exp_frame.columnconfigure(1, weight=1)

# Watering History Balancing Section
balance_frame = widgets['labelframe'](people_left, text="⚖️ Watering History Balancing", padding="10")
balance_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))

# Buttons for balancing
balance_button_frame = widgets['frame'](balance_frame)
balance_button_frame.grid(row=0, column=0, columnspan=2, pady=10)

analyze_button = widgets['button'](balance_button_frame, text="📊 Analyze Imbalance", command=lambda: show_watering_analysis())
analyze_button.grid(row=0, column=0, padx=(0, 10))

balance_button = widgets['primary_button'](balance_button_frame, text="⚖️ Balance History", command=lambda: balance_watering_counts())
balance_button.grid(row=0, column=1, padx=(10, 0))

# Configure grid weights for balance frame
balance_frame.columnconfigure(0, weight=1)
balance_frame.columnconfigure(1, weight=1)

# Right side - People list with details
people_right = widgets['frame'](people_frame)
people_right.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

widgets['heading_label'](people_right, text="📊 Current People & Statistics").grid(row=0, column=0, pady=(0, 15))

# Create treeview for people list
people_tree = widgets['treeview'](people_right, columns=('Name', 'Watering Count', 'Experience Level', 'Weight', 'Extra Weight'), show='headings', height=12)
people_tree.heading('Name', text='Name')
people_tree.heading('Watering Count', text='Times Watered')
people_tree.heading('Experience Level', text='Experience Level')
people_tree.heading('Weight', text='Weight')
people_tree.heading('Extra Weight', text='Extra Weight')
people_tree.column('Name', width=120)
people_tree.column('Watering Count', width=80)
people_tree.column('Experience Level', width=100)
people_tree.column('Weight', width=60)
people_tree.column('Extra Weight', width=70)
people_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Scrollbar for treeview
people_scrollbar = widgets['scrollbar'](people_right, orient=tk.VERTICAL, command=people_tree.yview)
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

def set_experience_level():
    """Set manual experience level for a person"""
    person = exp_person_var.get().strip()
    level = exp_level_var.get().strip()
    
    if not person:
        messagebox.showerror("Error", "Please select a person.")
        return
    
    if not level:
        messagebox.showerror("Error", "Please select an experience level.")
        return
    
    if set_person_experience_level(person, level):
        update_people_list()
        update_status()
        messagebox.showinfo("Success", f"Set {person}'s experience level to '{level}'.")
    else:
        messagebox.showerror("Error", "Failed to set experience level.")

def remove_experience_override():
    """Remove manual experience level override for a person"""
    person = exp_person_var.get().strip()
    
    if not person:
        messagebox.showerror("Error", "Please select a person.")
        return
    
    if remove_person_experience_override(person):
        update_people_list()
        update_status()
        messagebox.showinfo("Success", f"Reset {person}'s experience level to automatic calculation.")
    else:
        messagebox.showinfo("Info", f"No manual override found for {person}.")

def show_watering_analysis():
    """Show detailed analysis of watering history imbalance"""
    try:
        report = get_watering_history_report()
        
        # Create a new window to display the analysis
        analysis_window = tk.Toplevel(root)
        analysis_window.title("Watering History Analysis")
        analysis_window.geometry("600x500")
        
        # Create text widget with scrollbar
        text_frame = widgets['frame'](analysis_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = widgets['scrollbar'](text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert the report
        text_widget.insert(tk.END, report)
        text_widget.configure(state=tk.DISABLED)
        
        # Add buttons
        button_frame = widgets['frame'](analysis_window)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        balance_btn = widgets['primary_button'](button_frame, text="⚖️ Balance Now", 
                                               command=lambda: [balance_watering_counts(), analysis_window.destroy()])
        balance_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        close_btn = widgets['button'](button_frame, text="Close", command=analysis_window.destroy)
        close_btn.pack(side=tk.RIGHT)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate analysis: {str(e)}")

def balance_watering_counts():
    """Balance the watering counts across all people"""
    try:
        # First check if balancing is needed
        analysis = analyze_watering_imbalance()
        if not analysis:
            messagebox.showerror("Error", "No watering data available to balance.")
            return
        
        if analysis['difference'] <= 2:
            messagebox.showinfo("Info", 
                              f"Watering counts are already balanced.\n"
                              f"Current range: {analysis['min_count']} - {analysis['max_count']} (difference: {analysis['difference']})")
            return
        
        # Show confirmation dialog with current imbalance
        confirm_msg = (f"Current watering distribution:\n"
                      f"Range: {analysis['min_count']} - {analysis['max_count']} (difference: {analysis['difference']})\n"
                      f"Average: {analysis['average']:.1f}\n\n"
                      f"This will redistribute watering entries to balance the counts.\n"
                      f"Do you want to proceed?")
        
        if not messagebox.askyesno("Confirm Balancing", confirm_msg):
            return
        
        # Perform the balancing
        success, message = balance_watering_history()
        
        if success:
            # Update all displays
            update_people_list()
            update_schedule_display()
            update_status()
            messagebox.showinfo("Success", f"Watering history balanced successfully!\n\n{message}")
        else:
            messagebox.showinfo("Info", message)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to balance watering history: {str(e)}")

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
    
    # Update weights to ensure they reflect current watering counts
    data.update_weights()
    
    # Add people to treeview
    for i, person in enumerate(data.PEOPLE):
        watering_count = len(data.watering_history.get(person, []))
        experience_level = get_person_experience_level(person)
        # Add indicator for manual override
        if person in data.experience_overrides:
            experience_level += " (Manual)"
        weight = data.WEIGHTS[i] if i < len(data.WEIGHTS) else 1
        extra_weight = data.EXTRA_WEIGHTS[i] if i < len(data.EXTRA_WEIGHTS) else 1
        people_tree.insert('', 'end', values=(person, watering_count, experience_level, weight, extra_weight))
    
    # Update person combos when people list changes
    update_person_combos()

# Tab 2: Schedule Generation
schedule_frame = widgets['frame'](notebook, padding="15")
notebook.add(schedule_frame, text="📅 Schedule Generation")

# Schedule generation section
schedule_gen_frame = widgets['labelframe'](schedule_frame, text="🔄 Generate New Schedule", padding="15")
schedule_gen_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

# Schedule controls frame
schedule_controls = widgets['frame'](schedule_gen_frame)
schedule_controls.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

widgets['label'](schedule_controls, text="Schedule Options:").grid(row=0, column=0, padx=(0, 10))

# Dropdown for schedule type
schedule_type_var = tk.StringVar(value="Next 6 Weeks")
schedule_type_combo = widgets['combobox'](schedule_controls, textvariable=schedule_type_var, 
                                  values=["Next 6 Weeks", "Remaining Weeks"], 
                                  state="readonly", width=15)
schedule_type_combo.grid(row=0, column=1, padx=(0, 15))

generate_button = widgets['primary_button'](schedule_controls, text="🔄 Generate Schedule", command=lambda: generate_and_show_schedule())
generate_button.grid(row=0, column=2, padx=(15, 0))

refresh_button = widgets['button'](schedule_controls, text="🔄 Refresh Display", command=lambda: update_all_displays())
refresh_button.grid(row=0, column=3, padx=(10, 0))

# Schedule display
schedule_display_frame = widgets['labelframe'](schedule_frame, text="📋 Current Schedule", padding="15")
schedule_display_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))

# Create a frame to hold both the treeview and a visual calendar-like display
schedule_container = widgets['frame'](schedule_display_frame)
schedule_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Treeview for schedule display
schedule_tree = widgets['treeview'](schedule_container, columns=('Week', 'Date Range', 'Person 1', 'Person 2', 'ErsatzPerson 1', 'ErsatzPerson 2'), show='headings', height=10)
schedule_tree.heading('Week', text='Week')
schedule_tree.heading('Date Range', text='Date Range')
schedule_tree.heading('Person 1', text='Person 1')
schedule_tree.heading('Person 2', text='Person 2')
schedule_tree.heading('ErsatzPerson 1', text='ErsatzPerson 1')
schedule_tree.heading('ErsatzPerson 2', text='ErsatzPerson 2')
schedule_tree.column('Week', width=60)
schedule_tree.column('Date Range', width=120)
schedule_tree.column('Person 1', width=100)
schedule_tree.column('Person 2', width=100)
schedule_tree.column('ErsatzPerson 1', width=100)
schedule_tree.column('ErsatzPerson 2', width=100)
schedule_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

# Configure alternating row colors with theme colors
schedule_tree.tag_configure('oddrow', background=colors.LIGHT_GRAY)
schedule_tree.tag_configure('evenrow', background=colors.RED_CROSS_WHITE)
schedule_tree.tag_configure('current_week', background=colors.PALE_BLUE, foreground=colors.PROFESSIONAL_BLUE)
schedule_tree.tag_configure('next_week', background=colors.LIGHT_ORANGE, foreground=colors.WARM_ORANGE)

# Scrollbar for schedule treeview
schedule_tree_scrollbar = widgets['scrollbar'](schedule_container, orient=tk.VERTICAL, command=schedule_tree.yview)
schedule_tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
schedule_tree.configure(yscrollcommand=schedule_tree_scrollbar.set)

# Visual schedule summary frame
schedule_summary_frame = widgets['frame'](schedule_container)
schedule_summary_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

# Summary labels
summary_title = widgets['heading_label'](schedule_summary_frame, text="Schedule Summary")
summary_title.grid(row=0, column=0, pady=(0, 10))

# Create a canvas for visual schedule representation
schedule_canvas = tk.Canvas(schedule_summary_frame, width=300, height=400, 
                          bg=colors.RED_CROSS_WHITE, relief=tk.RIDGE, bd=1,
                          highlightbackground=colors.LIGHT_GRAY)
schedule_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Canvas scrollbar
canvas_scrollbar = widgets['scrollbar'](schedule_summary_frame, orient=tk.VERTICAL, command=schedule_canvas.yview)
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

def update_schedule_display():
    """Update the schedule display with current data"""
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
    week_assignments = {}  # week_number: {'main': [person1, person2], 'ersatz': [ersatz1, ersatz2]}
    
    for person in data.PEOPLE:
        if person in data.watering_history:
            for entry in data.watering_history[person]:
                if "KW" in entry:
                    try:
                        # Parse new KW format: "2025 KW 15: person1 and person2 (ErsatzPersons: ersatz1 and ersatz2)"
                        parts = entry.split(":")
                        if len(parts) >= 2:
                            week_part = parts[0].strip()
                            # Extract year and week number
                            if "KW" in week_part:
                                import re
                                match = re.search(r'(\d{4})\s*KW\s*(\d+)', week_part)
                                if match:
                                    year_num = int(match.group(1))
                                    week_num = int(match.group(2))
                                    
                                    # Only show entries for the current year being viewed
                                    if year_num == current_year:
                                        if week_num not in week_assignments:
                                            week_assignments[week_num] = {'main': [], 'ersatz': []}
                                        
                                        # Parse main persons and ersatz persons
                                        if person not in week_assignments[week_num]['main']:
                                            week_assignments[week_num]['main'].append(person)
                                        
                                        # Try to extract ErsatzPersons from the entry
                                        if "ErsatzPersons:" in entry:
                                            ersatz_part = entry.split("ErsatzPersons:")[1].strip()
                                            if " and " in ersatz_part:
                                                ersatz_persons = ersatz_part.rstrip(")").split(" and ")
                                                if len(ersatz_persons) >= 2:
                                                    ersatz1 = ersatz_persons[0].strip()
                                                    ersatz2 = ersatz_persons[1].strip()
                                                    if ersatz1 not in week_assignments[week_num]['ersatz']:
                                                        week_assignments[week_num]['ersatz'].append(ersatz1)
                                                    if ersatz2 not in week_assignments[week_num]['ersatz']:
                                                        week_assignments[week_num]['ersatz'].append(ersatz2)
                    except (ValueError, IndexError):
                        continue
                elif entry.startswith("Week "):  # Support old format for backward compatibility
                    try:
                        week_part = entry.split(":")[0]
                        week_num = int(week_part.split()[1])
                        
                        if week_num not in week_assignments:
                            week_assignments[week_num] = {'main': [], 'ersatz': []}
                        
                        if person not in week_assignments[week_num]['main']:
                            week_assignments[week_num]['main'].append(person)
                    except (ValueError, IndexError):
                        continue
    
    # Sort weeks and create display entries
    sorted_weeks = sorted(week_assignments.keys())
    current_week = datetime.date.today().isocalendar()[1]
    actual_current_year = datetime.date.today().year
    
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
        assignment = week_assignments[week_num]
        main_people = assignment.get('main', [])
        ersatz_people = assignment.get('ersatz', [])
        
        person1 = main_people[0] if len(main_people) > 0 else ""
        person2 = main_people[1] if len(main_people) > 1 else ""
        ersatz_person1 = ersatz_people[0] if len(ersatz_people) > 0 else ""
        ersatz_person2 = ersatz_people[1] if len(ersatz_people) > 1 else ""
        
        # Determine row styling - only highlight current/next week if viewing the actual current year
        if current_year == actual_current_year:
            if week_num == current_week:
                tag = 'current_week'
            elif week_num == current_week + 1:
                tag = 'next_week'
            else:
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
        else:
            # For past or future years, just use alternating row colors
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
        
        # Insert into treeview
        schedule_tree.insert('', 'end', values=(f"KW {week_num}", date_range, person1, person2, ersatz_person1, ersatz_person2), tags=(tag,))
    
    # Draw canvas visualization
    draw_schedule_visualization(sorted_weeks, week_assignments, current_week, current_year, actual_current_year)

def draw_schedule_visualization(sorted_weeks, week_assignments, current_week, current_year, actual_current_year):
    """Draw a visual representation of the schedule on the canvas"""
    canvas_width = 280
    canvas_height = max(400, len(sorted_weeks) * 60 + 100)
    
    # Update canvas scroll region
    schedule_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
    
    # Get theme colors if available
    if THEME_AVAILABLE:
        canvas_colors = theme.get_canvas_colors()
        person_colors = {person: theme.get_person_color(i) for i, person in enumerate(data.PEOPLE)}
    else:
        canvas_colors = {
            'background': '#ffffff',
            'border': '#cccccc',
            'current_week': '#e6f3ff',
            'current_week_border': '#0066cc',
            'next_week': '#ffe6cc',
            'next_week_border': '#ff8800',
            'text': '#333333',
            'title': '#0066cc',
            'legend': '#666666'
        }
        colors_list = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6', '#c4e17f']
        person_colors = {person: colors_list[i % len(colors_list)] for i, person in enumerate(data.PEOPLE)}
    
    # Draw title
    schedule_canvas.create_text(canvas_width//2, 20, text="Visual Schedule", 
                              font=('Segoe UI', 14, 'bold'), fill=canvas_colors['title'])
    
    # Draw week blocks
    y_offset = 50
    block_height = 50
    block_width = 260
    
    for i, week_num in enumerate(sorted_weeks):
        # Determine block color based on week status - only highlight current/next week if viewing the actual current year
        if current_year == actual_current_year:
            if week_num == current_week:
                border_color = canvas_colors['current_week_border']
                border_width = 3
                bg_color = canvas_colors['current_week']
            elif week_num == current_week + 1:
                border_color = canvas_colors['next_week_border']
                border_width = 2
                bg_color = canvas_colors['next_week']
            else:
                border_color = canvas_colors['border']
                border_width = 1
                bg_color = canvas_colors['background']
        else:
            # For past or future years, just use normal styling
            border_color = canvas_colors['border']
            border_width = 1
            bg_color = canvas_colors['background']
        
        # Draw main block
        schedule_canvas.create_rectangle(10, y_offset, 10 + block_width, y_offset + block_height, 
                                       outline=border_color, width=border_width, fill=bg_color)
        
        # Draw week number
        schedule_canvas.create_text(30, y_offset + 15, text=f"Week {week_num}", 
                                  font=('Segoe UI', 10, 'bold'), anchor='w', fill=canvas_colors['text'])
        
        # Get people for this week
        assignment = week_assignments.get(week_num, {'main': [], 'ersatz': []})
        main_people = assignment.get('main', [])
        
        if len(main_people) >= 2:
            person1, person2 = main_people[0], main_people[1]
            
            # Draw person 1 section
            person1_color = person_colors.get(person1, colors.LIGHT_GRAY)
            schedule_canvas.create_rectangle(15, y_offset + 25, 135, y_offset + 45, 
                                           fill=person1_color, outline=colors.DARK_GRAY, width=1)
            schedule_canvas.create_text(75, y_offset + 35, text=person1, 
                                      font=('Segoe UI', 9), anchor='center', fill=canvas_colors['text'])
            
            # Draw person 2 section
            person2_color = person_colors.get(person2, colors.LIGHT_GRAY)
            schedule_canvas.create_rectangle(140, y_offset + 25, 260, y_offset + 45, 
                                           fill=person2_color, outline=colors.DARK_GRAY, width=1)
            schedule_canvas.create_text(200, y_offset + 35, text=person2, 
                                      font=('Segoe UI', 9), anchor='center', fill=canvas_colors['text'])
        
        y_offset += block_height + 10
    
    # Draw legend
    legend_y = y_offset + 20
    schedule_canvas.create_text(15, legend_y, text="Legend:", 
                              font=('Segoe UI', 10, 'bold'), anchor='w', fill=canvas_colors['legend'])
    
    # Current week indicator
    schedule_canvas.create_rectangle(15, legend_y + 15, 25, legend_y + 25, 
                                   outline=canvas_colors['current_week_border'], width=3, 
                                   fill=canvas_colors['current_week'])
    schedule_canvas.create_text(30, legend_y + 20, text="Current Week", 
                              font=('Segoe UI', 9), anchor='w', fill=canvas_colors['text'])
    
    # Next week indicator
    schedule_canvas.create_rectangle(15, legend_y + 35, 25, legend_y + 45, 
                                   outline=canvas_colors['next_week_border'], width=2, 
                                   fill=canvas_colors['next_week'])
    schedule_canvas.create_text(30, legend_y + 40, text="Next Week", 
                              font=('Segoe UI', 9), anchor='w', fill=canvas_colors['text'])

def generate_and_show_schedule():
    try:
        schedule_type = schedule_type_var.get()
        
        # Import the schedule generation function
        from schedule import generate_schedule
        
        # Generate schedule with the selected type
        new_schedule = generate_schedule(schedule_type)
        
        if new_schedule:
            # Extract week information from the generated schedule
            week_info = []
            current_year = None
            week_numbers = []
            
            for entry in new_schedule:
                # Extract year and week number from entries like "2025 KW 48: Jan and Rosa"
                import re
                match = re.search(r'(\d{4}) KW (\d+)', entry)
                if match:
                    year = int(match.group(1))
                    week_num = int(match.group(2))
                    
                    if current_year is None:
                        current_year = year
                        week_numbers = [week_num]
                    elif year == current_year:
                        week_numbers.append(week_num)
                    else:
                        # Year changed, add previous year's info
                        if week_numbers:
                            if len(week_numbers) == 1:
                                week_info.append(f"{current_year}: KW {week_numbers[0]}")
                            else:
                                week_info.append(f"{current_year}: KW {min(week_numbers)}-{max(week_numbers)}")
                        
                        # Start new year
                        current_year = year
                        week_numbers = [week_num]
            
            # Add the last year's info
            if current_year and week_numbers:
                if len(week_numbers) == 1:
                    week_info.append(f"{current_year}: KW {week_numbers[0]}")
                else:
                    week_info.append(f"{current_year}: KW {min(week_numbers)}-{max(week_numbers)}")
            
            # Create success message with week ranges
            success_msg = f"Generate {schedule_type} schedule with {len(new_schedule)} weeks"
            if week_info:
                success_msg += f"\n\nWeeks generated:\n• " + "\n• ".join(week_info)
            
            # Show success message
            messagebox.showinfo("Success", success_msg)
        else:
            messagebox.showinfo("Info", "Schedule generation completed")
        
        # Update all displays - including year selection in case new year files were created
        refresh_years()
        update_schedule_display()
        update_people_list()
        update_status()
        # Update tabelle management displays
        if 'tabelle_manager' in globals():
            tabelle_manager.update_displays()
        
    except PermissionError:
        messagebox.showerror("File Permission Error", 
                           "Cannot access the file - it may be open in another application.\n\n"
                           "Please close any Excel files or other applications using this file and try again.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate schedule: {str(e)}")

# Tab 3: Manual Schedule Management
manual_frame = widgets['frame'](notebook, padding="15")
notebook.add(manual_frame, text="✏️ Manual Management")

# Tab 4: Tabelle Management
tabelle_manager.create_tabelle_tab(notebook)

# Manual date/week management
manual_mgmt_frame = widgets['labelframe'](manual_frame, text="✏️ Add/Remove Specific Dates or Weeks", padding="15")
manual_mgmt_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

# Calendar week and year selection
widgets['label'](manual_mgmt_frame, text="Calendar Week:").grid(row=0, column=0, sticky=tk.W, pady=8)
week_var = tk.StringVar()
week_combo = widgets['combobox'](manual_mgmt_frame, textvariable=week_var, width=10, state="readonly")
week_combo['values'] = [f"KW {i}" for i in range(1, 53)]
week_combo.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(10, 0))

widgets['label'](manual_mgmt_frame, text="Year:").grid(row=0, column=2, sticky=tk.W, pady=8, padx=(20, 0))
manual_year_var = tk.StringVar()
manual_year_combo = widgets['combobox'](manual_mgmt_frame, textvariable=manual_year_var, width=10, state="readonly")
manual_year_combo.grid(row=0, column=3, sticky=tk.W, pady=8, padx=(10, 0))

widgets['label'](manual_mgmt_frame, text="Person 1:").grid(row=1, column=0, sticky=tk.W, pady=8)
person1_var = tk.StringVar()
person1_combo = widgets['combobox'](manual_mgmt_frame, textvariable=person1_var, width=18)
person1_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))

widgets['label'](manual_mgmt_frame, text="Person 2:").grid(row=1, column=2, sticky=tk.W, pady=8, padx=(20, 0))
person2_var = tk.StringVar()
person2_combo = widgets['combobox'](manual_mgmt_frame, textvariable=person2_var, width=18)
person2_combo.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))

# ErsatzPerson (substitute person) fields
widgets['label'](manual_mgmt_frame, text="ErsatzPerson 1:").grid(row=2, column=0, sticky=tk.W, pady=8)
ersatz_person1_var = tk.StringVar()
ersatz_person1_combo = widgets['combobox'](manual_mgmt_frame, textvariable=ersatz_person1_var, width=18)
ersatz_person1_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))

widgets['label'](manual_mgmt_frame, text="ErsatzPerson 2:").grid(row=2, column=2, sticky=tk.W, pady=8, padx=(20, 0))
ersatz_person2_var = tk.StringVar()
ersatz_person2_combo = widgets['combobox'](manual_mgmt_frame, textvariable=ersatz_person2_var, width=18)
ersatz_person2_combo.grid(row=2, column=3, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))

manual_button_frame = widgets['frame'](manual_mgmt_frame)
manual_button_frame.grid(row=3, column=0, columnspan=4, pady=15)

add_date_button = widgets['success_button'](manual_button_frame, text="➕ Add Date/Week", command=lambda: add_date_or_week())
add_date_button.grid(row=0, column=0, padx=(0, 10))

delete_date_button = widgets['button'](manual_button_frame, text="➖ Delete Date/Week", command=lambda: delete_date_or_week())
delete_date_button.grid(row=0, column=1, padx=(10, 0))

# Configure grid weights for manual frame
manual_mgmt_frame.columnconfigure(1, weight=1)
manual_mgmt_frame.columnconfigure(3, weight=1)

def update_person_combos():
    """Update the combobox options with current people"""
    print(f"Updating combos with people: {data.PEOPLE}")
    person1_combo['values'] = data.PEOPLE
    person2_combo['values'] = data.PEOPLE
    ersatz_person1_combo['values'] = data.PEOPLE
    ersatz_person2_combo['values'] = data.PEOPLE
    
    # Update experience level management combo
    exp_person_combo['values'] = data.PEOPLE
    if data.PEOPLE and not exp_person_var.get():
        exp_person_var.set(data.PEOPLE[0])
    
    # Clear any existing selections that might be invalid
    if person1_var.get() not in data.PEOPLE:
        person1_var.set("")
    if person2_var.get() not in data.PEOPLE:
        person2_var.set("")
    if ersatz_person1_var.get() not in data.PEOPLE:
        ersatz_person1_var.set("")
    if ersatz_person2_var.get() not in data.PEOPLE:
        ersatz_person2_var.set("")
    
    # Update manual year combo with available years
    available_years = data.get_available_years()
    manual_year_combo['values'] = available_years
    if available_years:
        manual_year_var.set(available_years[-1])  # Set to latest year

def add_date_or_week():
    week_selection = week_var.get().strip()
    year_selection = manual_year_var.get().strip()

    print(f"Selected Week: {week_selection}, Selected Year: {year_selection}")

    person1 = person1_var.get().strip()
    person2 = person2_var.get().strip()
    ersatz_person1 = ersatz_person1_var.get().strip()
    ersatz_person2 = ersatz_person2_var.get().strip()

    # Clean up person names in case they contain extra text
    # Remove any parentheses and content within them
    import re
    person1 = re.sub(r'\s*\([^)]*\).*', '', person1).strip()
    person2 = re.sub(r'\s*\([^)]*\).*', '', person2).strip()
    ersatz_person1 = re.sub(r'\s*\([^)]*\).*', '', ersatz_person1).strip()
    ersatz_person2 = re.sub(r'\s*\([^)]*\).*', '', ersatz_person2).strip()

    print(f"Cleaned names - Person1: '{person1}', Person2: '{person2}', Ersatz1: '{ersatz_person1}', Ersatz2: '{ersatz_person2}'")
    print(f"Available people: {data.PEOPLE}")

    if not week_selection or not year_selection or not person1 or not person2:
        messagebox.showerror("Error", "Please fill in all main person fields.")
        return

    if person1 == person2:
        messagebox.showerror("Error", "Please select two different main people.")
        return

    if person1 not in data.PEOPLE or person2 not in data.PEOPLE:
        messagebox.showerror("Error", "Please select valid main people from the list.")
        return

    # Check ersatz persons if they are filled
    if ersatz_person1 and ersatz_person1 not in data.PEOPLE:
        messagebox.showerror("Error", "Please select valid ErsatzPerson 1 from the list.")
        return
    
    if ersatz_person2 and ersatz_person2 not in data.PEOPLE:
        messagebox.showerror("Error", "Please select valid ErsatzPerson 2 from the list.")
        return

    if ersatz_person1 and ersatz_person2 and ersatz_person1 == ersatz_person2:
        messagebox.showerror("Error", "Please select two different ErsatzPersons.")
        return

    # Ensure ErsatzPersons are not the same as main persons
    if ersatz_person1 and (ersatz_person1 == person1 or ersatz_person1 == person2):
        messagebox.showerror("Error", "ErsatzPerson 1 cannot be the same as a main person.")
        return
        
    if ersatz_person2 and (ersatz_person2 == person1 or ersatz_person2 == person2):
        messagebox.showerror("Error", "ErsatzPerson 2 cannot be the same as a main person.")
        return

    # Extract week number from KW format (e.g., "KW 15" -> "15")
    week_number = week_selection.replace("KW ", "").strip()

    # Check if week already has existing data
    existing_data = get_week_data_with_ersatz(year_selection, week_number)
    print(f"Existing Data for Week {week_number}: {existing_data}")
    
    # If there's existing data, show confirmation dialog
    if existing_data[0] or existing_data[1]:
        existing_person1 = existing_data[0] or "Unknown"
        existing_person2 = existing_data[1] or "Unknown"
        
        confirmation_message = f"Are you sure you want to change {week_selection} {year_selection} from {existing_person1} and {existing_person2} to {person1} and {person2}?"
        
        if not messagebox.askyesno("Confirm Change", confirmation_message):
            return

    # Update week data with ErsatzPersons
    update_week_data_with_ersatz(year_selection, week_number, person1, person2, ersatz_person1, ersatz_person2)

    # Reload the current data to reflect the changes in the global variables
    reload_current_data()

    # Excel functionality removed - using JSON-only data storage

    # Clear entries
    week_var.set("")
    manual_year_var.set("")
    person1_var.set("")
    person2_var.set("")
    ersatz_person1_var.set("")
    ersatz_person2_var.set("")

    update_people_list()
    update_schedule_display()
    update_status()
    # Update tabelle management displays
    if 'tabelle_manager' in globals():
        tabelle_manager.update_displays()
    
    # Create success message
    success_message = f"Entry for {year_selection} {week_selection} added successfully."
    if ersatz_person1 or ersatz_person2:
        ersatz_info = []
        if ersatz_person1:
            ersatz_info.append(f"ErsatzPerson 1: {ersatz_person1}")
        if ersatz_person2:
            ersatz_info.append(f"ErsatzPerson 2: {ersatz_person2}")
        success_message += f"\nErsatzPersons: {', '.join(ersatz_info)}"
    
    messagebox.showinfo("Success", success_message)

def delete_date_or_week():
    week_selection = week_var.get().strip()
    year_selection = manual_year_var.get().strip()

    if not week_selection or not year_selection:
        messagebox.showerror("Error", "Please select both calendar week and year to delete.")
        return
    
    # Extract week number from KW format
    week_number = week_selection.replace("KW ", "").strip()
    
    # Create search pattern for deletion
    search_pattern = f"{year_selection} {week_selection}:"
        
    # Count how many entries will be deleted
    entries_to_delete = 0
    for person in data.PEOPLE:
        entries_to_delete += len([entry for entry in data.watering_history[person] if entry.startswith(search_pattern)])
    
    if entries_to_delete == 0:
        messagebox.showinfo("Info", f"No matching entries found for {year_selection} {week_selection}.")
        return
    
    # Confirmation dialog
    if messagebox.askyesno("Confirm Delete", f"This will delete {entries_to_delete} entries for {year_selection} {week_selection}. Continue?"):
        for person in data.PEOPLE:
            data.watering_history[person] = [entry for entry in data.watering_history[person] if not entry.startswith(search_pattern)]

        # Save changes to JSON file
        save_to_file()

        # Excel functionality removed - using JSON-only data storage
        
        week_var.set("")
        manual_year_var.set("")
        update_people_list()
        update_schedule_display()
        update_status()
        # Update tabelle management displays
        if 'tabelle_manager' in globals():
            tabelle_manager.update_displays()
        messagebox.showinfo("Success", f"Entry for {year_selection} {week_selection} deleted successfully.")

def get_all_weeks_assignments():
    # Aggregate all week assignments from watering_history
    week_assignments = {}
    for person, entries in data.watering_history.items():
        for entry in entries:
            m = re.match(r"(\d{4} KW \d+): (.+) and (.+)", entry)
            if m:
                week, p1, p2 = m.group(1), m.group(2), m.group(3)
                week_assignments[week] = (p1, p2)
    # Sort by week number
    def week_sort_key(week):
        year, kw = re.match(r"(\d{4}) KW (\d+)", week).groups()
        return (int(year), int(kw))
    return [ (week, week_assignments[week][0], week_assignments[week][1]) 
             for week in sorted(week_assignments, key=week_sort_key) ]

# Initialize the GUI
def update_all_displays():
    """Update all display elements when data changes"""
    reload_current_data()  # Reload data from file to ensure we have the latest
    update_people_list()
    update_person_combos()
    update_schedule_display()
    update_status()
    # Update tabelle management displays
    if 'tabelle_manager' in globals():
        tabelle_manager.update_displays()

def initialize_gui():
    update_all_displays()
    refresh_years()  # Initialize year selection
    
    # Initialize manual management controls
    if 'manual_year_combo' in globals():
        available_years = data.get_available_years()
        manual_year_combo['values'] = available_years
        if available_years:
            manual_year_var.set(available_years[-1])  # Set to latest year
    
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
    • Red Cross Institute themed for professional use
    """
    messagebox.showinfo("Help", help_text)

# Initialize everything
initialize_gui()
setup_keyboard_shortcuts()

# Autofill person1 and person2 when week or year changes
def autofill_persons_for_week(*args):
    week_selection = week_var.get().strip()
    year_selection = manual_year_var.get().strip()
    if week_selection and year_selection:
        week_number = week_selection.replace("KW ", "").strip()
        existing_data = get_week_data_with_ersatz(year_selection, week_number)
        
        # existing_data format: [person1, person2, ersatz_person1, ersatz_person2]
        if existing_data and len(existing_data) >= 4:
            person1_var.set(existing_data[0] or "")
            person2_var.set(existing_data[1] or "")
            ersatz_person1_var.set(existing_data[2] or "")
            ersatz_person2_var.set(existing_data[3] or "")
        else:
            # If no data found, clear all fields
            person1_var.set("")
            person2_var.set("")
            ersatz_person1_var.set("")
            ersatz_person2_var.set("")

# Bind autofill to week and year changes
week_var.trace_add("write", autofill_persons_for_week)
manual_year_var.trace_add("write", autofill_persons_for_week)
week_combo.bind('<<ComboboxSelected>>', lambda e: autofill_persons_for_week())
manual_year_combo.bind('<<ComboboxSelected>>', lambda e: autofill_persons_for_week())

# Initialize combo boxes with current data
update_person_combos()

root.mainloop()
