import tkinter as tk
from tkinter import ttk # Imports notebook to be used for tab creation

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Spin Launch Analyses Tool')
        self.root.geometry('1080x720')

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.frame1 = tk.Frame(self.notebook, width=1080, height=720)
        self.frame2 = tk.Frame(self.notebook, width=1080, height=720)
        self.frame3 = tk.Frame(self.notebook, width=1080, height=720)
        self.frame4 = tk.Frame(self.notebook, width=1080, height=720)

        # Pack is not strictly necessary here; notebook handles layout
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()

        self.notebook.add(self.frame1, text='Parameters')
        self.notebook.add(self.frame2, text='Spin Up')
        self.notebook.add(self.frame3, text='Trajectory')
        self.notebook.add(self.frame4, text='Structural Analyses')

        self.root.mainloop()


