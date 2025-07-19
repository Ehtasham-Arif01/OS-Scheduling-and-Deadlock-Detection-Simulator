# 🧠 OS Scheduling & Deadlock Detection Simulator
![Screenshot from 2025-05-04 15-29-13](https://github.com/user-attachments/assets/182f5092-f14c-4503-a599-f186f709e4e1)

##  ![Screenshot from 2025-05-04 15-31-34](https://github.com/user-attachments/assets/5082325a-8a2c-45e7-aa55-9916eadacebd)
Features
![Screenshot from 2025-05-04 15-45-03](https://github.com/user-attachments/assets/d2007aa6-91cd-4134-8f14-d82a63d00088)

### ✅ CPU Scheduling Simulator
- Add custom processes with burst time, arrival time, priority, etc.
- Choose from scheduling algorithms:
  - FCFS (First-Come, First-Served)
  - SJF (Shortest Job First)
  - Priority Scheduling
  - Round Robin (with quantum)
- Generates and displays dynamic **Gantt Charts**
- Handles idle time between processes

### ✅ Deadlock Detection Module
- Input: Allocation Matrix, Max Matrix, Available Resources
- Implements **Banker's Algorithm**
- Detects **Deadlocks** or shows **Safe Sequence**
- Visualizes results using dynamic **resource allocation graphs**

---

## 🛠️ Tech Stack

| Component     | Technology                     |
|--------------|---------------------------------|
| Backend       | C Language (scheduler.c, dead.c) |
| Frontend      | Python with Tkinter + NetworkX |
| Communication | `subprocess` (no static input/output files) |
| Visualization | Gantt Charts (Tkinter Canvas), Graphs (NetworkX) |

---

## 📁 Folder Structure

.os_simulator
├── backend
│   ├── dead.c
│   ├── deadlock
│   ├── scheduler_backend
│   └── scheduler.c
└── frontend
    ├── deadlock.py
    ├── main.py
    └── scheduler.py

2 directories, 7 files

///////////////////////////////////////////////////////////////////////////////////

---

## 💻 Setup & Run Instructions

### Prerequisites:
- GCC (to compile C files)
- Python 3.x
- Python packages: `networkx`, `tkinter` , `matplotlib` (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/Ehtasham-Arif01/os-simulator.git

## 🚀 Features

### ✅ CPU Scheduling Simulator
- Add custom processes with burst time, arrival time, priority, etc.
- Choose from scheduling algorithms:
  - FCFS (First-Come, First-Served)
  - SJF (Shortest Job First)
  - Priority Scheduling
  - Round Robin (with quantum)
- Generates and displays dynamic **Gantt Charts**
- Handles idle time between processes

### ✅ Deadlock Detection Module
- Input: Allocation Matrix, Max Matrix, Available Resources
- Implements **Banker's Algorithm**
- Detects **Deadlocks** or shows **Safe Sequence**
- Visualizes results using dynamic **resource allocation graphs**

---

## 💻 Setup & Run Instructions

### Prerequisites:
- GCC (to compile C files)
- Python 3.x
- Python packages: `networkx`, `tkinter` (usually pre-installed), `matplotlib` (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/os-simulator.git
cd os-simulator

//////////////////////////////////////////////
2. Compile the Backend
cd backend
gcc scheduler.c -o scheduler
gcc dead.c -o deadlock

3. Run the GUI
cd ../frontend
python gui.py
///////////////////////////////////////////////////




