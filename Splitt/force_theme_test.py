#!/usr/bin/env python3
"""
Force Theme Test - Completely fresh application start
"""

import sys
import os

# Clear any cached modules
modules_to_clear = [mod for mod in sys.modules.keys() if 'theme' in mod or 'gui' in mod]
for mod in modules_to_clear:
    if mod in sys.modules:
        del sys.modules[mod]

# Now import fresh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk

print("🔄 Starting fresh theme test...")

try:
    from theme_integration import apply_rki_theme_to_app, RKIModernColors
    print("✅ Theme integration imported")
    
    # Create fresh window
    root = tk.Tk()
    root.title("🎨 Fresh Theme Test")
    root.geometry("900x700")
    
    print("🎨 Applying modern theme...")
    theme, widgets = apply_rki_theme_to_app(root, modern_theme=True)
    colors = RKIModernColors()
    
    # Add compatibility mappings
    colors.LIGHT_GRAY = colors.CARD_BACKGROUND
    colors.RED_CROSS_WHITE = colors.DARK_BACKGROUND
    colors.PALE_BLUE = colors.SOFT_BLUE
    colors.PROFESSIONAL_BLUE = colors.PRIMARY_TEXT
    colors.LIGHT_ORANGE = colors.WARNING_ORANGE
    colors.WARM_ORANGE = colors.WARNING_ORANGE
    colors.DARK_GRAY = colors.BORDER_COLOR
    colors.MEDIUM_GRAY = colors.SECONDARY_TEXT
    colors.ELECTRIC_BLUE = colors.SOFT_BLUE
    colors.BRIGHT_BLUE = colors.LIGHT_BLUE
    colors.MUTED_BLUE = colors.MUTED_BLUE
    
    print("✅ Modern theme applied")
    
    # Create main container
    main_frame = widgets['frame'](root, padding="15")
    main_frame.pack(fill='both', expand=True)
    
    # Title (should be RED)
    title_label = widgets['title_label'](main_frame, "🌱 Gießplan Generator")
    title_label.pack(pady=(0, 10))
    
    # Create a notebook to mimic the real application
    notebook = widgets['notebook'](main_frame)
    notebook.pack(fill='both', expand=True, pady=(10, 0))
    
    # Tab 1: People Management
    people_frame = widgets['frame'](notebook, padding="15")
    notebook.add(people_frame, text="👥 People Management")
    
    # Left and right sections
    people_left = widgets['frame'](people_frame)
    people_left.pack(side='left', fill='both', expand=True, padx=(0, 15))
    
    people_right = widgets['frame'](people_frame)
    people_right.pack(side='right', fill='both', expand=True)
    
    # Left side - Add/Remove people
    widgets['heading_label'](people_left, text="👤 Manage People").pack(pady=(0, 15))
    
    # Name entry
    name_frame = widgets['frame'](people_left)
    name_frame.pack(fill='x', pady=5)
    widgets['label'](name_frame, text="Name:").pack(side='left')
    name_entry = widgets['entry'](name_frame, width=20)
    name_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    # Buttons
    button_frame = widgets['frame'](people_left)
    button_frame.pack(pady=15)
    
    add_button = widgets['success_button'](button_frame, text="➕ Add Person")
    add_button.pack(side='left', padx=(0, 10))
    
    remove_button = widgets['button'](button_frame, text="➖ Remove Person")
    remove_button.pack(side='left')
    
    # Experience Level Management
    exp_frame = widgets['labelframe'](people_left, text="🎓 Experience Level Management", padding="15")
    exp_frame.pack(fill='x', pady=(15, 0))
    
    # Person dropdown
    person_frame = widgets['frame'](exp_frame)
    person_frame.pack(fill='x', pady=5)
    widgets['label'](person_frame, text="Person:").pack(side='left')
    person_combo = widgets['combobox'](person_frame, values=["Jan", "Jeff", "Antonia", "Melissa", "Rosa", "Alexander"])
    person_combo.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    # Experience level dropdown
    exp_level_frame = widgets['frame'](exp_frame)
    exp_level_frame.pack(fill='x', pady=5)
    widgets['label'](exp_level_frame, text="Experience Level:").pack(side='left')
    exp_combo = widgets['combobox'](exp_level_frame, values=["new", "learning", "experienced"])
    exp_combo.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    # Experience buttons
    exp_button_frame = widgets['frame'](exp_frame)
    exp_button_frame.pack(pady=10)
    
    set_exp_button = widgets['primary_button'](exp_button_frame, text="⚙️ Set Experience Level")
    set_exp_button.pack(side='left', padx=(0, 10))
    
    reset_exp_button = widgets['button'](exp_button_frame, text="🔄 Reset to Automatic")
    reset_exp_button.pack(side='left')
    
    # Right side - Statistics
    widgets['heading_label'](people_right, text="📊 Current People & Statistics").pack(pady=(0, 15))
    
    # Create treeview
    tree = widgets['treeview'](people_right, columns=('Name', 'Times Watered', 'Experience Level', 'Weight', 'Extra Weight'), show='headings', height=10)
    
    # Configure columns
    tree.heading('Name', text='Name')
    tree.heading('Times Watered', text='Times Watered')
    tree.heading('Experience Level', text='Experience Level')
    tree.heading('Weight', text='Weight')
    tree.heading('Extra Weight', text='Extra Weight')
    
    # Add sample data
    sample_data = [
        ("Jan", "9", "experienced", "7", "3"),
        ("Jeff", "8", "learning", "7", "3"),
        ("Antonia", "6", "learning", "9", "4"),
        ("Melissa", "8", "learning", "7", "3"),
        ("Rosa", "8", "learning", "7", "3"),
        ("Alexander", "7", "learning", "8", "4")
    ]
    
    for item in sample_data:
        tree.insert('', 'end', values=item)
    
    tree.pack(fill='both', expand=True, pady=(0, 10))
    
    # Select first item to test selection colors
    if tree.get_children():
        tree.selection_set(tree.get_children()[0])
    
    # Scrollbar
    scrollbar = widgets['scrollbar'](people_right, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    print("✅ Test window created successfully")
    print("\n📋 VISUAL TEST CHECKLIST:")
    print("   ❓ Is the main title RED?")
    print("   ❓ Are the section headings RED?")
    print("   ❓ Are the regular labels WHITE/LIGHT GREY?")
    print("   ❓ Is the 'Add Person' button GREEN?")
    print("   ❓ Is the 'Set Experience Level' button RED?")
    print("   ❓ Is the 'Remove Person' button SOFT BLUE (not harsh)?")
    print("   ❓ Is the selected item in the tree readable (blue background, white text)?")
    print("   ❓ Is the overall background DARK?")
    print("   ❓ Are the input fields dark with white text?")
    print("\n🖥️  If you see harsh bright colors or poor contrast, the theme isn't working!")
    
    root.mainloop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
