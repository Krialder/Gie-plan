#!/usr/bin/env python3
"""
Test script to verify the improved theme
"""

import tkinter as tk
from tkinter import ttk

try:
    from theme_integration import apply_rki_theme_to_app, RKIModernColors
    print("✅ Theme integration imported successfully")
    
    # Create test window
    root = tk.Tk()
    root.title("Theme Test")
    root.geometry("800x600")
    
    # Apply modern theme
    theme, widgets = apply_rki_theme_to_app(root, modern_theme=True)
    colors = RKIModernColors()
    print("✅ Modern theme applied successfully")
    
    # Test widgets
    main_frame = widgets['frame'](root, padding="20")
    main_frame.pack(fill='both', expand=True)
    
    # Title (should be red)
    title = widgets['title_label'](main_frame, "🌱 Gießplan Generator - Modern Theme")
    title.pack(pady=(0, 20))
    
    # Heading (should be red)
    heading = widgets['heading_label'](main_frame, "People Management")
    heading.pack(pady=(0, 10))
    
    # Regular text (should be white/light)
    label = widgets['label'](main_frame, "This text should be readable")
    label.pack(pady=5)
    
    # Buttons (softer colors)
    button_frame = widgets['frame'](main_frame)
    button_frame.pack(pady=10)
    
    # Red button for important actions
    widgets['primary_button'](button_frame, "Primary Action (Red)", command=lambda: print("Primary clicked")).pack(side='left', padx=5)
    
    # Softer blue button
    widgets['button'](button_frame, "Standard Button (Soft Blue)", command=lambda: print("Standard clicked")).pack(side='left', padx=5)
    
    # Green button
    widgets['success_button'](button_frame, "Success Action (Green)", command=lambda: print("Success clicked")).pack(side='left', padx=5)
    
    # Entry
    entry_frame = widgets['frame'](main_frame)
    entry_frame.pack(pady=10, fill='x')
    
    widgets['label'](entry_frame, "Test Entry:").pack(anchor='w')
    entry = widgets['entry'](entry_frame, width=30)
    entry.pack(pady=5, fill='x')
    entry.insert(0, "Test text - should be readable")
    
    # Treeview with selection test
    tree_frame = widgets['frame'](main_frame)
    tree_frame.pack(pady=10, fill='both', expand=True)
    
    widgets['label'](tree_frame, "Test Treeview (selection should be readable):").pack(anchor='w')
    
    tree = widgets['treeview'](tree_frame, columns=('Name', 'Value'), show='headings', height=6)
    tree.heading('Name', text='Name')
    tree.heading('Value', text='Value')
    tree.column('Name', width=200)
    tree.column('Value', width=200)
    
    # Add test data
    for i in range(5):
        tree.insert('', 'end', values=(f'Person {i+1}', f'Value {i+1}'))
    
    tree.pack(fill='both', expand=True)
    
    # Select first item to test selection colors
    tree.selection_set(tree.get_children()[0])
    
    print("✅ Theme test window created successfully")
    print("📋 Test checklist:")
    print("   - Title should be RED")
    print("   - Heading should be RED") 
    print("   - Regular text should be WHITE/LIGHT")
    print("   - Primary button should be RED")
    print("   - Standard button should be SOFT BLUE (not harsh)")
    print("   - Success button should be GREEN")
    print("   - Entry text should be readable")
    print("   - Selected treeview item should have good contrast")
    
    root.mainloop()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
