# Version: v1.1
# Developer: BlueFalcon
# App: BlueFalcon Shutdown Timer

import customtkinter as ctk
import os
import math
import webbrowser

class ShutdownTimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("BlueFalcon Shutdown Timer v1.1")
        self.geometry("350x260")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.timer_running = False
        self.time_left = 0
        self.original_input = ""

        # Settings/Info Button (Top Right)
        self.info_btn = ctk.CTkButton(
            self, 
            text="⚙️", 
            width=30, 
            height=30, 
            fg_color="transparent", 
            hover_color="gray25", 
            font=("Arial", 16), 
            command=self.open_about_window
        )
        self.info_btn.place(relx=0.96, rely=0.04, anchor="ne")

        # Unified Time Input / Display
        self.time_var = ctk.StringVar()
        self.time_entry = ctk.CTkEntry(
            self, 
            textvariable=self.time_var, 
            font=("Courier", 45, "bold"), 
            width=200, 
            height=60, 
            justify="center", 
            placeholder_text="Min"
        )
        self.time_entry.pack(pady=(40, 15))

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

    def toggle_timer(self):
        if not self.timer_running:
            self.start_timer()
        else:
            self.cancel_timer()

    def update_timer_display(self):
        if self.timer_running and self.time_left > 0:
            minutes = math.floor(self.time_left / 60)
            seconds = self.time_left % 60
            self.time_var.set(f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
            self.after(1000, self.update_timer_display)
        elif self.time_left <= 0 and self.timer_running:
            self.time_var.set("00:00")
            self.timer_running = False
            self.reset_ui_state()

    def start_timer(self):
        try:
            input_val = self.time_var.get()
            # If user typed something like "30:00", we just take the 30
            if ":" in input_val:
                minutes = int(input_val.split(":")[0])
            else:
                minutes = int(input_val)

            if minutes <= 0:
                return
                
            self.original_input = str(minutes)
            seconds = minutes * 60
            action = self.action_var.get()
            
            # Execute Windows OS commands
            if action == "Shutdown":
                os.system(f"shutdown /s /t {seconds}")
            elif action == "Restart":
                os.system(f"shutdown /r /t {seconds}")
            elif action == "Hibernate":
                os.system(f"timeout /t {seconds} /nobreak && shutdown /h")
            elif action == "Sleep":
                os.system(f"timeout /t {seconds} /nobreak && rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            # Update GUI state for Running
            self.time_left = seconds
            self.timer_running = True
            
            self.time_entry.configure(state="disabled", text_color="white")
            self.action_combo.configure(state="disabled")
            
            self.toggle_btn.configure(
                text="■ STOP", 
                fg_color="#dc3545", 
                hover_color="#c82333"
            )
            
            self.update_timer_display()

        except ValueError:
            self.time_var.set("Error")

    def cancel_timer(self):
        # Abort system shutdown/restart
        os.system("shutdown /a")
        
        # Reset GUI state for Idle
        self.timer_running = False
        self.reset_ui_state()
        self.time_var.set(self.original_input)

    def reset_ui_state(self):
        self.time_entry.configure(state="normal")
        self.action_combo.configure(state="normal")
        self.toggle_btn.configure(
            text="▶ START", 
            fg_color="#28a745", 
            hover_color="#218838"
        )

    def open_about_window(self):
        # Create small Toplevel window
        about_win = ctk.CTkToplevel(self)
        about_win.title("About")
        about_win.geometry("300x220")
        about_win.resizable(False, False)
        
        # Bring window to front
        about_win.attributes("-topmost", True)
        about_win.grab_set()

        # Title
        title_label = ctk.CTkLabel(about_win, text="BlueFalcon Shutdown Timer", font=("Arial", 16, "bold"))
        title_label.pack(pady=(20, 5))

        # Version
        version_label = ctk.CTkLabel(about_win, text="Version 1.1", font=("Arial", 12), text_color="gray")
        version_label.pack(pady=(0, 10))

        # Developer Info
        dev_label = ctk.CTkLabel(about_win, text="Developed by: BlueFalcon", font=("Arial", 13))
        dev_label.pack(pady=(5, 2))
        
        email_label = ctk.CTkLabel(about_win, text="Email: Bluefalcon2270@gmail.com", font=("Arial", 12))
        email_label.pack(pady=(0, 15))

        # GitHub Button
        github_url = "https://github.com/bluefalcon2270/bluefalcon-shutdown-timer"
        github_btn = ctk.CTkButton(
            about_win, 
            text="GitHub Repository", 
            width=150, 
            command=lambda: webbrowser.open(github_url)
        )
        github_btn.pack(pady=5)

if __name__ == "__main__":
    app = ShutdownTimerApp()
    app.mainloop()