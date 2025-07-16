import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
import os
import datetime
import re
import data
from data import get_current_year, get_available_years

# Try to import theme integration
try:
    from theme_integration import apply_rki_theme_to_app, RKIColors
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

class TabelleManager:
    def __init__(self, parent, widgets, colors, theme=None):
        self.parent = parent
        self.widgets = widgets
        self.colors = colors
        self.theme = theme
        self.csv_file_path = None
        self.current_csv_data = []
        
        # Initialize CSV file path based on current year
        self.update_csv_file_path()
        
    def update_csv_file_path(self):
        """Update CSV file path based on current year"""
        current_year = get_current_year()
        self.csv_file_path = f"giessplan_{current_year}.csv"
        
    def create_tabelle_tab(self, notebook):
        """Create the Tabelle Management tab"""
        # Create main frame for the tab
        tabelle_frame = self.widgets['frame'](notebook, padding="15")
        notebook.add(tabelle_frame, text="📊 Tabelle Management")
        
        # Configure grid weights
        tabelle_frame.columnconfigure(0, weight=1)
        tabelle_frame.rowconfigure(1, weight=1)
        
        # Title and controls section
        self.create_control_section(tabelle_frame)
        
        # Main content area with two columns
        content_frame = self.widgets['frame'](tabelle_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left column - Expected CSV Structure
        self.create_expected_structure_section(content_frame)
        
        # Right column - Current CSV Content
        self.create_current_csv_section(content_frame)
        
        # Initialize display
        self.update_displays()
        
    def create_control_section(self, parent):
        """Create the control section with buttons and status"""
        control_frame = self.widgets['labelframe'](parent, text="📋 CSV Tabelle Controls", padding="15")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File info and status
        info_frame = self.widgets['frame'](control_frame)
        info_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        info_frame.columnconfigure(1, weight=1)
        
        self.widgets['label'](info_frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.csv_file_label = self.widgets['label'](info_frame, text="")
        self.csv_file_label.grid(row=0, column=1, sticky=tk.W)
        
        self.widgets['label'](info_frame, text="Status:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.status_label = self.widgets['label'](info_frame, text="")
        self.status_label.grid(row=1, column=1, sticky=tk.W)
        
        # Buttons
        button_frame = self.widgets['frame'](control_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Create/Update CSV button
        self.create_csv_btn = self.widgets['primary_button'](button_frame, 
                                                           text="📊 Create/Update CSV Tabelle", 
                                                           command=self.create_update_csv)
        self.create_csv_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Open CSV button
        self.open_csv_btn = self.widgets['button'](button_frame, 
                                                  text="📂 Open CSV File", 
                                                  command=self.open_csv_file)
        self.open_csv_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Refresh button
        self.refresh_btn = self.widgets['button'](button_frame, 
                                                 text="🔄 Refresh", 
                                                 command=self.refresh_displays)
        self.refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Protection info
        protection_frame = self.widgets['frame'](control_frame)
        protection_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0))
        
        protection_text = "ℹ️ Die CSV-Datei ist für Endbenutzer bestimmt und wird automatisch als schreibgeschützt erstellt."
        self.widgets['label'](protection_frame, text=protection_text, 
                             foreground=self.colors.PROFESSIONAL_BLUE if hasattr(self.colors, 'PROFESSIONAL_BLUE') else '#0066cc').grid(row=0, column=0)
        
    def create_expected_structure_section(self, parent):
        """Create the expected CSV structure preview section"""
        expected_frame = self.widgets['labelframe'](parent, text="📋 Expected CSV Structure", padding="15")
        expected_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        expected_frame.columnconfigure(0, weight=1)
        expected_frame.rowconfigure(1, weight=1)
        
        # Description
        desc_text = "This shows how the CSV file will be structured for end users:"
        self.widgets['label'](expected_frame, text=desc_text).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Treeview for expected structure
        self.expected_tree = self.widgets['treeview'](expected_frame, 
                                                     columns=('Kalenderwoche', 'Jahr', 'Datum', 'Person 1', 'Person 2', 'Ersatz 1', 'Ersatz 2', 'Status'), 
                                                     show='headings', height=15)
        
        # Configure columns
        columns = [
            ('Kalenderwoche', 80, 'KW'),
            ('Jahr', 60, 'Year'),
            ('Datum', 120, 'Date Range'),
            ('Person 1', 100, 'Person 1'),
            ('Person 2', 100, 'Person 2'),
            ('Ersatz 1', 100, 'Substitute 1'),
            ('Ersatz 2', 100, 'Substitute 2'),
            ('Status', 80, 'Status')
        ]
        
        for col, width, heading in columns:
            self.expected_tree.heading(col, text=heading)
            self.expected_tree.column(col, width=width)
        
        self.expected_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        expected_scrollbar = self.widgets['scrollbar'](expected_frame, orient=tk.VERTICAL, command=self.expected_tree.yview)
        expected_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.expected_tree.configure(yscrollcommand=expected_scrollbar.set)
        
        # Configure row colors
        self.expected_tree.tag_configure('current', background='#e6f3ff', foreground='#0066cc')
        self.expected_tree.tag_configure('upcoming', background='#ffe6cc', foreground='#ff8800')
        self.expected_tree.tag_configure('past', background='#f5f5f5', foreground='#666666')
        self.expected_tree.tag_configure('future', background='#ffffff', foreground='#333333')
        
    def create_current_csv_section(self, parent):
        """Create the current CSV content section"""
        current_frame = self.widgets['labelframe'](parent, text="📄 Current CSV Content", padding="15")
        current_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        current_frame.columnconfigure(0, weight=1)
        current_frame.rowconfigure(1, weight=1)
        
        # Status info
        self.csv_status_label = self.widgets['label'](current_frame, text="")
        self.csv_status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Treeview for current CSV content
        self.current_tree = self.widgets['treeview'](current_frame, 
                                                    columns=('Kalenderwoche', 'Jahr', 'Datum', 'Person 1', 'Person 2', 'Ersatz 1', 'Ersatz 2', 'Status'), 
                                                    show='headings', height=15)
        
        # Configure columns
        columns = [
            ('Kalenderwoche', 80, 'KW'),
            ('Jahr', 60, 'Year'),
            ('Datum', 120, 'Date Range'),
            ('Person 1', 100, 'Person 1'),
            ('Person 2', 100, 'Person 2'),
            ('Ersatz 1', 100, 'Substitute 1'),
            ('Ersatz 2', 100, 'Substitute 2'),
            ('Status', 80, 'Status')
        ]
        
        for col, width, heading in columns:
            self.current_tree.heading(col, text=heading)
            self.current_tree.column(col, width=width)
        
        self.current_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        current_scrollbar = self.widgets['scrollbar'](current_frame, orient=tk.VERTICAL, command=self.current_tree.yview)
        current_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.current_tree.configure(yscrollcommand=current_scrollbar.set)
        
        # Configure row colors
        self.current_tree.tag_configure('current', background='#e6f3ff', foreground='#0066cc')
        self.current_tree.tag_configure('upcoming', background='#ffe6cc', foreground='#ff8800')
        self.current_tree.tag_configure('past', background='#f5f5f5', foreground='#666666')
        self.current_tree.tag_configure('future', background='#ffffff', foreground='#333333')
        
    def get_schedule_data(self):
        """Extract schedule data from the current data structure"""
        schedule_data = []
        current_year = get_current_year()
        
        # Get all week assignments from watering history
        week_assignments = {}
        
        for person in data.PEOPLE:
            if person in data.watering_history:
                for entry in data.watering_history[person]:
                    if "KW" in entry:
                        try:
                            # Parse KW format: "2025 KW 15: person1 and person2 (ErsatzPersons: ersatz1 and ersatz2)"
                            parts = entry.split(":")
                            if len(parts) >= 2:
                                week_part = parts[0].strip()
                                match = re.search(r'(\d{4})\s*KW\s*(\d+)', week_part)
                                if match:
                                    year_num = int(match.group(1))
                                    week_num = int(match.group(2))
                                    
                                    if week_num not in week_assignments:
                                        week_assignments[week_num] = {
                                            'year': year_num,
                                            'main': [],
                                            'ersatz': []
                                        }
                                    
                                    # Add main person
                                    if person not in week_assignments[week_num]['main']:
                                        week_assignments[week_num]['main'].append(person)
                                    
                                    # Extract ErsatzPersons
                                    if "ErsatzPersons:" in entry:
                                        ersatz_part = entry.split("ErsatzPersons:")[1].strip()
                                        if " and " in ersatz_part:
                                            ersatz_persons = ersatz_part.rstrip(")").split(" and ")
                                            for ersatz in ersatz_persons:
                                                ersatz = ersatz.strip()
                                                if ersatz and ersatz not in week_assignments[week_num]['ersatz']:
                                                    week_assignments[week_num]['ersatz'].append(ersatz)
                        except (ValueError, IndexError):
                            continue
        
        # Convert to schedule data format
        current_week = datetime.date.today().isocalendar()[1]
        current_date = datetime.date.today()
        
        for week_num in sorted(week_assignments.keys()):
            assignment = week_assignments[week_num]
            year = assignment['year']
            
            # Calculate date range
            try:
                jan_1 = datetime.date(year, 1, 1)
                week_start = jan_1 + datetime.timedelta(weeks=week_num-1)
                week_start = week_start - datetime.timedelta(days=week_start.weekday())
                week_end = week_start + datetime.timedelta(days=6)
                date_range = f"{week_start.strftime('%d.%m')} - {week_end.strftime('%d.%m')}"
                
                # Determine status
                if year == current_date.year:
                    if week_num == current_week:
                        status = "Aktuelle Woche"
                    elif week_num == current_week + 1:
                        status = "Nächste Woche"
                    elif week_num < current_week:
                        status = "Vergangen"
                    else:
                        status = "Zukünftig"
                else:
                    status = "Vergangen" if year < current_date.year else "Zukünftig"
                        
            except:
                date_range = "TBD"
                status = "Unbekannt"
            
            # Get persons
            main_people = assignment['main']
            ersatz_people = assignment['ersatz']
            
            person1 = main_people[0] if len(main_people) > 0 else ""
            person2 = main_people[1] if len(main_people) > 1 else ""
            ersatz1 = ersatz_people[0] if len(ersatz_people) > 0 else ""
            ersatz2 = ersatz_people[1] if len(ersatz_people) > 1 else ""
            
            schedule_data.append({
                'week': f"KW {week_num}",
                'year': str(year),
                'date_range': date_range,
                'person1': person1,
                'person2': person2,
                'ersatz1': ersatz1,
                'ersatz2': ersatz2,
                'status': status
            })
        
        return schedule_data
    
    def update_expected_display(self):
        """Update the expected structure display"""
        # Clear existing items
        for item in self.expected_tree.get_children():
            self.expected_tree.delete(item)
        
        # Get schedule data
        schedule_data = self.get_schedule_data()
        
        # Add data to treeview
        for item in schedule_data:
            # Determine tag for styling
            if item['status'] == "Aktuelle Woche":
                tag = 'current'
            elif item['status'] == "Nächste Woche":
                tag = 'upcoming'
            elif item['status'] == "Vergangen":
                tag = 'past'
            else:
                tag = 'future'
            
            self.expected_tree.insert('', 'end', values=(
                item['week'],
                item['year'],
                item['date_range'],
                item['person1'],
                item['person2'],
                item['ersatz1'],
                item['ersatz2'],
                item['status']
            ), tags=(tag,))
    
    def update_current_csv_display(self):
        """Update the current CSV content display"""
        # Clear existing items
        for item in self.current_tree.get_children():
            self.current_tree.delete(item)
        
        # Check if CSV file exists
        if not os.path.exists(self.csv_file_path):
            self.csv_status_label.config(text="📄 No CSV file found - Create one using the button above")
            return
        
        # Try to read current CSV file
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8-sig', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                if not rows:
                    self.csv_status_label.config(text="📄 CSV file is empty")
                    return
                
                self.csv_status_label.config(text=f"📄 CSV file loaded - {len(rows)} entries")
                
                # Add data to treeview
                for row in rows:
                    # Determine tag for styling
                    status = row.get('Status', '')
                    if status == "Aktuelle Woche":
                        tag = 'current'
                    elif status == "Nächste Woche":
                        tag = 'upcoming'
                    elif status == "Vergangen":
                        tag = 'past'
                    else:
                        tag = 'future'
                    
                    self.current_tree.insert('', 'end', values=(
                        row.get('Kalenderwoche', ''),
                        row.get('Jahr', ''),
                        row.get('Datum', ''),
                        row.get('Person 1', ''),
                        row.get('Person 2', ''),
                        row.get('Ersatz 1', ''),
                        row.get('Ersatz 2', ''),
                        status
                    ), tags=(tag,))
                    
        except Exception as e:
            self.csv_status_label.config(text=f"❌ Error reading CSV file: {str(e)}")
    
    def create_update_csv(self):
        """Create or update the CSV file"""
        try:
            # Get schedule data
            schedule_data = self.get_schedule_data()
            
            if not schedule_data:
                messagebox.showwarning("No Data", "No schedule data available to export to CSV.")
                return
            
            # Create CSV file
            with open(self.csv_file_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
                fieldnames = ['Kalenderwoche', 'Jahr', 'Datum', 'Person 1', 'Person 2', 'Ersatz 1', 'Ersatz 2', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data
                for item in schedule_data:
                    writer.writerow({
                        'Kalenderwoche': item['week'],
                        'Jahr': item['year'],
                        'Datum': item['date_range'],
                        'Person 1': item['person1'],
                        'Person 2': item['person2'],
                        'Ersatz 1': item['ersatz1'],
                        'Ersatz 2': item['ersatz2'],
                        'Status': item['status']
                    })
            
            # Make file read-only for users
            try:
                import stat
                os.chmod(self.csv_file_path, stat.S_IREAD)
            except:
                pass  # If we can't set read-only, continue anyway
            
            # Update displays
            self.update_displays()
            
            messagebox.showinfo("Success", 
                              f"CSV Tabelle successfully created/updated!\n\n"
                              f"File: {self.csv_file_path}\n"
                              f"Entries: {len(schedule_data)}\n"
                              f"File is set to read-only for end users.")
            
        except PermissionError:
            messagebox.showerror("Permission Error", 
                               "Cannot write to CSV file - it may be open in another application.\n\n"
                               "Please close Excel or other applications using this file and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create/update CSV file: {str(e)}")
    
    def open_csv_file(self):
        """Open the CSV file in the default application"""
        if not os.path.exists(self.csv_file_path):
            messagebox.showwarning("File Not Found", 
                                 f"CSV file not found: {self.csv_file_path}\n\n"
                                 "Please create it first using the 'Create/Update CSV Tabelle' button.")
            return
        
        try:
            os.startfile(self.csv_file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CSV file: {str(e)}")
    
    def refresh_displays(self):
        """Refresh both displays"""
        self.update_csv_file_path()
        self.update_displays()
    
    def update_displays(self):
        """Update all displays"""
        self.update_expected_display()
        self.update_current_csv_display()
        self.update_status_labels()
    
    def update_status_labels(self):
        """Update status labels"""
        self.csv_file_label.config(text=self.csv_file_path)
        
        if os.path.exists(self.csv_file_path):
            try:
                stat_info = os.stat(self.csv_file_path)
                file_size = stat_info.st_size
                mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime)
                
                # Check if file is read-only
                is_readonly = not (stat_info.st_mode & 0o200)
                readonly_text = " (Read-only)" if is_readonly else ""
                
                status_text = f"File exists - {file_size} bytes, modified: {mod_time.strftime('%Y-%m-%d %H:%M')}{readonly_text}"
                self.status_label.config(text=status_text)
            except:
                self.status_label.config(text="File exists")
        else:
            self.status_label.config(text="File not found - Create using button above")
