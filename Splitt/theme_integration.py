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

class RKIModernColors:
    """Modern refined theme color palette inspired by Red Cross Institute"""
    
    # Dark theme backgrounds (different levels for visual hierarchy)
    DARK_BACKGROUND = "#2b2d31"       # Main window background
    DARKER_BACKGROUND = "#1e1f23"     # Deeper sections
    CARD_BACKGROUND = "#36393f"       # Card/container background
    SIDEBAR_BACKGROUND = "#32353b"    # Sidebar areas
    
    # Primary Red Cross colors (kept for important elements)
    RED_CROSS_RED = "#DC143C"
    RED_CROSS_BRIGHT = "#e53e3e"
    RED_CROSS_MUTED = "#c53030"
    
    # Softer accent colors (less aggressive)
    SOFT_BLUE = "#5865f2"
    LIGHT_BLUE = "#7289da"
    MUTED_BLUE = "#4f63d2"
    
    # Text colors (changed to white for everything except title)
    PRIMARY_TEXT = "#ffffff"
    SECONDARY_TEXT = "#ffffff"  # Changed from #b9bbbe to white
    MUTED_TEXT = "#ffffff"     # Changed from #8e9297 to white
    DISABLED_TEXT = "#cccccc"   # Slightly dimmed white for disabled items
    
    # UI element colors (proper hierarchy)
    BORDER_COLOR = "#40444b"
    HOVER_COLOR = "#3c4043"
    ACTIVE_COLOR = "#42464d"
    INPUT_BACKGROUND = "#40444b"
    
    # Status colors (toned down)
    SUCCESS_GREEN = "#43b581"
    WARNING_ORANGE = "#faa61a"
    ERROR_RED = "#f04747"
    INFO_BLUE = "#5865f2"
    
    # Selection colors (fixed contrast)
    SELECTION_BACKGROUND = "#5865f2"
    SELECTION_TEXT = "#ffffff"
    
    # Gradient colors for modern look
    GRADIENT_START = "#DC143C"
    GRADIENT_END = "#5865f2"

