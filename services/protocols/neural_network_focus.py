#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 17:17:21 2024

@author: rumyanaandonova
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 17:40:03 2024

@author: md1avn
"""

from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
import matplotlib.pyplot as plt
import math
import random
import time
import tensorflow as tf
import cv2
import numpy as np
import operator
from services.extra_functions import ExtraFunctions


class NeuralNetworkFocus (BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(NeuralNetworkFocus, self).__init__(fresco_xyz=fresco_xyz,
                                                     z_camera=z_camera,
                                                     images_storage=images_storage)
        self.currentWell = [-1, -1]
        self.ef = ExtraFunctions(self.fresco_xyz,self.z_camera,self.images_storage)
        self.frescoXYZ = fresco_xyz
        self.images_storage = images_storage
        self.well12_1_coord_x = -12200 #change to your specifications
        self.well12_1_coord_y = -60900
        self.well_step_96 = 7200
        
    def perform(self):
        self.frescoXYZ.blue_led_switch(True)
        self.frescoXYZ.go_to_zero_manifold()
        self.ef.calibrate()
        self.frescoXYZ.white_led_switch(True)

        
#        well_list_1  = [[5,2],[5,3],[5,4], [6,4], [7,4], [7,3], [7,2], [6,2]]
        # well_list_2 = [[5, 6], [5, 7], [6, 7], [6, 6]]
        # well_list_3 = [[10,7], [10, 6], [10,5], [10, 4]]
        # well_list_4 = [[9, 2], [10, 2], [11, 2]]
        well_list_1 = [[2,2], [3,2]]
        
        focus_well_list_1=self.find_focus(well_list_1)
        self.frescoXYZ.white_led_switch(False)
        
        self.focus_blue(well_list_1, focus_well_list_1, 15)
        # self.focus_picture(well_list_2, 20)
        # self.focus_picture(well_list_3, 20)
        # self.focus_picture(well_list_4, 20)

    # Function that takes a list of wells formatted in [column, row]
    # Autofocuses and takes pictures and repeats to number of iterations
    
    def focus_blue (self, well_list, focus_values, iterations):
        session_folder_path = self.images_storage.create_new_session_folder()
        print('Folder ' + session_folder_path)
        
        for i in range (iterations):
            for well, focus_value in zip(well_list, focus_values):
                
                self.ef.travel_to_well(well)
                self.blue_led_focus(focus_value, session_folder_path, well, i)
                

    
    
    def find_focus(self, well_list):

        focus_list = []
        
        for well in well_list:
            self.ef.travel_to_well(well)
            focus = self.calculate_well_focus()           
            focus_list.append(focus)
        print ('Focus list ', focus_list)
        
        return focus_list
        
    def calculate_well_focus (self):
            initial_focus, steps_1 = self.first_focus_attempt()
            focus_2, steps_2, delta_jumps_2, jump_size_2 = self.refine_focus()
            focus = initial_focus + (-1*self.z_camera.one_jump*self.z_camera.auto_focus_delta_number_of_jumps) + steps_1 + focus_2 + (-1*delta_jumps_2*jump_size_2) + steps_2
            return focus
    
    def first_focus_attempt (self):
        self.z_camera.fresco_camera.set_exposure(1500)
        initial_focus = self.z_camera.auto_focus_anchor + self.z_camera.auto_focus_delta_number_of_jumps / 2
        self.z_camera.z_go_to_zero()
        self.frescoXYZ.delta(0, 0, initial_focus)
        # first focus attempt with big steps
        measure_1, steps_1 = self.z_camera.find_offset_for_best_measure(one_jump_size=self.z_camera.one_jump,
                                                               delta_jumps=self.z_camera.auto_focus_delta_number_of_jumps)
#        print('measure_1 = ' + str(measure_1))
#        print('steps_1 = ' + str(steps_1))
        self.frescoXYZ.delta(0, 0, steps_1)
        return initial_focus, steps_1
        
    def refine_focus (self):
        delta_jumps_2 = 10
        jump_size_2 = 2
        focus_2 = (delta_jumps_2 * jump_size_2) / 2
        self.frescoXYZ.delta(0, 0, focus_2)
        # second focus attempt with small steps
        measure_2, steps_2 = self.z_camera.find_offset_for_best_measure(one_jump_size=jump_size_2,
                                                                delta_jumps=delta_jumps_2)
#        print('measure_2 = ' + str(measure_2))
#        print('steps_2 = ' + str(steps_2))
        self.frescoXYZ.delta(0, 0, steps_2)
        return focus_2, steps_2, delta_jumps_2, jump_size_2
    
    def blue_led_focus(self, focus_value, session_folder_path, well, i):
        self.z_camera.z_go_to_zero()
        self.z_camera.fresco_camera.set_exposure(40000)
        self.hold_position(1)
        self.frescoXYZ.blue_led_switch(False)
        self.hold_position(1)
        print('Focus value is', focus_value)
        self.frescoXYZ.delta(0, 0, focus_value + 3)
        self.hold_position(1)
        self.focus_by_model()
        self.hold_position(1)
        image_at_focus = self.z_camera.fresco_camera.get_current_image()
        self.images_storage.save(image_at_focus,
                         session_folder_path + '/' + 'focus_test' + str(well) + '_' + str(i) + '.png')
        self.frescoXYZ.blue_led_switch(True)
        self.hold_position(1)


    def focus_by_model(self):
       
        self.modelTuned = tf.keras.models.load_model('imageRegressionTunedConstrained.h5')
            
        #go back 10 steps and use finely tuned model
#        self.fresco_xyz.delta(0,0,10)
        res = []
        steps_range = 80
        for a in range (steps_range):
            image = self.z_camera.fresco_camera.get_current_image()
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            resize = tf.image.resize(image, (256, 256))
            steps = self.modelTuned.predict(np.expand_dims(resize/255, 0))[0][0]
            print(steps)
            self.frescoXYZ.delta(0,0,-1)
            self.hold_position(1)
            res.append(steps)
            
        print(res)
        steps_down = steps_range - np.argmin(np.array(res))
        self.frescoXYZ.delta(0,0,steps_down)