import tkinter as tk
from tkinter import ttk
import time

class AtOS:
    def __init__(self, root):
        self.root = root
        self.root.title("atOS")
        self.root.geometry("800x600")
        self.root.configure(bg="#3A6EA5") # XP Desktop Blue

        # --- OS-like elements ---
        self.desktop_frame = tk.Frame(self.root, bg="#3A6EA5") # XP Desktop Blue
        self.desktop_frame.pack(fill=tk.BOTH, expand=True)

        self.taskbar_frame = tk.Frame(self.root, bg="#245EDC", height=40) # XP Taskbar Blue
        self.taskbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.taskbar_frame.pack_propagate(False) # Prevent resizing by children

        self.start_button = tk.Button(
            self.taskbar_frame,
            text="Start",
            font=("Tahoma", 10, "bold"),
            bg="#5CB033", # XP Start Button Green
            fg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=2,
            command=self.toggle_start_menu
        )
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clock_label = tk.Label(
            self.taskbar_frame,
            text="",
            font=("Tahoma", 9),
            bg="#245EDC", # XP Taskbar Blue
            fg="white"
        )
        self.clock_label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.update_clock()

        # --- Start Menu (initially hidden) ---
        self.start_menu = None

        # --- Desktop Icons ---
        self.create_desktop_icons()

        # --- File System Mock ---
        self.file_system = {
            "Desktop": {
                "CRAP": {
                    "type": "folder",
                    "contents": {
                        "test.py": {"type": "file", "content": "# This is a test Python file."},
                        "snake.py": {"type": "file", "content": "# This is a snake game Python file."}
                    }
                }
            }
        }
        self.open_windows = {} # To keep track of open folder windows

    def update_clock(self):
        """Updates the clock on the taskbar."""
        current_time = time.strftime("%I:%M %p") # e.g., 02:30 PM
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock) # Update every second

    def create_desktop_icons(self):
        """Creates icons on the desktop."""
        # CRAP Folder Icon
        crap_folder_icon = self.create_icon_button(
            self.desktop_frame,
            text="📁\nCRAP",
            command=lambda: self.open_folder_window("CRAP", self.file_system["Desktop"]["CRAP"]["contents"])
        )
        crap_folder_icon.place(x=30, y=30) # Position on desktop

    def create_icon_button(self, parent, text, command, icon_char=None):
        """Helper to create an icon-like button."""
        # In a real scenario, you'd use images. Here, we use text.
        # If an icon character is provided, use it. Otherwise, parse from text.
        display_text = text
        if icon_char:
            display_text = f"{icon_char}\n{text}"

        button = tk.Button(
            parent,
            text=display_text,
            font=("Tahoma", 8),
            bg="#3A6EA5", # Desktop background for transparency effect
            fg="white",
            compound=tk.TOP, # For text below icon (if we had an image)
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0, # Removes focus border
            activebackground="#4D82B7", # Slightly different shade for active
            activeforeground="white",
            command=command,
            wraplength=60, # Wrap text if too long
            justify=tk.CENTER
        )
        return button

    def toggle_start_menu(self):
        """Shows or hides the start menu."""
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
        else:
            self.start_menu = tk.Toplevel(self.root)
            self.start_menu.overrideredirect(True) # Remove window decorations
            
            # Position start menu
            start_button_x = self.start_button.winfo_rootx()
            start_button_y = self.start_button.winfo_rooty()
            start_button_height = self.start_button.winfo_height()
            
            menu_width = 200
            menu_height = 300
            
            # Ensure it doesn't go off screen (basic check)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            x_pos = start_button_x
            y_pos = start_button_y - menu_height

            if y_pos < 0 : y_pos = 0 # prevent going above screen
            if x_pos + menu_width > screen_width: x_pos = screen_width - menu_width


            self.start_menu.geometry(f"{menu_width}x{menu_height}+{x_pos}+{y_pos}")
            self.start_menu.configure(bg="#D4D0C8") # XP Menu Grey
            self.start_menu.attributes("-topmost", True) # Keep on top

            # Start Menu content (simple example)
            user_frame = tk.Frame(self.start_menu, bg="#245EDC", height=60) # XP Blue header
            user_frame.pack(fill=tk.X, side=tk.TOP)
            user_frame.pack_propagate(False)
            
            tk.Label(user_frame, text="atOS User", font=("Tahoma", 12, "bold"), fg="white", bg="#245EDC").pack(pady=15, padx=10, side=tk.LEFT)

            programs_button = tk.Button(self.start_menu, text="Programs ▸", anchor="w", relief=tk.FLAT, bg="#D4D0C8", fg="black", font=("Tahoma", 9), padx=10, command=self.show_programs_submenu)
            programs_button.pack(fill=tk.X, pady=2)
            
            # A separator
            separator = tk.Frame(self.start_menu, height=1, bg="#ACA899", relief=tk.SUNKEN) # XP Separator color
            separator.pack(fill=tk.X, padx=5, pady=5)

            shutdown_button = tk.Button(self.start_menu, text="Turn Off Computer...", anchor="w", relief=tk.FLAT, bg="#D4D0C8", fg="black", font=("Tahoma", 9), padx=10, command=self.shutdown_atos)
            shutdown_button.pack(fill=tk.X, pady=2, side=tk.BOTTOM)

            # Make menu disappear if clicked outside
            self.start_menu.bind("<FocusOut>", lambda e: self.close_start_menu_on_focus_out())
            self.root.bind("<Button-1>", lambda e: self.close_start_menu_on_click_outside(e), add="+")
            self.start_menu.focus_set()


    def close_start_menu_on_focus_out(self):
        if self.start_menu and self.start_menu.winfo_exists():
            # Check if focus is still within the start menu or its children
            # This is a bit tricky; a simpler way is to close on any click outside
            pass # For now, rely on click outside

    def close_start_menu_on_click_outside(self, event):
        if self.start_menu and self.start_menu.winfo_exists():
            # Check if the click was outside the start menu and not on the start button
            widget_clicked = event.widget
            if widget_clicked != self.start_button and not self.is_widget_child_of(widget_clicked, self.start_menu):
                self.start_menu.destroy()
                self.start_menu = None
                # Unbind after closing to prevent issues
                self.root.unbind("<Button-1>")


    def is_widget_child_of(self, widget, parent_widget):
        """Checks if a widget is a child of parent_widget or is parent_widget itself."""
        current = widget
        while current:
            if current == parent_widget:
                return True
            current = current.master
        return False

    def show_programs_submenu(self):
        # Placeholder for programs submenu
        if self.start_menu and self.start_menu.winfo_exists():
            print("Programs submenu would appear here.")
            # For a real app, you'd create another Toplevel window
            # and position it next to the "Programs" button.

    def shutdown_atos(self):
        """Simulates shutting down the OS."""
        # Create a simple shutdown dialog
        shutdown_dialog = tk.Toplevel(self.root)
        shutdown_dialog.title("Turn Off Computer")
        shutdown_dialog.geometry("300x150")
        shutdown_dialog.configure(bg="#D4D0C8")
        shutdown_dialog.resizable(False, False)
        center_window(shutdown_dialog, self.root)
        shutdown_dialog.attributes("-topmost", True)


        tk.Label(shutdown_dialog, text="What do you want the computer to do?", bg="#D4D0C8", font=("Tahoma", 9)).pack(pady=10)

        btn_frame = tk.Frame(shutdown_dialog, bg="#D4D0C8")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Shut Down", command=self.root.quit, width=10, font=("Tahoma", 8)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Restart", command=lambda: self.restart_message(shutdown_dialog), width=10, font=("Tahoma", 8)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=shutdown_dialog.destroy, width=10, font=("Tahoma", 8)).pack(side=tk.LEFT, padx=5)
        
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None


    def restart_message(self, dialog):
        dialog.destroy()
        msg_box = tk.Toplevel(self.root)
        msg_box.title("Restart")
        msg_box.geometry("250x100")
        center_window(msg_box, self.root)
        msg_box.attributes("-topmost", True)
        tk.Label(msg_box, text="Restart functionality is not implemented.", font=("Tahoma", 9)).pack(pady=20, padx=10)
        tk.Button(msg_box, text="OK", command=msg_box.destroy, width=10).pack(pady=5)


    def open_folder_window(self, folder_name, contents):
        """Opens a new window for a folder."""
        if folder_name in self.open_windows and self.open_windows[folder_name].winfo_exists():
            self.open_windows[folder_name].lift()
            return

        folder_window = tk.Toplevel(self.root)
        folder_window.title(folder_name)
        folder_window.geometry("400x300")
        folder_window.configure(bg="#FFFFFF") # White background for folder content area
        center_window(folder_window, self.root) # Center the new window

        # Store reference to the window
        self.open_windows[folder_name] = folder_window
        folder_window.bind("<Destroy>", lambda e, name=folder_name: self.on_window_close(name))


        # --- Toolbar (simplified) ---
        toolbar = tk.Frame(folder_window, bg="#ECE9D8", height=30) # XP toolbar-like grey
        toolbar.pack(side=tk.TOP, fill=tk.X)
        tk.Label(toolbar, text=f"  File  Edit  View  Favorites  Tools  Help", bg="#ECE9D8", fg="black", font=("Tahoma", 8)).pack(side=tk.LEFT)

        # --- Address Bar (simplified) ---
        address_bar_frame = tk.Frame(folder_window, bg="#ECE9D8", height=25)
        address_bar_frame.pack(side=tk.TOP, fill=tk.X, pady=(0,1)) # Small space below
        tk.Label(address_bar_frame, text=" Address:", bg="#ECE9D8", fg="black", font=("Tahoma", 8)).pack(side=tk.LEFT, padx=2)
        address_entry = tk.Entry(address_bar_frame, font=("Tahoma", 8), relief=tk.SUNKEN, borderwidth=1)
        address_entry.insert(0, f" Desktop > {folder_name}")
        address_entry.config(state=tk.DISABLED) # Read-only
        address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)


        # --- Content Area ---
        content_area = tk.Frame(folder_window, bg="white", padx=10, pady=10)
        content_area.pack(fill=tk.BOTH, expand=True)

        current_x, current_y = 10, 10
        icon_width, icon_height = 70, 70 # Approximate space for icon + text

        for item_name, item_details in contents.items():
            icon_char = "📄" if item_details["type"] == "file" else "📁"
            
            file_icon_button = self.create_icon_button(
                content_area,
                text=item_name,
                command=lambda name=item_name, details=item_details: self.open_file_or_folder(name, details, folder_window),
                icon_char=icon_char
            )
            # Simple grid layout for icons within the folder
            file_icon_button.place(x=current_x, y=current_y, width=icon_width, height=icon_height)
            
            current_x += icon_width + 10 # Move to next column
            if current_x + icon_width > 380: # If next icon exceeds window width (approx)
                current_x = 10
                current_y += icon_height + 10 # Move to next row
        
        folder_window.protocol("WM_DELETE_WINDOW", lambda name=folder_name: self.on_window_close_protocol(name))


    def on_window_close(self, window_name):
        """Callback when a Toplevel window is destroyed."""
        if window_name in self.open_windows:
            del self.open_windows[window_name]
            # print(f"Window '{window_name}' closed and removed from tracking.")

    def on_window_close_protocol(self, window_name):
        """Handles the WM_DELETE_WINDOW protocol for custom close behavior."""
        if window_name in self.open_windows:
            if self.open_windows[window_name].winfo_exists():
                self.open_windows[window_name].destroy()
            # The <Destroy> binding will call on_window_close to clean up the dictionary
            # print(f"Window '{window_name}' explicitly closed via protocol.")


    def open_file_or_folder(self, name, details, parent_window):
        """Handles clicking on a file or folder icon within a folder window."""
        if details["type"] == "file":
            self.open_file_viewer(name, details["content"], parent_window)
        elif details["type"] == "folder":
            # This basic example doesn't have nested folders beyond CRAP.
            # For a more complex system, you'd call open_folder_window recursively.
            print(f"Opening sub-folder '{name}' is not implemented in this basic demo.")
            self.show_message_dialog("Not Implemented", f"Opening sub-folder '{name}' is not implemented.", parent_window)


    def open_file_viewer(self, file_name, file_content, parent_window):
        """Opens a simple text viewer for a file."""
        if file_name in self.open_windows and self.open_windows[file_name].winfo_exists():
             self.open_windows[file_name].lift()
             return

        file_viewer = tk.Toplevel(parent_window) # Make it a child of the folder window
        file_viewer.title(f"{file_name} - atOS Text Viewer")
        file_viewer.geometry("500x400")
        file_viewer.configure(bg="#FFFFFF")
        center_window(file_viewer, parent_window)

        self.open_windows[file_name] = file_viewer # Track this window
        file_viewer.bind("<Destroy>", lambda e, name=file_name: self.on_window_close(name))
        file_viewer.protocol("WM_DELETE_WINDOW", lambda name=file_name: self.on_window_close_protocol(name))


        # Menu bar for the text viewer
        menubar = tk.Menu(file_viewer)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Close", command=lambda name=file_name: self.on_window_close_protocol(name))
        menubar.add_cascade(label="File", menu=file_menu)
        file_viewer.config(menu=menubar)

        text_area = tk.Text(file_viewer, wrap=tk.WORD, font=("Courier New", 10), relief=tk.FLAT)
        text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_area.insert(tk.END, file_content)
        text_area.config(state=tk.DISABLED) # Read-only

        # Scrollbar
        scrollbar = ttk.Scrollbar(text_area, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)

    def show_message_dialog(self, title, message, parent_window):
        """Displays a simple message dialog."""
        dialog = tk.Toplevel(parent_window)
        dialog.title(title)
        dialog.geometry("300x100")
        center_window(dialog, parent_window)
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        
        tk.Label(dialog, text=message, wraplength=280, font=("Tahoma", 9)).pack(pady=15, padx=10)
        tk.Button(dialog, text="OK", command=dialog.destroy, width=10).pack(pady=5)


def center_window(window, parent_window=None):
    """Centers a Toplevel window on the screen or relative to its parent."""
    window.update_idletasks() # Ensure window dimensions are calculated
    width = window.winfo_width()
    height = window.winfo_height()
    
    if parent_window:
        parent_x = parent_window.winfo_x()
        parent_y = parent_window.winfo_y()
        parent_width = parent_window.winfo_width()
        parent_height = parent_window.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
    else:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
    window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    main_root = tk.Tk()
    app = AtOS(main_root)
    main_root.mainloop()
