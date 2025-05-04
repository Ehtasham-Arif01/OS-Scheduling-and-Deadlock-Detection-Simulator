import tkinter as tk
from tkinter import font, ttk, messagebox
import webbrowser
import subprocess
import platform
import os

class WelcomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS FOR KIDS")
        self.root.geometry("1250x650")
        self.root.configure(bg="#f0f8ff")
        
        try:
            if platform.system() == "Windows":
                self.root.state('zoomed')
            else:
                self.root.attributes('-zoomed', True)
        except:
            self.root.geometry("1250x650")
            
        self.title_font = font.Font(family="Helvetica", size=42, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=18)
        self.button_font = font.Font(family="Verdana", size=16, weight="bold")
        self.dev_font = font.Font(family="Arial", size=12, slant="italic")
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        header_frame = tk.Frame(main_frame, bg="#f0f8ff")
        header_frame.pack(pady=(30, 20))
        
        title_label = tk.Label(header_frame, text="OS FOR KIDS", 
                             font=self.title_font, bg="#f0f8ff", fg="#2c3e50")
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Making Operating Systems Learning Fun and Easy", 
                                font=self.subtitle_font, bg="#f0f8ff", fg="#7f8c8d")
        subtitle_label.pack(pady=(15, 40))
        
        button_frame = tk.Frame(main_frame, bg="#f0f8ff")
        button_frame.pack(pady=30)
        
        scheduling_btn = tk.Button(button_frame, text="CPU Scheduling Simulator", 
                                 font=self.button_font, bg="#3498db", fg="white",
                                 width=30, height=2, bd=0, relief=tk.RAISED,
                                 activebackground="#2980b9",
                                 command=self.run_scheduling)
        scheduling_btn.pack(pady=15, ipadx=20, ipady=5)
        
        deadlock_btn = tk.Button(button_frame, text="Deadlock Simulator", 
                               font=self.button_font, bg="#e74c3c", fg="white",
                               width=30, height=2, bd=0, relief=tk.RAISED,
                               activebackground="#c0392b",
                               command=self.run_deadlock)
        deadlock_btn.pack(pady=15, ipadx=20, ipady=5)
        
        footer_frame = tk.Frame(main_frame, bg="#f0f8ff")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(30, 0))
        
        sep = ttk.Separator(footer_frame, orient='horizontal')
        sep.pack(fill=tk.X, pady=10)
        
        dev_frame = tk.Frame(footer_frame, bg="#f0f8ff")
        dev_frame.pack()
        

                # DEVELOPED BY label with dark styling
        developed_by_label = tk.Label(dev_frame, text="DEVELOPED BY:", 
                             font=("Arial", 10, "bold"), 
                             bg="#2c3e50", fg="#ecf0f1",  # Dark bg, light text
                             padx=5, pady=2)
        developed_by_label.pack(side=tk.LEFT)


        dev1_btn = tk.Button(dev_frame, text=" EHTASHAM ARIF ", 
                            font=self.dev_font, bg="#f0f8ff", fg="#3498db",
                            bd=0, cursor="hand2", 
                            command=lambda: webbrowser.open("https://github.com/Ehtasham-Arif01"))
        dev1_btn.pack(side=tk.LEFT, padx=10)
        
        dev2_btn = tk.Button(dev_frame, text=" AHMED ABDULLAH", 
                            font=self.dev_font, bg="#f0f8ff", fg="#e74c3c",
                            bd=0, cursor="hand2", 
                            command=lambda: webbrowser.open("https://github.com/Ahmed-Abdullah-01"))
        dev2_btn.pack(side=tk.LEFT, padx=10)
        
    def run_scheduling(self):
        self.root.withdraw()
        try:
            # Use full path to python executable and script
            script_path = os.path.join(os.path.dirname(__file__), "scheduler.py")
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Could not start scheduler: {str(e)}")
        
    def run_deadlock(self):
        self.root.withdraw()
        try:
            # Use full path to python executable and script
            script_path = os.path.join(os.path.dirname(__file__), "deadlock.py")
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Could not start deadlock simulator: {str(e)}")

def main():
    root = tk.Tk()
    app = WelcomeApp(root)
    root.mainloop()

if __name__ == "__main__":
    import sys  # Added for sys.executable
    main()