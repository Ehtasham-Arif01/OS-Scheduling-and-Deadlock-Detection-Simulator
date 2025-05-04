import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global state
available = []
processes = []  # List of dicts: {name, allocation, max, need, priority}
resource_count = 0
deadlock_flag = False  # Indicates if last run detected a deadlock

# Helper to clear input fields
def clear_fields():
    entry_available.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_allocation.delete(0, tk.END)
    entry_max.delete(0, tk.END)
    entry_priority.delete(0, tk.END)

# Clear everything
def clear_all():
    global available, processes, resource_count, deadlock_flag
    available = []
    processes = []
    resource_count = 0
    deadlock_flag = False
    clear_fields()
    log.delete('1.0', tk.END)
    ax.clear()
    ax.set_title("Resource Allocation Graph", fontsize=12)
    canvas.draw()
    log.insert(tk.END, "[+] All data cleared\n")

# Exit application
def exit_app():
    root.destroy()

# Calculate need from allocation and max
def calculate_need(allocation, max_demand):
    return [m - a for a, m in zip(allocation, max_demand)]

# Validate input is comma-separated integers
def validate_input(input_str, field_name):
    if not input_str.strip():
        messagebox.showerror("Input Error", f"{field_name} cannot be empty.")
        return None
    try:
        return list(map(int, input_str.split(',')))
    except ValueError:
        messagebox.showerror("Input Error", f"{field_name} must be integer values separated by commas.")
        return None

# Set available resources and detect resource count
def set_available():
    global available, resource_count
    input_str = entry_available.get().strip()
    vals = validate_input(input_str, "Available resources")
    if vals is None:
        return
    
    if len(vals) == 0:
        messagebox.showerror("Input Error", "Enter at least one resource value.")
        return
    
    available = vals
    resource_count = len(available)
    log.insert(tk.END, f"[+] Available resources set: {available}\n")
    entry_available.delete(0, tk.END)
    update_graph()

# Add a new process
def add_process():
    global resource_count
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("Input Error", "Enter process name.")
        return
    
    alloc_str = entry_allocation.get().strip()
    max_str = entry_max.get().strip()
    prio_text = entry_priority.get().strip()
    
    allocation = validate_input(alloc_str, "Allocation")
    max_demand = validate_input(max_str, "Max Demand")
    if allocation is None or max_demand is None:
        return
    
    try:
        priority = int(prio_text) if prio_text else 0
    except ValueError:
        messagebox.showerror("Input Error", "Priority must be an integer.")
        return
    
    if resource_count == 0:
        messagebox.showerror("Input Error", "Set available resources first.")
        return
    
    if len(allocation) != resource_count or len(max_demand) != resource_count:
        messagebox.showerror("Input Error", f"Provide exactly {resource_count} values for Allocation and Max.")
        return
    
    # Check if allocation exceeds max demand
    for a, m in zip(allocation, max_demand):
        if a > m:
            messagebox.showerror("Input Error", "Allocation cannot exceed Max Demand.")
            return
    
    need = calculate_need(allocation, max_demand)
    processes.append({
        'name': name,
        'allocation': allocation,
        'max': max_demand,
        'need': need,
        'priority': priority
    })
    log.insert(tk.END, f"[+] Process {name} added: alloc={allocation}, max={max_demand}, need={need}, prio={priority}\n")
    clear_fields()
    update_graph()

# Update resource allocation graph
def update_graph():
    ax.clear()
    G = nx.DiGraph()

    # Add resource nodes
    for i, res in enumerate(available):
        G.add_node(f"R{i}", color='#3498db', type='resource')

    # Add process nodes and edges
    for p in processes:
        G.add_node(p['name'], color='#2ecc71', type='process')
        # Allocation edges (solid) - only when allocation > 0
        for i, alloc in enumerate(p['allocation']):
            if alloc > 0:
                G.add_edge(f"R{i}", p['name'])
        # Request edges (dashed) - only when need > 0
        for i, need in enumerate(p['need']):
            if need > 0:
                G.add_edge(p['name'], f"R{i}")

    # Positions
    pos = nx.spring_layout(G, seed=42)

    # Draw edges - separate solid (allocation) and dashed (request)
    allocation_edges = [(u, v) for u, v in G.edges() if G.nodes[u]['type'] == 'resource']
    request_edges = [(u, v) for u, v in G.edges() if G.nodes[u]['type'] == 'process']
    
    nx.draw_networkx_edges(G, pos, edgelist=allocation_edges, 
                         ax=ax, edge_color='#95a5a6', width=2, style='solid')
    nx.draw_networkx_edges(G, pos, edgelist=request_edges,
                         ax=ax, edge_color='#95a5a6', width=2, style='dashed')

    # Draw resource nodes as squares
    resource_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'resource']
    resource_colors = [G.nodes[n]['color'] for n in resource_nodes]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=resource_nodes,
        node_shape='s',
        node_color=resource_colors,
        node_size=1200,
        ax=ax
    )

    # Draw process nodes as circles
    process_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'process']
    process_colors = [G.nodes[n]['color'] for n in process_nodes]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=process_nodes,
        node_shape='o',
        node_color=process_colors,
        node_size=1200,
        ax=ax
    )

    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold', font_color='black')

    # If deadlock detected, overlay label
    if deadlock_flag:
        ax.text(0.5, 0.5, "DEADLOCK", fontsize=30, fontweight='bold',
                color='red', ha='center', va='center', transform=ax.transAxes)

    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    ax.set_title("Resource Allocation Graph\nsolid line=Allocated | Dashed line=Requesting\n", fontsize=12, color='black')
    canvas.draw()

