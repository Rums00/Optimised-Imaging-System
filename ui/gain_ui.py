import tkinter as tk
from tkinter.ttk import Frame, Label, Entry
from services.z_camera import ZCamera


class GainUI(Frame):
    def __init__(self, master, z_camera: ZCamera):
        super().__init__(master=master, height=400, width=400)
        self.z_camera = z_camera
        self.gain_entry: Entry = None
        self.init_ui()

    def init_ui(self):
        set_gain_label = Label(self, text='Set gain')
        set_gain_label.place(x=10, y=0)

        self.gain_entry = Entry(self)
        self.gain_entry.place(x=10, y=40)

        set_gain_button = tk.Button(self, text="Set Gain", command=self.set_gain)
        set_gain_button.place(x=10, y=80)

        run_auto_gain_button = tk.Button(self, text="Run Auto Gain", command=self.run_auto_gain)
        run_auto_gain_button.place(x=10, y=120)

    def set_gain(self):
        self.z_camera.fresco_camera.set_gain(float(self.gain_entry.get()))

    def run_auto_gain(self):
        self.z_camera.fresco_camera.set_auto_gain(True)
