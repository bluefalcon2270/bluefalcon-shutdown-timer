# Version: v1.4
# Developer: BlueFalcon
# App: BlueFalcon Shutdown Timer

import customtkinter as ctk
import subprocess
import math
import webbrowser

class ShutdownTimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("BlueFalcon Shutdown Timer v1.4")
        self.geometry("450x280")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # State Variables
        self.timer_running = False
        self.time_left = 0
        self.original_input = ""
        
        # Settings Variables
        self.input_unit = ctk.StringVar(value="Minutes")
        self.show_days = ctk.BooleanVar(value=False) # Changed to False by default
        self.show_seconds = ctk.BooleanVar(value=True)

        # Settings/Info Button (Top Right)
        self.info_btn = ctk.CTkButton(
            self, 
            text="⚙️", 
            width=30, 
            height=30, 
            fg_color="transparent", 
            hover_color="gray25", 
            font=("Arial", 16), 
            command=self.open_settings_window
        )
        self.info_btn.place(relx=0.96, rely=0.04, anchor="ne")

        # Dynamic Unit / Status Label
        self.status_label = ctk.CTkLabel(
            self, 
            text="Current Unit: Minutes", 
            font=("Arial", 12), 
            text_color="gray"
        )
        self.status_label.pack(pady=(25, 0))

        # Unified Time Input / Display
        self.time_var = ctk.StringVar()
        self.time_entry = ctk.CTkEntry(
            self, 
            textvariable=self.time_var, 
            font=("Courier", 40, "bold"), 
            width=320, 
            height=65, 
            justify="center", 
            placeholder_text="Time (Minutes)"
        )
        self.time_entry.pack(pady=(2, 15))

        # Action Dropdown
        self.action_var = ctk.StringVar(value="Shutdown")
        self.action_combo = ctk.CTkComboBox(
            self, 
            values=["Shutdown", "Restart", "Hibernate", "Sleep"], 
            variable=self.action_var, 
            width=200, 
            height=35, 
            font=("Arial", 14)
        )
        self.action_combo.pack(pady=(0, 20))

        # Unified Toggle Button (Start/Stop)
        self.toggle_btn = ctk.CTkButton(
            self, 
            text="▶ START", 
            width=200, 
            height=40, 
            font=("Arial", 14, "bold"),
            fg_color="#28a745", 
            hover_color="#218838", 
            command=self.toggle_timer
        )
        self.toggle_btn.pack()

    def update_unit_display(self, *args):
        # Update the placeholder and status label based on the selected unit
        unit = self.input_unit.get()
        self.time_entry.configure(placeholder_text=f"Time ({unit})")
        
        # Only update the text if the timer is NOT currently running
        if not self.timer_running:
            self.status_label.configure(text=f"Current Unit: {unit}")

    def format_time(self, total_seconds):
        # Calculate time components
        d = total_seconds // 86400
        h = (total_seconds % 86400) // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60

        # Build dynamic string based on settings
        parts = []
        if self.show_days.get():
            parts.append(f"{d:02d}")
        
        parts.append(f"{h:02d}")
        parts.append(f"{m:02d}")
        
        if self.show_seconds.get():
            parts.append(f"{s:02d}")

        return ":".join(parts)

    def toggle_timer(self):
        if not self.timer_running:
            self.start_timer()
        else:
            self.cancel_timer()

    def update_timer_display(self):
        if self.timer_running and self.time_left > 0:
            self.time_var.set(self.format_time(self.time_left))
            self.time_left -= 1
            self.after(1000, self.update_timer_display)
            
        elif self.time_left <= 0 and self.timer_running:
            self.time_var.set(self.format_time(0))
            self.timer_running = False
            self.execute_delayed_action()
            self.reset_ui_state()

    def start_timer(self):
        try:
            input_val = self.time_var.get()
            
            # Basic validation to grab the raw number if they typed something complex
            if ":" in input_val:
                base_time = int(input_val.split(":")[0])
            else:
                base_time = int(input_val)

            if base_time <= 0:
                return
                
            self.original_input = str(base_time)
            
            # Convert based on selected unit
            if self.input_unit.get() == "Minutes":
                seconds = base_time * 60
            else:
                seconds = base_time * 3600

            action = self.action_var.get()
            
            # Execute Windows OS commands IMMEDIATELY in the background (Non-Blocking)
            if action == "Shutdown":
                subprocess.Popen(f"shutdown /s /t {seconds}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            elif action == "Restart":
                subprocess.Popen(f"shutdown /r /t {seconds}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # NOTE: Hibernate and Sleep are executed when the timer hits zero.

            # Update GUI state for Running
            self.time_left = seconds
            self.timer_running = True
            
            # Visual Updates
            self.status_label.configure(text="Time Remaining", text_color="#1f6aa5")
            self.time_entry.configure(state="disabled", text_color="white")
            self.action_combo.configure(state="disabled")
            
            self.toggle_btn.configure(
                text="■ STOP", 
                fg_color="#dc3545", 
                hover_color="#c82333"
            )
            
            # Force immediate visual update so it doesn't wait 1 second to change
            self.time_var.set(self.format_time(self.time_left))
            
            # Start the loop countdown
            self.time_left -= 1
            self.after(1000, self.update_timer_display)

        except ValueError:
            self.time_var.set("Error")

    def execute_delayed_action(self):
        # Execute delayed commands in the background (Non-Blocking)
        action = self.action_var.get()
        if action == "Hibernate":
            subprocess.Popen("shutdown /h", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        elif action == "Sleep":
            subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

    def cancel_timer(self):
        # Abort system shutdown/restart in the background (Non-Blocking)
        subprocess.Popen("shutdown /a", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Reset GUI state for Idle
        self.timer_running = False
        self.reset_ui_state()
        self.time_var.set(self.original_input)

    def reset_ui_state(self):
        self.status_label.configure(text=f"Current Unit: {self.input_unit.get()}", text_color="gray")
        self.time_entry.configure(state="normal")
        self.action_combo.configure(state="normal")
        self.toggle_btn.configure(
            text="▶ START", 
            fg_color="#28a745", 
            hover_color="#218838"
        )

    def open_settings_window(self):
        # Prevent multiple windows from opening
        if hasattr(self, "settings_win") and self.settings_win is not None and self.settings_win.winfo_exists():
            self.settings_win.focus()
            return

        # Create Toplevel window
        self.settings_win = ctk.CTkToplevel(self)
        self.settings_win.title("Settings & Info")
        self.settings_win.geometry("380x320")
        self.settings_win.resizable(False, False)
        
        # Bring window to front
        self.settings_win.attributes("-topmost", True)
        self.settings_win.grab_set()

        # Create Tabview
        tabview = ctk.CTkTabview(self.settings_win, width=340, height=280)
        tabview.pack(pady=10, padx=10)
        tabview.add("Settings")
        tabview.add("About")

        # --- SETTINGS TAB ---
        # Input Unit Control
        unit_label = ctk.CTkLabel(tabview.tab("Settings"), text="Time Input Unit:", font=("Arial", 13, "bold"))
        unit_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        unit_menu = ctk.CTkOptionMenu(
            tabview.tab("Settings"),
            values=["Minutes", "Hours"],
            variable=self.input_unit,
            command=self.update_unit_display
        )
        unit_menu.grid(row=0, column=1, padx=10, pady=(20, 10))

        # Days Display Control
        days_switch = ctk.CTkSwitch(
            tabview.tab("Settings"),
            text="Display Days in Timer (DD:HH...)",
            variable=self.show_days,
            font=("Arial", 12)
        )
        days_switch.grid(row=1, column=0, columnspan=2, padx=20, pady=15, sticky="w")

        # Seconds Display Control
        secs_switch = ctk.CTkSwitch(
            tabview.tab("Settings"),
            text="Display Seconds in Timer (...MM:SS)",
            variable=self.show_seconds,
            font=("Arial", 12)
        )
        secs_switch.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky="w")

        # --- ABOUT TAB ---
        title_label = ctk.CTkLabel(tabview.tab("About"), text="BlueFalcon Shutdown Timer", font=("Arial", 16, "bold"))
        title_label.pack(pady=(20, 5))

        version_label = ctk.CTkLabel(tabview.tab("About"), text="Version 1.4", font=("Arial", 12), text_color="gray")
        version_label.pack(pady=(0, 10))

        dev_label = ctk.CTkLabel(tabview.tab("About"), text="Developed by: BlueFalcon", font=("Arial", 13))
        dev_label.pack(pady=(5, 2))
        
        email_label = ctk.CTkLabel(tabview.tab("About"), text="Email: Bluefalcon2270@gmail.com", font=("Arial", 12))
        email_label.pack(pady=(0, 15))

        github_url = "https://github.com/bluefalcon2270/bluefalcon-shutdown-timer"
        github_btn = ctk.CTkButton(
            tabview.tab("About"), 
            text="GitHub Repository", 
            width=150, 
            command=lambda: webbrowser.open(github_url)
        )
        github_btn.pack(pady=5)

if __name__ == "__main__":
    app = ShutdownTimerApp()
    app.mainloop()