"""
Theme Integration for Rotkreuz-Institut Berufsbildungswerk
Red Cross Institute Vocational Training colors and styling

This module provides color schemes and styling configurations
specifically designed for the Red Cross Institute environment.
"""

import tkinter as tk
from tkinter import ttk

# Red Cross Institute Color Palette
class RKIColors:
    """Color palette inspired by Red Cross Institute branding"""
    
    # Primary Red Cross colors
    RED_CROSS_RED = "#DC143C"
    RED_CROSS_WHITE = "#FFFFFF"
    
    # Professional blues for education/trust
    PROFESSIONAL_BLUE = "#1E3A8A"
    LIGHT_BLUE = "#3B82F6"
    PALE_BLUE = "#E6F3FF"
    
    # Supporting colors
    EDUCATION_GREEN = "#059669"
    LIGHT_GREEN = "#10B981"
    PALE_GREEN = "#ECFDF5"
    
    # Neutral colors
    DARK_GRAY = "#374151"
    MEDIUM_GRAY = "#6B7280"
    LIGHT_GRAY = "#F3F4F6"
    BACKGROUND_GRAY = "#F9FAFB"
    
    # Accent colors
    WARM_ORANGE = "#EA580C"
    LIGHT_ORANGE = "#FED7AA"
    SUCCESS_GREEN = "#16A34A"
    WARNING_YELLOW = "#EAB308"
    ERROR_RED = "#DC2626"

