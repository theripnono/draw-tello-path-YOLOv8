import tkinter as tk
from tkinter import ttk


class ProgressBarApp:
    def __init__(self, delay_ms=10000):
        self.root = tk.Tk()
        self.root.title("Working on the drone")

        self.progressbar = ttk.Progressbar(mode="indeterminate")
        self.progressbar.place(x=30, y=60, width=200)
        self.progressbar.start()
        stop_button = ttk.Button(self.root, text="Stop", command=self.stop_progress)
        stop_button.place(x=120, y=120)

        self.root.geometry("300x200")
        self.root.after(delay_ms, self.close_window)
        self.root.mainloop()

    def close_window(self):
        self.root.destroy()

    def stop_progress(self):
        self.progressbar.stop()
        self.root.destroy()

