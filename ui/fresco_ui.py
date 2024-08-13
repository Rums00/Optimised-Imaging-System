from tkinter import BOTH, Tk
import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.fresco_camera import FrescoCamera
from services.protocols_performer import ProtocolsPerformer
from services.images_storage import ImagesStorage
from services.image_processor import ImageProcessor
from PIL import Image, ImageTk
from tkinter import Toplevel

from ui.steps_manual_controller_ui import StepsManualController
from ui.macro_steps_manual_controller_ui import MacroStepsManualController
from ui.initialization_ui import Initialization
from ui.auto_focus_ui import AutoFocus
from ui.functions_ui import Functions
from ui.serial_connection_ui import SerialConnectionView

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


class MainUI(Frame):

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 fresco_camera: FrescoCamera):
        super().__init__()
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.fresco_camera = fresco_camera
        self.image_label = None
        self.number_of_focus_measures_to_show = 50
        self.focus_measures = [0]

        # debug
        self.subplot = None
        self.figure = None

        self.init_ui()

    def init_ui(self):
        self.master.title("Fresco Labs")

        self.pack(fill=BOTH, expand=1)

        steps_manual_controller = StepsManualController(self, fresco_xyz=self.fresco_xyz)
        steps_manual_controller.place(x=0, y=0)

        macro_steps_controller = MacroStepsManualController(self, fresco_xyz=self.fresco_xyz)
        macro_steps_controller.place(x=0, y=130)

        initialization_controller = Initialization(self, fresco_xyz=self.fresco_xyz)
        initialization_controller.place(x=0, y=340)

        auto_focus_controller = AutoFocus(self, fresco_xyz=self.fresco_xyz, z_camera=self.z_camera)
        auto_focus_controller.place(x=0, y=460)

        images_storage = ImagesStorage()
        protocols_performer = ProtocolsPerformer(fresco_xyz=self.fresco_xyz,
                                                 z_camera=self.z_camera,
                                                 images_storage=images_storage)
        functions_controller = Functions(self,
                                         fresco_xyz=self.fresco_xyz,
                                         z_camera=self.z_camera,
                                         protocols_performer=protocols_performer,
                                         images_storage=images_storage)
        functions_controller.place(x=0, y=560)

        serial_port_control_button = tk.Button(self, text='Serial', command=self.open_serial_connection_ui)
        serial_port_control_button.place(x=300, y=0)

        image_array = self.fresco_camera.get_current_image()
        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array).resize((800, 800), Image.ANTIALIAS))
        self.image_label = Label(self, image=camera_image)
        self.image_label.image = camera_image
        self.image_label.place(x=300, y=30)

        # Uncomment to debug focus measure
        # self.init_debug_focus_measure()

        self.after(100, self.update_image)

    def init_debug_focus_measure(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.subplot.plot(self.focus_measures)
        self.figure.set_label('Focus measure')
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=1700, y=50)

    def update_debug_focus_measure(self, image_array):
        measure = self.z_camera.get_focus_measure(image_array)
        self.add_measure(measure)
        self.figure.clf()
        self.subplot = self.figure.add_subplot(111)
        self.subplot.plot(self.focus_measures)
        self.figure.canvas.draw()

    def update_image(self):
        image_array = self.fresco_camera.get_current_image()

        # Uncomment to debug focus measure
        # self.update_debug_focus_measure(image_array)

        camera_image = ImageTk\
            .PhotoImage(image=Image.fromarray(image_array).resize((800, 800), Image.ANTIALIAS))
        self.image_label.configure(image=camera_image)
        self.image_label.image = camera_image

        self.after(20, self.update_image)

    def add_measure(self, measure):
        if len(self.focus_measures) >= self.number_of_focus_measures_to_show:
            self.focus_measures.pop(0)
        self.focus_measures.append(measure)

    def open_serial_connection_ui(self):
        new_window = Toplevel(self)
        new_window.title("Serial connection")
        new_window.geometry("400x250")
        SerialConnectionView(new_window).pack()


def main():
    fresco_xyz = FrescoXYZ()
    fresco_camera = FrescoCamera()
    z_camera = ZCamera(fresco_xyz, fresco_camera)

    root = Tk()
    root.geometry("1800x1200+300+300")
    app = MainUI(fresco_xyz, z_camera, fresco_camera)
    root.mainloop()


if __name__ == '__main__':
    main()
