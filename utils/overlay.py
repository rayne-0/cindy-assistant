import tkinter as tk
from utils.tasks import get_tasks, remove_task

class TodoOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cindy Todo List")
        
        # Make the window always on top
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True) # Remove window borders
        
        # Transparency (alpha between 0.0 and 1.0)
        self.root.attributes("-alpha", 0.8)
        
        self.root.configure(bg="#2b2b2b")
        
        # Position in top left corner
        window_width = 300
        window_height = 400
        x = 20
        y = 50
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Header
        header = tk.Label(self.root, text="To-Do List", font=("Segoe UI", 16, "bold"), bg="#1a1a1a", fg="white", pady=10)
        header.pack(fill=tk.X)
        
        # Container for tasks
        self.tasks_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close Button
        close_btn = tk.Button(self.root, text="Close", command=self.close_overlay, bg="#cc0000", fg="white", font=("Segoe UI", 10, "bold"), borderwidth=0)
        close_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        self.refresh_tasks()

    def refresh_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
            
        tasks = get_tasks()
        if not tasks:
            lbl = tk.Label(self.tasks_frame, text="✓ No tasks to do!", font=("Segoe UI", 12), bg="#2b2b2b", fg="white")
            lbl.pack(anchor="w", pady=5)
        else:
            for i, task in enumerate(tasks):
                var = tk.IntVar()
                chk = tk.Checkbutton(self.tasks_frame, text=task, variable=var, 
                                     command=lambda idx=i: self.check_task(idx),
                                     font=("Segoe UI", 12), bg="#2b2b2b", fg="white",
                                     selectcolor="#4a4a4a", activebackground="#2b2b2b", activeforeground="white")
                chk.pack(anchor="w", pady=2)

    def check_task(self, index):
        remove_task(index)
        self.refresh_tasks()
                
    def close_overlay(self):
        self.root.destroy()
        
    def start(self):
        self.root.mainloop()

def show_overlay():
    overlay = TodoOverlay()
    overlay.start()

if __name__ == "__main__":
    show_overlay()