class RKITheme:
    """Theme configuration for Red Cross Institute styling"""
    
    def __init__(self, root, modern_theme=True):
        self.root = root
        self.modern_theme = modern_theme
        self.colors = RKIModernColors() if modern_theme else RKIColors()
        self.style = ttk.Style()
        
    def apply_theme(self):
        """Apply the complete Red Cross Institute theme"""
        print(f"🎨 Applying theme - Modern: {self.modern_theme}")
        self._configure_root()
        if self.modern_theme:
            print("🌙 Configuring modern dark theme...")
            self._configure_modern_styles()
        else:
            print("☀️ Configuring classic theme...")
            self._configure_ttk_styles()
        self._configure_canvas_styles()
        print("✅ Theme configuration complete")
        
    def _configure_root(self):
        """Configure the main window"""
        if self.modern_theme:
            self.root.configure(bg=self.colors.DARK_BACKGROUND)
        else:
            self.root.configure(bg=self.colors.BACKGROUND_GRAY)
            
    def _configure_modern_styles(self):
        """Configure modern dark theme styles"""
        
        # AGGRESSIVE STYLE RESET
        # Clear any existing styles first by switching themes multiple times
        available_themes = self.style.theme_names()
        for theme_name in available_themes:
            try:
                self.style.theme_use(theme_name)
            except:
                continue
        
        # Now set our base theme
        try:
            self.style.theme_use('clam')
        except:
            try:
                self.style.theme_use('alt')
            except:
                self.style.theme_use('default')
        
        # Force clear all existing RKI styles
        rki_styles = [
            'RKI.TFrame', 'RKI.Card.TFrame', 'RKI.Title.TLabel', 'RKI.Heading.TLabel',
            'RKI.TLabel', 'RKI.Card.TLabel', 'RKI.Status.TLabel', 'RKI.TButton',
            'RKI.Primary.TButton', 'RKI.Success.TButton', 'RKI.TNotebook',
            'RKI.TNotebook.Tab', 'RKI.TEntry', 'RKI.TCombobox', 'RKI.TLabelframe',
            'RKI.TLabelframe.Label', 'RKI.Treeview', 'RKI.Treeview.Heading',
            'RKI.Vertical.TScrollbar', 'RKI.TSeparator'
        ]
        
        for style_name in rki_styles:
            try:
                # Configure with empty dictionary to clear
                self.style.configure(style_name, **{})
                self.style.map(style_name, **{})
            except:
                pass
        
        # Configure main frame style with consistent background
        self.style.configure('RKI.TFrame', 
                           background=self.colors.DARK_BACKGROUND,
                           relief='flat',
                           borderwidth=0)
        print(f"   ✓ Frame background: {self.colors.DARK_BACKGROUND}")
        
        # Configure card-like frames with consistent styling
        self.style.configure('RKI.Card.TFrame',
                           background=self.colors.CARD_BACKGROUND,  # Match container background
                           relief='flat',
                           borderwidth=0)
        print(f"   ✓ Card background: {self.colors.CARD_BACKGROUND}")
        
        # Configure title label
        self.style.configure('RKI.Title.TLabel',
                           font=('Segoe UI', 24, 'bold'),
                           background=self.colors.DARK_BACKGROUND,
                           foreground=self.colors.RED_CROSS_RED)
        print(f"   ✓ Title color: {self.colors.RED_CROSS_RED} (RED)")
        
        # Configure heading labels
        self.style.configure('RKI.Heading.TLabel',
                           font=('Segoe UI', 14, 'bold'),
                           background=self.colors.DARK_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT)
        print(f"   ✓ Heading color: {self.colors.PRIMARY_TEXT}")
        
        # Configure regular labels with consistent background
        self.style.configure('RKI.TLabel',
                           font=('Segoe UI', 11),
                           background=self.colors.DARK_BACKGROUND,
                           foreground=self.colors.SECONDARY_TEXT)
        print(f"   ✓ Label color: {self.colors.SECONDARY_TEXT}")
        
        # Configure card labels with consistent background
        self.style.configure('RKI.Card.TLabel',
                           font=('Segoe UI', 11),
                           background=self.colors.CARD_BACKGROUND,  # Match container background
                           foreground=self.colors.SECONDARY_TEXT)
        
        # Configure status labels
        self.style.configure('RKI.Status.TLabel',
                           font=('Segoe UI', 10),
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.MUTED_TEXT,
                           relief='flat',
                           padding=(8, 4))
        
        # Configure modern buttons with professional styling inspired by reference design
        button_color = '#4c5fd5'  # Professional dark blue/purple
        button_hover = '#5a6edf'  # Subtle lighter hover
        button_pressed = '#3d4fb8'  # Darker when pressed
        
        # Standard buttons - consistent height and modern appearance
        standard_padding = (16, 10)  # Professional padding for good clickability
        self.style.configure('RKI.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           background=button_color,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,  # Clean flat design
                           relief='flat',
                           focuscolor='none',
                           padding=standard_padding)
        print(f"   ✓ Standard button: {button_color} (PROFESSIONAL BLUE)")
        
        self.style.map('RKI.TButton',
                      background=[('active', button_hover),
                                ('pressed', button_pressed)])
        
        # Primary action buttons - SAME SIZE as standard for consistency
        self.style.configure('RKI.Primary.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background=button_color,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,
                           relief='flat',
                           focuscolor='none',
                           padding=standard_padding)  # Same padding as standard
        print(f"   ✓ Primary button: {button_color} (PROFESSIONAL BLUE)")
        
        self.style.map('RKI.Primary.TButton',
                      background=[('active', button_hover),
                                ('pressed', button_pressed)])
        
        # Success buttons - same as standard for group consistency
        self.style.configure('RKI.Success.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           background=button_color,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,
                           relief='flat',
                           focuscolor='none',
                           padding=standard_padding)
        
        self.style.map('RKI.Success.TButton',
                      background=[('active', button_hover),
                                ('pressed', button_pressed)])
        
        # Small utility buttons - compact for secondary actions
        small_padding = (12, 8)  # Smaller but still clickable
        self.style.configure('RKI.Small.TButton',
                           font=('Segoe UI', 9, 'bold'),
                           background=button_color,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,
                           relief='flat',
                           focuscolor='none',
                           padding=small_padding)
        
        self.style.map('RKI.Small.TButton',
                      background=[('active', button_hover),
                                ('pressed', button_pressed)])
        
        # Configure modern notebook tabs with dark blue/purple theme
        tab_color = '#4c5fd5'  # Same dark blue/purple as buttons
        tab_hover = '#5a6edf'   # Lighter on hover
        
        self.style.configure('RKI.TNotebook',
                           background=self.colors.DARK_BACKGROUND,
                           borderwidth=0,
                           tabposition='n')
        
        self.style.configure('RKI.TNotebook.Tab',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.SECONDARY_TEXT,
                           padding=(24, 12),
                           borderwidth=0,
                           relief='flat')
        
        self.style.map('RKI.TNotebook.Tab',
                      background=[('selected', tab_color),
                                ('active', tab_hover)],
                      foreground=[('selected', self.colors.PRIMARY_TEXT),
                                ('active', self.colors.PRIMARY_TEXT)])
        
        # Configure modern entries with container-matching background
        self.style.configure('RKI.TEntry',
                           font=('Segoe UI', 10),
                           fieldbackground=self.colors.CARD_BACKGROUND,  # Match container background
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,  # Clean flat design
                           relief='flat',
                           insertcolor=self.colors.PRIMARY_TEXT,
                           padding=(12, 8))  # Comfortable padding
        
        self.style.map('RKI.TEntry',
                      fieldbackground=[('focus', self.colors.CARD_BACKGROUND)],
                      lightcolor=[('focus', self.colors.SOFT_BLUE)],
                      darkcolor=[('focus', self.colors.SOFT_BLUE)])
        
        # Configure modern comboboxes with container-matching background
        self.style.configure('RKI.TCombobox',
                           font=('Segoe UI', 10),
                           fieldbackground=self.colors.CARD_BACKGROUND,  # Match container background
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,
                           relief='flat',
                           padding=(12, 8),
                           arrowcolor=self.colors.SECONDARY_TEXT)
        
        # Remove auto-selection and focus highlighting - match container background
        self.style.map('RKI.TCombobox',
                      fieldbackground=[('readonly', self.colors.CARD_BACKGROUND),
                                     ('focus', self.colors.CARD_BACKGROUND)],
                      selectbackground=[('readonly', self.colors.CARD_BACKGROUND)],
                      selectforeground=[('readonly', self.colors.PRIMARY_TEXT)],
                      focuscolor=[('readonly', 'none')])
        
        # Configure modern labelframes with professional styling
        self.style.configure('RKI.TLabelframe',
                           background=self.colors.CARD_BACKGROUND,
                           borderwidth=0,  # Clean flat design
                           relief='flat')
        
        self.style.configure('RKI.TLabelframe.Label',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT,  # Changed to white
                           padding=(0, 5))
        
        # Configure modern treeview with professional appearance
        self.style.configure('RKI.Treeview',
                           font=('Segoe UI', 10),
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.SECONDARY_TEXT,
                           fieldbackground=self.colors.CARD_BACKGROUND,
                           borderwidth=0,  # Clean flat design
                           relief='flat')
        
        self.style.configure('RKI.Treeview.Heading',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.colors.DARKER_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT,
                           relief='flat',
                           borderwidth=0)
        
        # Professional selection colors to match input field background
        self.style.map('RKI.Treeview',
                      background=[('selected', self.colors.INPUT_BACKGROUND)],
                      foreground=[('selected', self.colors.PRIMARY_TEXT)])
        
        # Configure additional treeview tags for schedule display with consistent backgrounds
        self.schedule_treeview_tags = {
            'oddrow': {'background': self.colors.INPUT_BACKGROUND, 'foreground': self.colors.SECONDARY_TEXT},
            'evenrow': {'background': self.colors.DARKER_BACKGROUND, 'foreground': self.colors.SECONDARY_TEXT},
            'current_week': {'background': '#4c5fd5', 'foreground': self.colors.PRIMARY_TEXT},  # Dark blue/purple
            'next_week': {'background': self.colors.WARNING_ORANGE, 'foreground': self.colors.PRIMARY_TEXT}
        }
        
        # Configure modern text widget style
        self.text_widget_config = {
            'font': ('Consolas', 10),
            'bg': self.colors.CARD_BACKGROUND,  # Match container background
            'fg': self.colors.SECONDARY_TEXT,
            'insertbackground': self.colors.PRIMARY_TEXT,
            'selectbackground': self.colors.SELECTION_BACKGROUND,
            'selectforeground': self.colors.SELECTION_TEXT,
            'relief': 'flat',
            'borderwidth': 0,  # No border for consistency
            'highlightbackground': self.colors.CARD_BACKGROUND,  # Match background
            'highlightcolor': self.colors.SOFT_BLUE
        }
        
        # Configure canvas styling
        self.canvas_config = {
            'bg': self.colors.CARD_BACKGROUND,  # Match container background
            'relief': 'flat',
            'bd': 0,  # No border for consistency
            'highlightbackground': self.colors.CARD_BACKGROUND  # Match background
        }
        
        # Configure canvas fonts for schedule visualization
        self.canvas_fonts = {
            'title': ('Segoe UI', 14, 'bold'),
            'heading': ('Segoe UI', 10, 'bold'),
            'text': ('Segoe UI', 9),
            'legend': ('Segoe UI', 9)
        }
        
        # Configure modern scrollbars
        self.style.configure('RKI.Vertical.TScrollbar',
                           background=self.colors.CARD_BACKGROUND,
                           troughcolor=self.colors.DARKER_BACKGROUND,
                           borderwidth=0,
                           arrowcolor=self.colors.SECONDARY_TEXT,
                           relief='flat')
        
        self.style.map('RKI.Vertical.TScrollbar',
                      background=[('active', self.colors.HOVER_COLOR)])
        
    def _configure_root(self):
        """Configure the main window"""
        if self.modern_theme:
            self.root.configure(bg=self.colors.DARK_BACKGROUND)
        else:
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
                           foreground=self.colors.PRIMARY_TEXT)  # Changed to white
        
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
        
        # Configure entries (updated to match modern theme)
        self.style.configure('RKI.TEntry',
                           font=('Segoe UI', 10),
                           fieldbackground=self.colors.CARD_BACKGROUND,  # Match container background
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,
                           relief='flat',
                           insertcolor=self.colors.PRIMARY_TEXT,
                           padding=(12, 8))
        
        self.style.map('RKI.TEntry',
                      fieldbackground=[('focus', self.colors.CARD_BACKGROUND)])
        
        # Configure comboboxes (updated to match modern theme)
        self.style.configure('RKI.TCombobox',
                           font=('Segoe UI', 10),
                           fieldbackground=self.colors.CARD_BACKGROUND,  # Match container background
                           background=self.colors.CARD_BACKGROUND,
                           foreground=self.colors.PRIMARY_TEXT,
                           borderwidth=0,
                           relief='flat',
                           padding=(12, 8),
                           arrowcolor=self.colors.SECONDARY_TEXT)
        
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
        if self.modern_theme:
            self.canvas_colors = {
                'background': self.colors.CARD_BACKGROUND,
                'border': self.colors.BORDER_COLOR,
                'current_week': self.colors.SOFT_BLUE,
                'current_week_border': self.colors.LIGHT_BLUE,
                'next_week': self.colors.WARNING_ORANGE,
                'next_week_border': self.colors.WARNING_ORANGE,
                'text': self.colors.PRIMARY_TEXT,
                'title': self.colors.RED_CROSS_RED,
                'legend': self.colors.SECONDARY_TEXT
            }
            
            # Person color palette for schedule visualization (dark theme friendly)
            self.person_colors = [
                '#4a90e2',    # Bright blue
                '#2ed573',    # Bright green
                '#ff6b7a',    # Bright pink
                '#ffa502',    # Bright orange
                '#7bed9f',    # Light green
                '#ff4757',    # Bright red
                '#5f27cd',    # Purple
                '#00d2d3',    # Cyan
                '#ff9ff3',    # Light pink
                '#54a0ff'     # Light blue
            ]
        else:
            self.canvas_colors = {
                'background': '#FFFFFF',
                'border': '#F3F4F6',
                'current_week': '#E6F3FF',
                'current_week_border': '#1E3A8A',
                'next_week': '#FED7AA',
                'next_week_border': '#EA580C',
                'text': '#374151',
                'title': '#1E3A8A',
                'legend': '#6B7280'
            }
            
            # Person color palette for schedule visualization
            self.person_colors = [
                '#E6F3FF',    # Light blue
                '#ECFDF5',    # Light green
                '#FFE5E5',    # Light pink
                '#FFF0E5',    # Light peach
                '#E5F0FF',    # Very light blue
                '#F0FFE5',    # Very light green
                '#FFE5F0',    # Light lavender
                '#E5FFFF',    # Light cyan
                '#FFFFE5',    # Light yellow
                '#F0E5FF'     # Light purple
            ]
    
    def get_person_color(self, person_index):
        """Get a color for a person based on their index"""
        return self.person_colors[person_index % len(self.person_colors)]
    
    def get_canvas_colors(self):
        """Get canvas color scheme"""
        return self.canvas_colors
    
    def configure_treeview_tags(self, treeview):
        """Configure treeview tags for schedule display"""
        if hasattr(self, 'schedule_treeview_tags'):
            for tag, config in self.schedule_treeview_tags.items():
                treeview.tag_configure(tag, **config)
    
    def configure_text_widget(self, text_widget):
        """Configure a text widget with modern styling"""
        if hasattr(self, 'text_widget_config'):
            text_widget.configure(**self.text_widget_config)
    
    def configure_canvas(self, canvas):
        """Configure a canvas with modern styling"""
        if hasattr(self, 'canvas_config'):
            canvas.configure(**self.canvas_config)
    
    def get_canvas_font(self, font_type):
        """Get canvas font configuration"""
        if hasattr(self, 'canvas_fonts'):
            return self.canvas_fonts.get(font_type, ('Segoe UI', 9))
        return ('Segoe UI', 9)

