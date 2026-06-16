# Version: v1.0
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
        self.title("BlueFalcon Shutdown Timer v1.0")
        self.geometry("450x380")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.timer_running = False
        self.time_left = 0

        # Timer Display Label
        self.timer_label = ctk.CTkLabel(self, text="--:--", font=("Courier", 40, "bold"))
        self.timer_label.pack(pady=(35, 25))

        # Minutes Input Entry
        self.minutes_entry = ctk.CTkEntry(self, placeholder_text="Minutes", width=200, justify="center")
        self.minutes_entry.pack(pady=10)

        # Action Dropdown Combobox
        self.action_var = ctk.StringVar(value="Shutdown")
        self.action_combo = ctk.CTkComboBox(
            self, 
            values=["Shutdown", "Restart", "Hibernate", "Sleep"], 
            variable=self.action_var, 
            width=200
        )
        self.action_combo.pack(pady=10)

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Start Button
        self.start_btn = ctk.CTkButton(self.button_frame, text="Start Timer", width=120, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=10)

        # Cancel Button
        self.cancel_btn = ctk.CTkButton(self.button_frame, text="Cancel Timer", width=120, command=self.cancel_timer)
        self.cancel_btn.grid(row=0, column=1, padx=10)

        # About / Info Button
        self.info_btn = ctk.CTkButton(
            self, 
            text="ℹ️", 
            width=32, 
            height=32, 
            corner_radius=16, 
            fg_color="transparent", 
            hover_color="gray25",
            font=("Arial", 16),
            command=self.open_about_window
        )
        self.info_btn.place(relx=0.95, rely=0.95, anchor="se")

    def update_timer_display(self):
        if self.timer_running and self.time_left > 0:
            minutes = math.floor(self.time_left / 60)
            seconds = self.time_left % 60
            self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
            self.after(1000, self.update_timer_display)
        elif self.time_left <= 0 and self.timer_running:
            self.timer_label.configure(text="00:00")
            self.timer_running = False

    def start_timer(self):
        try:
            minutes = int(self.minutes_entry.get())
            if minutes <= 0:
                return
                
            seconds = minutes * 60
            action = self.action_var.get()
            
            # Execute Windows OS commands
            if action == "Shutdown":
                os.system(f"shutdown /s /t {seconds}")
            elif action == "Restart":
                os.system(f"shutdown /r /t {seconds}")
            elif action == "Hibernate":
                # Windows hibernate does not natively support a timeout parameter via cmd.
                # A common workaround is scheduling it or just executing immediately.
                os.system(f"timeout /t {seconds} /nobreak && shutdown /h")
            elif action == "Sleep":
                os.system(f"timeout /t {seconds} /nobreak && rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            # Update GUI state
            self.time_left = seconds
            self.timer_running = True
            self.update_timer_display()
            self.minutes_entry.configure(state="disabled")
            self.action_combo.configure(state="disabled")
            self.start_btn.configure(state="disabled")

        except ValueError:
            self.timer_label.configure(text="Error")

    def cancel_timer(self):
        # Abort system shutdown/restart
        os.system("shutdown /a")
        
        # Reset GUI state
        self.timer_running = False
        self.timer_label.configure(text="--:--")
        self.minutes_entry.configure(state="normal")
        self.action_combo.configure(state="normal")
        self.start_btn.configure(state="normal")
        self.minutes_entry.delete(0, 'end')

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
        version_label = ctk.CTkLabel(about_win, text="Version 1.0", font=("Arial", 12), text_color="gray")
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