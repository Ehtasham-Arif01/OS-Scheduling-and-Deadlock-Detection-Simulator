import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import os
import sys

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Scheduling Simulator")
        self.root.geometry("1250x650")
        self.processes = []
        self.selected_algo = tk.StringVar(value="FCFS")
        self.backend_path = os.path.join(os.path.dirname(__file__), os.pardir, 'backend', 'scheduler_backend')
        if not os.path.exists(self.backend_path):
            messagebox.showerror("Execution Error", 
                                f"Backend executable not found at: {self.backend_path}\n"
                                f"Compile the C code and place it in the 'backend' folder.")
            return
        self.build_ui()

    def build_ui(self):
        # Left Frame for Controls
        left_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right Frame for Visualization
        self.right_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.SOLID)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Control Panel (Left Side)
        algo_label = tk.Label(left_frame, text="Choose Scheduling Algorithm", fg="white", bg="#2c3e50", font=("Arial", 12, "bold"))
        algo_label.pack(pady=(0,10))

        btn_frame = tk.Frame(left_frame, bg="#2c3e50")
        btn_frame.pack()
        for algo in ["FCFS", "SJF", "SRTF", "PRIORITY", "ROBIN"]:  # Added "SRTF"
            tk.Radiobutton(
            btn_frame,
            text=algo,
            variable=self.selected_algo,
            value=algo,
            command=self.toggle_columns,
            indicatoron=0,
            width=20,
            bg="#3498db",
            fg="white",
            selectcolor="#1abc9c",
            font=("Arial", 12, "bold")
            ).pack(pady=2)

        self.tree = ttk.Treeview(left_frame, columns=("Arrival", "Burst", "Priority"), show="headings", height=7)
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.column("Priority", width=80)
        self.tree.pack(pady=(20, 10))

        # Input fields
        input_frame = tk.Frame(left_frame, bg="#2c3e50")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Arrival Time", bg="#2c3e50", fg="white").grid(row=0, column=0)
        self.entry_arrival = tk.Entry(input_frame, width=10)
        self.entry_arrival.grid(row=0, column=1)

        tk.Label(input_frame, text="Burst Time", bg="#2c3e50", fg="white").grid(row=0, column=2)
        self.entry_burst = tk.Entry(input_frame, width=10)
        self.entry_burst.grid(row=0, column=3)

        self.priority_label = tk.Label(input_frame, text="Priority", bg="#2c3e50", fg="white")
        self.entry_priority = tk.Entry(input_frame, width=10)
        self.priority_label.grid(row=0, column=4)
        self.entry_priority.grid(row=0, column=5)

        tk.Button(left_frame, text="Add Process", command=self.add_process, bg="#1abc9c", fg="white", font=("Arial", 11, "bold"), width=20).pack(pady=5)

        self.quantum_label = tk.Label(left_frame, text="Time Slice", bg="#2c3e50", fg="white")
        self.quantum_entry = tk.Entry(left_frame, width=10)
        tk.Button(left_frame, text="Visualize", command=self.visualize, bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)
        
        # Bottom frame for the two buttons
        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(side=tk.BOTTOM, pady=15)

        # Clear All button
        tk.Button(bottom_frame, text="Clear All", command=self.clear_all, bg="#e74c3c", fg="white", 
                font=("Arial", 12, "bold"), width=15).pack(side=tk.LEFT, padx=5)

        # Exit button
        tk.Button(bottom_frame, text="Exit", command=self.return_to_welcome, bg="#34495e", fg="white", 
                font=("Arial", 12, "bold"), width=15).pack(side=tk.RIGHT, padx=5)
        self.toggle_columns()

    def toggle_columns(self):
        algo = self.selected_algo.get()
        if algo == "PRIORITY":
            self.tree["displaycolumns"] = ("Arrival", "Burst", "Priority")
            self.priority_label.grid()
            self.entry_priority.grid()
        else:
            self.tree["displaycolumns"] = ("Arrival", "Burst")
            self.priority_label.grid_remove()
            self.entry_priority.grid_remove()

        if algo == "ROBIN":
            self.quantum_entry.config(state='normal')
            self.quantum_label.config(state='normal')
            self.quantum_label.pack()
            self.quantum_entry.pack()
        else:
            self.quantum_label.pack_forget()
            self.quantum_entry.pack_forget()

    def add_process(self):
        arrival = self.entry_arrival.get()
        burst = self.entry_burst.get()
        priority = self.entry_priority.get() if self.selected_algo.get() == "PRIORITY" else '0'
        
        if not (arrival.isdigit() and burst.isdigit() and (priority.isdigit() or self.selected_algo.get() != "PRIORITY")):
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return

        pid = f"P{len(self.processes) + 1}"
        self.processes.append({"id": pid, "arrival": int(arrival), "burst": int(burst), "priority": int(priority)})
        self.tree.insert('', 'end', values=(arrival, burst, priority))
        self.entry_arrival.delete(0, tk.END)
        self.entry_burst.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)

    def clear_all(self):
        self.processes.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def visualize(self):
        if not self.processes:
            messagebox.showerror("Error", "No process added.")
            return

        algo = self.selected_algo.get()
        quantum = self.quantum_entry.get() if algo == "ROBIN" else "0"
        
        # Prepare input for C backend
        input_data = f"{algo}\n"
        if algo == "ROBIN":
            input_data += f"{quantum}\n"
        input_data += f"{len(self.processes)}\n"
        for p in self.processes:
            input_data += f"{p['id'][1:]} {p['arrival']} {p['burst']} {p['priority']}\n"
        input_data += "END\n"

        try:
            # Run the C backend
            result = subprocess.run(
                [self.backend_path],
                input=input_data.encode(),
                capture_output=True,
                timeout=30
            )
            
            if result.returncode != 0:
                messagebox.showerror("Backend Error", result.stderr.decode())
                return
                
            output = result.stdout.decode()
            self.parse_and_display_results(output)
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Backend timed out")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run backend: {str(e)}")


    def return_to_welcome(self): 
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Build absolute path to main.py
            main_path = os.path.join(current_dir, "main.py")
    
            # Verify main.py exists before closing current window
            if os.path.exists(main_path):
                self.root.destroy()  # Use self.root instead of root
                subprocess.Popen([sys.executable, main_path])
            else:
                messagebox.showerror("Error", "Could not find main menu program")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to welcome: {str(e)}")

    def parse_and_display_results(self, output):
        # Clear previous results
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Parse output
        lines = output.split('\n')
        execution = []
        metrics = []
        
        for line in lines:
            if line.startswith("Average"):
                metrics.append(line)
            elif line.startswith("Process"):
                try:
                    # Parse both formats:
                    # "Process 1: Start Time = 0, Duration = 2" 
                    # or "Process 1: Start Time = 1, Duration = 2"
                    parts = line.replace("=", "").replace(",", "").split()
                    pid = parts[1].rstrip(':')
                    start_time = int(parts[4])
                    duration = int(parts[6])
                    execution.append((f"P{pid}", start_time, duration))
                except (IndexError, ValueError) as e:
                    print(f"Warning: Could not parse execution step - {line}")
                    continue

        # Draw Gantt Chart
        if execution:
            self.draw_gantt_chart(execution)
        else:
            messagebox.showwarning("No Data", "No execution steps found in backend output")

        # Display Metrics
        metrics_frame = tk.Frame(self.right_frame, bg="white")
        metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(metrics_frame, text="Performance Metrics", font=("Arial", 12, "bold"), 
                bg="white", fg="black").pack(anchor='w')
        
        for metric in metrics:
            tk.Label(metrics_frame, text=metric, font=("Arial", 11), 
                    bg="white", fg="black").pack(anchor='w')

        # Display Execution Steps
        steps_frame = tk.Frame(self.right_frame, bg="white")
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(steps_frame, text="Execution Steps", font=("Arial", 12, "bold"), 
                bg="white", fg="black").pack(anchor='w')
        
        cols = ["Process", "Start Time", "Duration"]
        tree = ttk.Treeview(steps_frame, columns=cols, show='headings', height=min(10, len(execution)))
        
        style = ttk.Style()
        style.configure("Treeview", 
                      background="white", 
                      foreground="black", 
                      fieldbackground="white", 
                      rowheight=25, 
                      font=("Arial", 10))
        style.configure("Treeview.Heading", 
                      font=("Arial", 10, "bold"))
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=100)
        
        for step in execution:
            tree.insert("", "end", values=step)
        
        # Add scrollbars if needed
        if len(execution) > 10:
            scroll_y = ttk.Scrollbar(steps_frame, orient=tk.VERTICAL, command=tree.yview)
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scroll_y.set)
            
            scroll_x = ttk.Scrollbar(steps_frame, orient=tk.HORIZONTAL, command=tree.xview)
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            tree.configure(xscrollcommand=scroll_x.set)
        
        tree.pack(fill=tk.BOTH, expand=True)

    def draw_gantt_chart(self, execution):
        colors = plt.cm.get_cmap("tab20", len(execution) + 1)
        fig, ax = plt.subplots(figsize=(10, 2))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        for i, (pid, st, dur) in enumerate(execution):
            ax.barh(0, dur, left=st, height=0.5, color=colors(i), edgecolor='black')
            ax.text(st + dur / 2, 0, pid, va='center', ha='center', color='white', fontweight='bold')
        
        ax.set_yticks([])
        ax.set_xlabel("Time", color='black')
        ax.set_title("Gantt Chart", color='black')
        ax.tick_params(axis='x', colors='black')
        
        if execution:
            ax.set_xlim(0, max([st + dur for _, st, dur in execution]) + 1)
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=(10, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()