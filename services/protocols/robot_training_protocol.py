# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:52:10 2023

@author: md1avn
"""
import tkinter as tk
from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
import matplotlib.pyplot as plt
import math
import random
import time
import operator
import tensorflow as tf
import cv2
import numpy as np
 
class RobotTrainingProtocol(BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(RobotTrainingProtocol, self).__init__(fresco_xyz=fresco_xyz,
                                                     z_camera=z_camera,
                                                     images_storage=images_storage)
        self.images_storage = images_storage
        self.number_of_stacks = 100
        self.stack_size = 30
        self.image_prefix = 'S_'
        self.position =[0, 0]
        self.step_size = [1, 1, 1]
        self.start_position = [0,0]
        self.end_position = [0,0]
        self.exp = 0
        self.show_form()
        
        
    def left(self):
        self.position[0] -= self.step_size[2]
        #self.fresco_xyz.delta(0, 0, 0)
        
    def right(self):
        self.position[0] += self.step_size

    def up(self):
        self.position[1] += self.step_size[2]
        self.fresco_xyz.delta(0,0,-1*self.step_size[2])
        
    def down(self):
        self.position[1] -= self.step_size[2]
        self.fresco_xyz.delta(0,0,self.step_size[2])
        
    def save_position(self):
        self.start_position = [self.position[0], self.position[1]]
        print (self.start_position)
        
    def save_top_position(self):
        self.end_position = [self.position[0], self.position[1]]   
    
    def run_protocol(self):
        print("run training")
        #move to start
        delta = self.position[1] - self.start_position[1]
        self.fresco_xyz.delta(0,0,delta)
        self.position[1] = self.start_position[1]
        #make folder
        self.exp += 1
        folder_name = self.images_storage.create_new_session_folder()

        
        number_of_steps = (self.end_position[1]-self.start_position[1])/self.step_size[2]
        print (number_of_steps)
        for a in range(int(number_of_steps)):
            self.up()
            self.hold_position(0.5)
            image = self.z_camera.fresco_camera.get_current_image()
           
            self.images_storage.save(image, folder_name + '/' 'im' + str(a) + '.png')
            self.hold_position(0.2)
            #make a pic
        
        #move randomly the cells
        #repeate 10 times
        
    def show_form(self):
        # code to show form with buttons and handle button presses
        # create a new window
        window = tk.Tk()
        window.title("Robot Controller")

        # create the buttons and add their callbacks
        left_button = tk.Button(window, text="Left", command=self.left)
        right_button = tk.Button(window, text="Right", command=self.right)
        up_button = tk.Button(window, text="Up", command=self.up)
        down_button = tk.Button(window, text="Down", command=self.down)
        save_button = tk.Button(window, text="Save Bottom Position", command=self.save_position)
        save_up_button = tk.Button(window, text="Save Top Position", command=self.save_top_position)
        run_button = tk.Button(window, text="Run Protocol", command=self.run_protocol)
        
        focus_button = tk.Button(window, text="Focus", command=self.focus)

        # add the buttons to the window
        left_button.pack(side=tk.LEFT)
        right_button.pack(side=tk.LEFT)
        up_button.pack(side=tk.TOP)
        down_button.pack(side=tk.TOP)
        save_up_button.pack(side=tk.TOP)
        save_button.pack(side=tk.BOTTOM)
        run_button.pack(side=tk.BOTTOM)
        focus_button.pack(side=tk.BOTTOM)
        # start the GUI event loop
        window.mainloop()
        
        
        
    def find_offset_for_best_measure(self, one_jump_size: int, delta_jumps: int) -> (int, int):
        focus_measure_data_points = []
        for jump_index in range(0, delta_jumps):
            pixels_array = self.z_camera.fresco_camera.get_current_image()
            measure = self.z_camera.get_focus_measure(pixels_array)
            focus_measure_data_points.append(measure)
            #self.frescoXYZ.delta(0, 0, -1 * one_jump_size)
            self.up()
            time.sleep(0.5)
        max_index, max_value = max(enumerate(focus_measure_data_points), key=operator.itemgetter(1))
        number_of_steps_back = (delta_jumps - max_index + 1) * one_jump_size
        
        
        
        return max_value, number_of_steps_back

    def focus_by_model(self):
       
        
        self.model = tf.keras.models.load_model('imageRegression2.h5')
        self.modelTuned = tf.keras.models.load_model('imageRegressionTunedConstrained.h5')
        oldsteps = 100
        #first we go with rough model to find approximate position
#        while True:
#        #for a in range (20):
#            
#            image = self.z_camera.fresco_camera.get_current_image()
#            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
#            resize = tf.image.resize(image, (256, 256))
#            steps = self.model.predict(np.expand_dims(resize/255, 0))[0][0]
#            print (steps)
#            if steps <oldsteps:
#                self.fresco_xyz.delta(0,0,(-1)*steps)
#                oldsteps = steps
#            else:
#                break
#

            
        oldsteps = 100
        #go back 10 steps and use finely tuned model
#        self.fresco_xyz.delta(0,0,10)
        for a in range (40):
            image = self.z_camera.fresco_camera.get_current_image()
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
#
#            image2 = self.z_camera.fresco_camera.get_current_image()
#            image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2RGB)

#            image = cv2.vconcat([image1, image2])
            resize = tf.image.resize(image, (256, 256))
            steps = self.modelTuned.predict(np.expand_dims(resize/255, 0))[0][0]
            print(steps)
            if steps <=oldsteps:
                self.fresco_xyz.delta(0,0,-1)
                oldsteps = steps
            else:
                break
            print(steps)
        
    def focus(self):
        print("focusing")
        self.focus_by_model()
        return
        print(self.position[1])
        #move to start
        delta = self.position[1] - self.start_position[1]
        self.fresco_xyz.delta(0,0,delta)
        self.position[1] -= delta
        
        
        
        #self.frescoXYZ.delta(0, 0, self.auto_focus_anchor + self.auto_focus_delta_number_of_jumps / 2)
        # first focus attempt with big steps
        number_of_steps = self.end_position[1]-self.start_position[1]
        measure_1, steps_1 = self.find_offset_for_best_measure(one_jump_size=1,
                                                               delta_jumps=number_of_steps)
        
        
        self.fresco_xyz.delta(0, 0, steps_1)
        self.position[1] -= steps_1
        print(self.position[1])