def create_styled_widgets(modern_theme=True):
    """Factory functions for creating styled widgets"""
    
    def create_title_label(parent, text="", **kwargs):
        return ttk.Label(parent, text=text, style='RKI.Title.TLabel', **kwargs)
    
    def create_heading_label(parent, text="", **kwargs):
        return ttk.Label(parent, text=text, style='RKI.Heading.TLabel', **kwargs)
    
    def create_label(parent, text="", **kwargs):
        # Extract textvariable if present
        textvariable = kwargs.pop('textvariable', None)
        style = 'RKI.Card.TLabel' if modern_theme and 'card' in str(parent).lower() else 'RKI.TLabel'
        if textvariable:
            return ttk.Label(parent, text=text, textvariable=textvariable, style=style, **kwargs)
        else:
            return ttk.Label(parent, text=text, style=style, **kwargs)
    
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
    
    def create_small_button(parent, text, command=None, **kwargs):
        return ttk.Button(parent, text=text, command=command, style='RKI.Small.TButton', **kwargs)
    
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
        # Check if this should be a card-style frame
        card_style = kwargs.pop('card_style', False) or 'card' in kwargs.get('name', '').lower()
        if modern_theme and card_style:
            return ttk.Frame(parent, style='RKI.Card.TFrame', **kwargs)
        else:
            return ttk.Frame(parent, style='RKI.TFrame', **kwargs)
    
    def create_scrollbar(parent, **kwargs):
        return ttk.Scrollbar(parent, style='RKI.Vertical.TScrollbar', **kwargs)
    
    def create_separator(parent, **kwargs):
        return ttk.Separator(parent, style='RKI.TSeparator', **kwargs)
    
    return {
        'title_label': create_title_label,
        'heading_label': create_heading_label,
        'label': create_label,
        'status_label': create_status_label,
        'button': create_button,
        'primary_button': create_primary_button,
        'success_button': create_success_button,
        'small_button': create_small_button,
        'entry': create_entry,
        'combobox': create_combobox,
        'labelframe': create_labelframe,
        'treeview': create_treeview,
        'notebook': create_notebook,
        'frame': create_frame,
        'scrollbar': create_scrollbar,
        'separator': create_separator
    }