class RKITheme:
    """Theme configuration for Red Cross Institute styling"""
    
    def __init__(self, root):
        self.root = root
        self.colors = RKIColors()
        self.style = ttk.Style()
        
    def apply_theme(self):
        """Apply the complete Red Cross Institute theme"""
        self._configure_root()
        self._configure_ttk_styles()
        self._configure_canvas_styles()
        
    def _configure_root(self):
        """Configure the main window"""
        self.root.configure(bg=self.colors.BACKGROUND_GRAY)
        
    def _configure_ttk_styles(self):
        """Configure TTK widget styles"""
        
        # Use a modern theme as base
        try:
            self.style.theme_use('clam')
        except:
            self.style.theme_use('default')
        
        # Configure main frame style
        self.style.configure('RKI.TFrame', 
                           background=self.colors.BACKGROUND_GRAY,
                           relief='flat',
                           borderwidth=0)
        
        # Configure title label
        self.style.configure('RKI.Title.TLabel',
                           font=('Segoe UI', 20, 'bold'),
                           background=self.colors.BACKGROUND_GRAY,
                           foreground=self.colors.RED_CROSS_RED)
        
        # Configure heading labels
        self.style.configure('RKI.Heading.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           background=self.colors.BACKGROUND_GRAY,
                           foreground=self.colors.PROFESSIONAL_BLUE)
        
        # Configure regular labels
        self.style.configure('RKI.TLabel',
                           font=('Segoe UI', 10),
                           background=self.colors.BACKGROUND_GRAY,
                           foreground=self.colors.DARK_GRAY)
        
        # Configure status labels
        self.style.configure('RKI.Status.TLabel',
                           font=('Segoe UI', 9),
                           background=self.colors.LIGHT_GRAY,
                           foreground=self.colors.MEDIUM_GRAY,
                           relief='sunken',
                           padding=(5, 2))
        
        # Configure buttons
        self.style.configure('RKI.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.PROFESSIONAL_BLUE,
                           foreground=self.colors.RED_CROSS_WHITE,
                           borderwidth=0,
                           focuscolor='none',
                           padding=(10, 5))
        
        self.style.map('RKI.TButton',
                      background=[('active', self.colors.LIGHT_BLUE),
                                ('pressed', self.colors.PROFESSIONAL_BLUE)])
        
        # Configure primary action buttons
        self.style.configure('RKI.Primary.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.colors.RED_CROSS_RED,
                           foreground=self.colors.RED_CROSS_WHITE,
                           borderwidth=0,
                           focuscolor='none',
                           padding=(12, 8))
        
        self.style.map('RKI.Primary.TButton',
                      background=[('active', '#B22222'),
                                ('pressed', self.colors.RED_CROSS_RED)])
        
        # Configure success buttons
        self.style.configure('RKI.Success.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.SUCCESS_GREEN,
                           foreground=self.colors.RED_CROSS_WHITE,
                           borderwidth=0,
                           focuscolor='none',
                           padding=(10, 5))
        
        self.style.map('RKI.Success.TButton',
                      background=[('active', '#15803D'),    # Darker green on hover
                                ('pressed', '#22C55E')])     # Lighter green when pressed
        
        # Configure notebook tabs
        self.style.configure('RKI.TNotebook',
                           background=self.colors.BACKGROUND_GRAY,
                           borderwidth=0)
        
        self.style.configure('RKI.TNotebook.Tab',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.LIGHT_GRAY,
                           foreground=self.colors.DARK_GRAY,
                           padding=(20, 10),
                           borderwidth=0)
        
        self.style.map('RKI.TNotebook.Tab',
                      background=[('selected', self.colors.PALE_BLUE),
                                ('active', self.colors.LIGHT_BLUE)],
                      foreground=[('selected', self.colors.PROFESSIONAL_BLUE),
                                ('active', self.colors.RED_CROSS_WHITE)])
        
        # Configure entries
        self.style.configure('RKI.TEntry',
                           font=('Segoe UI', 10),
                           fieldbackground=self.colors.RED_CROSS_WHITE,
                           borderwidth=1,
                           relief='solid',
                           padding=(5, 3))
        
        self.style.map('RKI.TEntry',
                      bordercolor=[('focus', self.colors.PROFESSIONAL_BLUE)])
        
        # Configure comboboxes
        self.style.configure('RKI.TCombobox',
                           font=('Segoe UI', 10),
                           fieldbackground=self.colors.RED_CROSS_WHITE,
                           borderwidth=1,
                           relief='solid',
                           padding=(5, 3))
        
        # Configure labelframes
        self.style.configure('RKI.TLabelframe',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.BACKGROUND_GRAY,
                           foreground=self.colors.PROFESSIONAL_BLUE,
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('RKI.TLabelframe.Label',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.BACKGROUND_GRAY,
                           foreground=self.colors.PROFESSIONAL_BLUE)
        
        # Configure treeview
        self.style.configure('RKI.Treeview',
                           font=('Segoe UI', 10),
                           background=self.colors.RED_CROSS_WHITE,
                           foreground=self.colors.DARK_GRAY,
                           fieldbackground=self.colors.RED_CROSS_WHITE,
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('RKI.Treeview.Heading',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.PALE_BLUE,
                           foreground=self.colors.PROFESSIONAL_BLUE,
                           borderwidth=1,
                           relief='solid')
        
        # Configure scrollbars
        self.style.configure('RKI.Vertical.TScrollbar',
                           background=self.colors.LIGHT_GRAY,
                           troughcolor=self.colors.BACKGROUND_GRAY,
                           borderwidth=0,
                           arrowcolor=self.colors.PROFESSIONAL_BLUE)
        
    def _configure_canvas_styles(self):
        """Configure canvas color schemes for visual elements"""
        self.canvas_colors = {
            'background': self.colors.RED_CROSS_WHITE,
            'border': self.colors.LIGHT_GRAY,
            'current_week': self.colors.PALE_BLUE,
            'current_week_border': self.colors.PROFESSIONAL_BLUE,
            'next_week': self.colors.LIGHT_ORANGE,
            'next_week_border': self.colors.WARM_ORANGE,
            'text': self.colors.DARK_GRAY,
            'title': self.colors.PROFESSIONAL_BLUE,
            'legend': self.colors.MEDIUM_GRAY
        }
        
        # Person color palette for schedule visualization
        self.person_colors = [
            self.colors.PALE_BLUE,    # Light blue
            self.colors.PALE_GREEN,   # Light green
            '#FFE5E5',                # Light pink
            '#FFF0E5',                # Light peach
            '#E5F0FF',                # Very light blue
            '#F0FFE5',                # Very light green
            '#FFE5F0',                # Light lavender
            '#E5FFFF',                # Light cyan
            '#FFFFE5',                # Light yellow
            '#F0E5FF'                 # Light purple
        ]
    
    def get_person_color(self, person_index):
        """Get a color for a person based on their index"""
        return self.person_colors[person_index % len(self.person_colors)]
    
    def get_canvas_colors(self):
        """Get canvas color scheme"""
        return self.canvas_colors

def create_styled_widgets():
    """Factory functions for creating styled widgets"""
    
    def create_title_label(parent, text="", **kwargs):
        return ttk.Label(parent, text=text, style='RKI.Title.TLabel', **kwargs)
    
    def create_heading_label(parent, text="", **kwargs):
        return ttk.Label(parent, text=text, style='RKI.Heading.TLabel', **kwargs)
    
    def create_label(parent, text="", **kwargs):
        # Extract textvariable if present
        textvariable = kwargs.pop('textvariable', None)
        if textvariable:
            return ttk.Label(parent, text=text, textvariable=textvariable, style='RKI.TLabel', **kwargs)
        else:
            return ttk.Label(parent, text=text, style='RKI.TLabel', **kwargs)
    
    def create_status_label(parent, text="", **kwargs):
        textvariable = kwargs.pop('textvariable', None)
        if textvariable:
            return ttk.Label(parent, text=text, textvariable=textvariable, style='RKI.Status.TLabel', **kwargs)
        else:
            return ttk.Label(parent, text=text, style='RKI.Status.TLabel', **kwargs)
    
    def create_button(parent, text, command=None, **kwargs):
        return ttk.Button(parent, text=text, command=command, style='RKI.TButton', **kwargs)
    
    def create_primary_button(parent, text, command=None, **kwargs):
        return ttk.Button(parent, text=text, command=command, style='RKI.Primary.TButton', **kwargs)
    
    def create_success_button(parent, text, command=None, **kwargs):
        return ttk.Button(parent, text=text, command=command, style='RKI.Success.TButton', **kwargs)
    
    def create_entry(parent, **kwargs):
        return ttk.Entry(parent, style='RKI.TEntry', **kwargs)
    
    def create_combobox(parent, **kwargs):
        return ttk.Combobox(parent, style='RKI.TCombobox', **kwargs)
    
    def create_labelframe(parent, text, **kwargs):
        return ttk.LabelFrame(parent, text=text, style='RKI.TLabelframe', **kwargs)
    
    def create_treeview(parent, **kwargs):
        return ttk.Treeview(parent, style='RKI.Treeview', **kwargs)
    
    def create_notebook(parent, **kwargs):
        return ttk.Notebook(parent, style='RKI.TNotebook', **kwargs)
    
    def create_frame(parent, **kwargs):
        return ttk.Frame(parent, style='RKI.TFrame', **kwargs)
    
    def create_scrollbar(parent, **kwargs):
        return ttk.Scrollbar(parent, style='RKI.Vertical.TScrollbar', **kwargs)
    
    return {
        'title_label': create_title_label,
        'heading_label': create_heading_label,
        'label': create_label,
        'status_label': create_status_label,
        'button': create_button,
        'primary_button': create_primary_button,
        'success_button': create_success_button,
        'entry': create_entry,
        'combobox': create_combobox,
        'labelframe': create_labelframe,
        'treeview': create_treeview,
        'notebook': create_notebook,
        'frame': create_frame,
        'scrollbar': create_scrollbar
    }

def apply_rki_theme_to_app(root):
    """Apply Red Cross Institute theme to the entire application"""
    theme = RKITheme(root)
    theme.apply_theme()
    widget_factory = create_styled_widgets()
    
    return theme, widget_factory

# Example usage and theme preview
if __name__ == "__main__":
    # Create a demo window to show the theme
    demo_root = tk.Tk()
    demo_root.title("RKI Theme Demo")
    demo_root.geometry("600x400")
    
    # Apply theme
    theme, widgets = apply_rki_theme_to_app(demo_root)
    
    # Create demo content
    main_frame = widgets['frame'](demo_root, padding="20")
    main_frame.pack(fill='both', expand=True)
    
    # Title
    title = widgets['title_label'](main_frame, "Red Cross Institute Theme Demo")
    title.pack(pady=(0, 20))
    
    # Heading
    heading = widgets['heading_label'](main_frame, "Sample Interface Elements")
    heading.pack(pady=(0, 10))
    
    # Button frame
    button_frame = widgets['frame'](main_frame)
    button_frame.pack(pady=10)
    
    # Sample buttons
    widgets['primary_button'](button_frame, "Primary Action").pack(side='left', padx=5)
    widgets['button'](button_frame, "Standard Button").pack(side='left', padx=5)
    widgets['success_button'](button_frame, "Success Action").pack(side='left', padx=5)
    
    # Entry and combobox
    entry_frame = widgets['frame'](main_frame)
    entry_frame.pack(pady=10, fill='x')
    
    widgets['label'](entry_frame, "Sample Entry:").pack(anchor='w')
    widgets['entry'](entry_frame, width=30).pack(pady=5, fill='x')
    
    widgets['label'](entry_frame, "Sample Combobox:").pack(anchor='w')
    combo = widgets['combobox'](entry_frame, values=["Option 1", "Option 2", "Option 3"])
    combo.pack(pady=5, fill='x')
    
    # Sample labelframe
    lf = widgets['labelframe'](main_frame, "Sample Group", padding="10")
    lf.pack(pady=10, fill='x')
    
    widgets['label'](lf, "This is content inside a labelframe").pack()
    
    demo_root.mainloop()
