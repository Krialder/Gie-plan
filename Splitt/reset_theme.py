#!/usr/bin/env python3
"""
Style Reset and Fresh Theme Application
Run this script to apply the modern theme without conflicts
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def reset_and_apply_theme():
    """Reset all styles and apply fresh modern theme"""
    
    print("🔄 Resetting and applying fresh modern theme...")
    
    # Clear any existing GUI modules from cache
    modules_to_clear = [mod for mod in sys.modules.keys() if any(x in mod.lower() for x in ['gui', 'theme', 'tabelle'])]
    for mod in modules_to_clear:
        if mod in sys.modules:
            del sys.modules[mod]
    
    print("✅ Cleared module cache")
    
    # Import fresh modules
    from theme_integration import RKIModernColors
    
    # Create a test to verify our theme works
    root = tk.Tk()
    root.title("🎨 Theme Reset Test")
    root.geometry("800x600")
    
    # FORCE COMPLETE STYLE RESET
    style = ttk.Style()
    
    # Switch between all available themes to clear cache
    for theme_name in style.theme_names():
        try:
            style.theme_use(theme_name)
        except:
            pass
    
    # Set to clam as base
    style.theme_use('clam')
    
    # Get our colors
    colors = RKIModernColors()
    
    # Apply root background
    root.configure(bg=colors.DARK_BACKGROUND)
    
    # MANUALLY CONFIGURE STYLES (bypass any conflicts)
    print("🎨 Manually configuring all styles...")
    
    # Configure button styles manually
    style.configure('Modern.TButton',
                   font=('Segoe UI', 11, 'bold'),
                   background=colors.SOFT_BLUE,
                   foreground=colors.PRIMARY_TEXT,
                   borderwidth=0,
                   focuscolor='none',
                   relief='flat',
                   padding=(16, 8))
    
    style.configure('Modern.Primary.TButton',
                   font=('Segoe UI', 12, 'bold'),
                   background=colors.RED_CROSS_RED,
                   foreground=colors.PRIMARY_TEXT,
                   borderwidth=0,
                   focuscolor='none',
                   relief='flat',
                   padding=(20, 10))
    
    style.configure('Modern.Success.TButton',
                   font=('Segoe UI', 11, 'bold'),
                   background=colors.SUCCESS_GREEN,
                   foreground=colors.PRIMARY_TEXT,
                   borderwidth=0,
                   focuscolor='none',
                   relief='flat',
                   padding=(16, 8))
    
    # Configure label styles
    style.configure('Modern.Title.TLabel',
                   font=('Segoe UI', 24, 'bold'),
                   background=colors.DARK_BACKGROUND,
                   foreground=colors.RED_CROSS_RED)
    
    style.configure('Modern.Heading.TLabel',
                   font=('Segoe UI', 14, 'bold'),
                   background=colors.DARK_BACKGROUND,
                   foreground=colors.RED_CROSS_RED)  # Make headings red too
    
    style.configure('Modern.TLabel',
                   font=('Segoe UI', 11),
                   background=colors.DARK_BACKGROUND,
                   foreground=colors.SECONDARY_TEXT)
    
    # Configure frame styles
    style.configure('Modern.TFrame',
                   background=colors.DARK_BACKGROUND,
                   relief='flat',
                   borderwidth=0)
    
    style.configure('Modern.TLabelframe',
                   font=('Segoe UI', 12, 'bold'),
                   background=colors.CARD_BACKGROUND,
                   foreground=colors.RED_CROSS_RED,
                   borderwidth=1,
                   relief='flat')
    
    # Configure entry styles
    style.configure('Modern.TEntry',
                   font=('Segoe UI', 11),
                   fieldbackground=colors.INPUT_BACKGROUND,
                   background=colors.INPUT_BACKGROUND,
                   foreground=colors.PRIMARY_TEXT,
                   borderwidth=1,
                   relief='flat',
                   insertcolor=colors.PRIMARY_TEXT,
                   padding=(8, 6))
    
    # Configure treeview styles
    style.configure('Modern.Treeview',
                   font=('Segoe UI', 10),
                   background=colors.CARD_BACKGROUND,
                   foreground=colors.SECONDARY_TEXT,
                   fieldbackground=colors.CARD_BACKGROUND,
                   borderwidth=1,
                   relief='flat')
    
    style.configure('Modern.Treeview.Heading',
                   font=('Segoe UI', 11, 'bold'),
                   background=colors.DARKER_BACKGROUND,
                   foreground=colors.PRIMARY_TEXT,
                   relief='flat')
    
    # Configure selection colors
    style.map('Modern.Treeview',
              background=[('selected', colors.SELECTION_BACKGROUND)],
              foreground=[('selected', colors.SELECTION_TEXT)])
    
    print("✅ All styles configured manually")
    
    # Create test UI
    main_frame = ttk.Frame(root, style='Modern.TFrame', padding="20")
    main_frame.pack(fill='both', expand=True)
    
    # Title
    title = ttk.Label(main_frame, text="🌱 Gießplan Generator", style='Modern.Title.TLabel')
    title.pack(pady=(0, 20))
    
    # Heading
    heading = ttk.Label(main_frame, text="👥 People Management", style='Modern.Heading.TLabel')
    heading.pack(pady=(0, 10))
    
    # Regular text
    label = ttk.Label(main_frame, text="This text should be readable (white/light grey)", style='Modern.TLabel')
    label.pack(pady=5)
    
    # Buttons
    button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
    button_frame.pack(pady=10)
    
    ttk.Button(button_frame, text="Primary Action (Red)", style='Modern.Primary.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Standard Button (Soft Blue)", style='Modern.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Success Action (Green)", style='Modern.Success.TButton').pack(side='left', padx=5)
    
    # Entry
    entry_frame = ttk.Frame(main_frame, style='Modern.TFrame')
    entry_frame.pack(pady=10, fill='x')
    
    ttk.Label(entry_frame, text="Test Entry:", style='Modern.TLabel').pack(anchor='w')
    entry = ttk.Entry(entry_frame, style='Modern.TEntry')
    entry.pack(pady=5, fill='x')
    entry.insert(0, "This text should be readable")
    
    # Treeview
    tree_frame = ttk.Frame(main_frame, style='Modern.TFrame')
    tree_frame.pack(pady=10, fill='both', expand=True)
    
    ttk.Label(tree_frame, text="Test Treeview (selection should be readable):", style='Modern.TLabel').pack(anchor='w')
    
    tree = ttk.Treeview(tree_frame, columns=('Name', 'Value'), show='headings', height=6, style='Modern.Treeview')
    tree.heading('Name', text='Name')
    tree.heading('Value', text='Value')
    
    for i in range(5):
        tree.insert('', 'end', values=(f'Person {i+1}', f'Value {i+1}'))
    
    tree.pack(fill='both', expand=True)
    tree.selection_set(tree.get_children()[0])
    
    print("\n📋 THEME TEST CHECKLIST:")
    print("   ❓ Is the title RED?")
    print("   ❓ Is the heading RED?")
    print("   ❓ Are regular labels light grey/white?")
    print("   ❓ Is the Primary button RED?")
    print("   ❓ Is the Standard button SOFT BLUE (not harsh bright blue)?")
    print("   ❓ Is the Success button GREEN?")
    print("   ❓ Is the entry text readable (white on dark)?")
    print("   ❓ Is the selected tree item readable (white text on blue background)?")
    print("   ❓ Is the overall background DARK?")
    print("\n🎯 If all answers are YES, the theme is working correctly!")
    print("💡 Close this window and run 'python main.py' to see the improved application.")
    
    root.mainloop()

if __name__ == "__main__":
    reset_and_apply_theme()
