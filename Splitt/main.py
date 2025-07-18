# Entry point for the Gießplan application

import os
import sys
import atexit
import tkinter.messagebox as messagebox

def check_single_instance():
    """Ensure only one instance of the application is running"""
    pid_file = "giessplan.pid"
    
    # Check if PID file exists
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            # Check if process is still running (Windows compatible)
            try:
                if os.name == 'nt':  # Windows
                    import subprocess
                    result = subprocess.run(['tasklist', '/fi', f'PID eq {old_pid}'], 
                                          capture_output=True, text=True)
                    if str(old_pid) in result.stdout:
                        # Process exists
                        messagebox.showerror("Gießplan bereits geöffnet", 
                                           "Eine andere Instanz von Gießplan läuft bereits.\n\nBitte schließen Sie die andere Anwendung zuerst.")
                        sys.exit(1)
                else:  # Unix/Linux/Mac
                    os.kill(old_pid, 0)  # Signal 0 just checks if process exists
                    messagebox.showerror("Gießplan already running", 
                                       "Another instance of Gießplan is already running.\n\nPlease close the other application first.")
                    sys.exit(1)
            except (subprocess.CalledProcessError, OSError, FileNotFoundError):
                # Process doesn't exist, remove stale PID file
                try:
                    os.remove(pid_file)
                except:
                    pass
        except (ValueError, FileNotFoundError):
            # Invalid or missing PID file, remove it
            try:
                os.remove(pid_file)
            except:
                pass
    
    # Create new PID file
    try:
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # Clean up PID file on exit
        atexit.register(lambda: os.path.exists(pid_file) and os.remove(pid_file))
    except Exception as e:
        print(f"Warning: Could not create PID file: {e}")

# Check for single instance before importing GUI
check_single_instance()

from gui import root
# The application starts when gui.py is imported and root.mainloop() is called there.