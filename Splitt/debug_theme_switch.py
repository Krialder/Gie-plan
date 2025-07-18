#!/usr/bin/env python3
"""
Debug theme switch setup
"""

import tkinter as tk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_theme_switch():
    """Debug the theme switch setup process"""
    
    try:
        # Import required modules
        from theme_integration import apply_rki_theme_to_app
        print("✅ Theme integration import successful")
        
        # Create basic window
        root = tk.Tk()
        root.title("Theme Switch Debug")
        root.geometry("800x200")
        
        # Apply theme
        theme, widgets = apply_rki_theme_to_app(root, modern_theme=True)
        print("✅ Theme applied successfully")
        
        # Create year frame (mimicking the real GUI structure)
        year_frame = widgets['labelframe'](root, text="Year Selection")
        year_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Add some content to match the real layout
        widgets['label'](year_frame, text="Select Year:").grid(row=0, column=0, padx=(10, 5))
        year_var = tk.StringVar(value="2025")
        year_combo = widgets['combobox'](year_frame, textvariable=year_var, values=["2025"])
        year_combo.grid(row=0, column=1, padx=5)
        
        refresh_btn = widgets['small_button'](year_frame, text="🔄 Refresh Years")
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
        
        current_year_label = widgets['label'](year_frame, text="Working on: 2025")
        current_year_label.grid(row=0, column=3, padx=(20, 0))
        
        # Status bar
        status_var = tk.StringVar(value="Current file: people_2025.json | Year: 2025 | People: 0")
        status_bar = widgets['label'](year_frame, textvariable=status_var)
        status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        print("✅ Basic layout created")
        
        # Now add theme switch manually
        theme_var = tk.BooleanVar(value=True)
        
        def toggle_theme():
            print(f"🔄 Theme toggle clicked! Current state: {theme_var.get()}")
            theme_var.set(not theme_var.get())
            print(f"   New state: {theme_var.get()}")
        
        # Create theme switch
        print("🔧 Creating theme switch...")
        theme_frame = widgets['frame'](year_frame)
        theme_frame.grid(row=1, column=3, sticky='w', padx=(20, 0), pady=(5, 0))
        print(f"   Theme frame created and placed at row=1, column=3")
        
        # Moon icon
        moon_label = widgets['label'](theme_frame, text="🌙", font=('Segoe UI', 10))
        moon_label.grid(row=0, column=0, padx=(0, 3))
        print("   Moon icon created")
        
        # Switch container
        switch_frame = widgets['frame'](theme_frame)
        switch_frame.grid(row=0, column=1, padx=2)
        print("   Switch frame created")
        
        # Switch background
        switch_bg = tk.Frame(switch_frame, width=35, height=18, relief='solid', bd=1, bg='gray')
        switch_bg.grid(row=0, column=0)
        switch_bg.grid_propagate(False)
        print("   Switch background created")
        
        # Switch handle
        switch_handle = tk.Button(switch_bg, text="", width=1, height=1, relief='raised', bd=1,
                                 bg='red', command=toggle_theme)
        switch_handle.place(x=2, y=2, width=14, height=14)
        print("   Switch handle created")
        
        # Sun icon
        sun_label = widgets['label'](theme_frame, text="☀️", font=('Segoe UI', 10))
        sun_label.grid(row=0, column=2, padx=(3, 0))
        print("   Sun icon created")
        
        print("✅ Theme switch setup complete!")
        print("🚀 Starting GUI...")
        
        # Start the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_theme_switch()