def apply_rki_theme_to_app(root, modern_theme=True):
    """Apply Red Cross Institute theme to the entire application"""
    
    print("🔄 FORCE APPLYING MODERN THEME...")
    
    # NUCLEAR OPTION: Complete TTK reset
    try:
        # Get fresh style instance
        style = ttk.Style()
        
        # Cycle through ALL themes to clear any cached configurations
        for theme_name in style.theme_names():
            try:
                style.theme_use(theme_name)
                root.update_idletasks()  # Force refresh
            except:
                pass
        
        # Set base theme
        style.theme_use('clam')
        root.update_idletasks()
        
        print("✅ TTK style cache cleared")
        
        # Delete the old style object and create fresh one in theme
        del style
        
    except Exception as e:
        print(f"⚠️  Style reset warning: {e}")
    
    # Apply our theme
    theme = RKITheme(root, modern_theme=modern_theme)
    theme.apply_theme()
    widget_factory = create_styled_widgets(modern_theme=modern_theme)
    
    # FORCE IMMEDIATE APPLICATION
    try:
        root.configure(bg=theme.colors.DARK_BACKGROUND)
        root.update()
        root.update_idletasks()
        
        # Force style refresh on all existing widgets
        def refresh_widget_styles(widget):
            try:
                if hasattr(widget, 'configure'):
                    # Try to force style refresh
                    if hasattr(widget, 'cget') and 'style' in str(widget.configure()):
                        current_style = widget.cget('style') if widget.cget('style') else ''
                        if current_style and 'RKI' in current_style:
                            widget.configure(style=current_style)
                
                # Recursively refresh children
                for child in widget.winfo_children():
                    refresh_widget_styles(child)
            except:
                pass
        
        root.after_idle(lambda: refresh_widget_styles(root))
        
    except Exception as e:
        print(f"⚠️  Force refresh warning: {e}")
    
    print("✅ MODERN THEME FORCE APPLIED")
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