def return_to_welcome():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Build absolute path to main.py
        main_path = os.path.join(current_dir, "main.py")
        
        # Verify main.py exists before closing current window
        if os.path.exists(main_path):
            root.destroy()
            subprocess.Popen([sys.executable, main_path])
        else:
            messagebox.showerror("Error", "Could not find main menu program")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to return to welcome: {str(e)}")


# Run Banker's algorithm via C backend
def run_bankers():
    global deadlock_flag
    if resource_count == 0:
        messagebox.showerror("Error", "Set available resources first.")
        return

    if len(processes) == 0:
        messagebox.showerror("Error", "Add at least one process.")
        return

    exe = os.path.join(os.path.dirname(__file__), os.pardir, 'backend', 'deadlock')
    if not os.path.exists(exe):
        messagebox.showerror("Execution Error", f"Backend executable not found: {exe}")
        return

    # Construct input for C backend
    lines = [" ".join(map(str, available))]
    for p in processes:
        alloc = " ".join(map(str, p['allocation']))
        maxd = " ".join(map(str, p['max']))
        lines.append(f"{p['name']} {alloc} {maxd}")
    lines.append("END")
    input_data = "\n".join(lines) + "\n"

    # Run subprocess
    try:
        result = subprocess.run([exe], input=input_data.encode(), capture_output=True, timeout=10)
        if result.returncode != 0:
            messagebox.showerror("Execution Error", result.stderr.decode())
            deadlock_flag = False
            return
        output = result.stdout.decode().lower()
        log.insert(tk.END, output + "\n")

        # Determine if deadlock occurred
        deadlock_flag = "deadlock state" in output or "deadlock" in output
        update_graph()
    except subprocess.TimeoutExpired:
        messagebox.showerror("Execution Error", "Backend process timed out.")
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Deadlock Simulation GUI")
root.geometry("1250x650")  # Window size
root.configure(bg="#1e272e")

# Left Panel (Inputs + Log)
left_frame = tk.Frame(root, bg="#34495e")
left_frame.place(x=10, y=10, width=660, height=580)

# Input section
tk.Label(left_frame, text="Available Resources (comma-separated):",
         bg="#34495e", fg="white", font=('Arial', 10, 'bold')).pack(anchor='w')
entry_available = tk.Entry(left_frame, bg="#2c3e50", fg="white", insertbackground='white')
entry_available.pack(fill='x', pady=5)
tk.Button(left_frame, text="Set Available", bg="#16a085",
          fg="white", font=('Arial', 10, 'bold'), command=set_available).pack(pady=5)

fields = ["Process Name", "Allocation (comma-separated)",
          "Max Demand (comma-separated)", "Priority"]
entries = {}
for f in fields:
    tk.Label(left_frame, text=f, bg="#34495e", fg="white", font=('Arial', 10, 'bold')).pack(anchor='w')
    ent = tk.Entry(left_frame, bg="#2c3e50", fg="white", insertbackground='white')
    ent.pack(fill='x', pady=2)
    entries[f] = ent
entry_name = entries['Process Name']
entry_allocation = entries['Allocation (comma-separated)']
entry_max = entries['Max Demand (comma-separated)']
entry_priority = entries['Priority']

# Add process button
tk.Button(left_frame, text="Add Process", bg="#27ae60",
          fg="white", font=('Arial', 10, 'bold'), command=add_process).pack(pady=5)

# Log section
log = scrolledtext.ScrolledText(left_frame, bg="#2c3e50",
                                fg="white", font=("Consolas", 10), height=12)
log.pack(fill='both', expand=True, padx=10, pady=10)

# Right Panel (Graph)
right_frame = tk.Frame(root, bg="white")
right_frame.place(x=680, y=10, width=690, height=580)

fig, ax = plt.subplots(figsize=(6.2, 5.8), dpi=100, facecolor='white')
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill='both', expand=True)

# Button Panel at bottom
button_frame = tk.Frame(root, bg="#1e272e")
button_frame.place(x=10, y=600, width=1350, height=40)

# Buttons with equal width
button_width = 1350 // 3  # Divide space equally among 3 buttons

run_btn = tk.Button(button_frame, text="Run Banker's Algorithm",
                    bg="#2980b9", fg="white", font=('Arial', 14, 'bold'), 
                    command=run_bankers)
run_btn.pack(side='left', fill='both', expand=True, padx=2)

clear_btn = tk.Button(button_frame, text="Clear All",
                     bg="#e74c3c", fg="white", font=('Arial', 13, 'bold'), 
                     command=clear_all)
clear_btn.pack(side='left', fill='both', expand=True, padx=2)

exit_btn = tk.Button(button_frame, text="Exit",
                    bg="#f39c12", fg="white", font=('Arial', 13, 'bold'), 
                    command=return_to_welcome)
exit_btn.pack(side='left', fill='both', expand=True, padx=2)

root.mainloop()