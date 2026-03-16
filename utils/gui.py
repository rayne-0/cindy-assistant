import customtkinter as ctk
import threading
from core.assistant import CindyAssistant

class StatusLight(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = ctk.CTkCanvas(self, width=20, height=20, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack()
        self.circle = self.canvas.create_oval(2, 2, 18, 18, fill="gray", outline="")

    def set_status(self, state: str):
        colors = {
            "idle": "gray",
            "listening": "#00ff00",
            "processing": "#ffaa00",
            "speaking": "#00bbff"
        }
        self.canvas.itemconfig(self.circle, fill=colors.get(state, "gray"))

class CindyOverlay:
    def __init__(self, assistant: CindyAssistant):
        self.assistant = assistant
        self.pending_query = None
        
        # Initialize the CustomTkinter root
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("Cindy Assistant")
        
        # Make the window borderless and always on top
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        
        # Position top center
        window_width = 400
        window_height = 60
        screen_width = self.root.winfo_screenwidth()
        x = (screen_width // 2) - (window_width // 2)
        y = 20
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create UI Elements
        self.frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a", corner_radius=15)
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Status Light
        self.status = StatusLight(self.frame, fg_color="#1a1a1a", width=30)
        self.status.pack(side="left", padx=10)
        
        # Search Entry Bar
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Ask Cindy or type a command...", 
                                  width=280, border_width=0, fg_color="#333333")
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", self.handle_input)
        
        # Close Button
        self.close_btn = ctk.CTkButton(self.frame, text="✖", width=30, fg_color="transparent", 
                                       hover_color="#550000", command=self.hide)
        self.close_btn.pack(side="right", padx=5)
        
    def handle_input(self, event):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.pending_query = f"execute {query}"

    def get_and_clear_query(self):
        q = getattr(self, "pending_query", None)
        self.pending_query = None
        return q

    def update_status_externally(self, state: str):
        """Called by main.py to change the LED indicator during voice interactions."""
        self.status.set_status(state)
            
    def hide(self):
        # We don't destroy, we just hide it so it can be brought back
        self.root.withdraw()
        
    def show(self):
        self.root.deiconify()

    def update(self):
        """Called periodically by the main thread to process GUI events"""
        try:
            self.root.update()
        except:
            pass

# Global reference
overlay_instance = None

def get_overlay(assistant=None):
    global overlay_instance
    if overlay_instance is None and assistant is not None:
        overlay_instance = CindyOverlay(assistant)
    return overlay_instance
