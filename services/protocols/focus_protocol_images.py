# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:37:56 2024

@author: user
"""

from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
import matplotlib.pyplot as plt
import math
import random
import time
from services.extra_functions import ExtraFunctions

class FocusProtocolImages (BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(FocusProtocolImages, self).__init__(fresco_xyz=fresco_xyz,
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
        self.fresco_xyz.white_led_switch(True)
        self.fresco_xyz.go_to_zero_manifold()
        self.ef.calibrate()
        
        
#        well_list_1  = [[5,2],[5,3],[5,4], [6,4], [7,4], [7,3], [7,2], [6,2]]
        # well_list_2 = [[5, 6], [5, 7], [6, 7], [6, 6]]
        # well_list_3 = [[10,7], [10, 6], [10,5], [10, 4]]
        # well_list_4 = [[9, 2], [10, 2], [11, 2]]
        well_list_1 = [[2,2], [2,3]]
        
        focus_well_list_1=self.find_focus(well_list_1)
        
        
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
                self.white_led_focus(focus_value)
                self.blue_led_picture(session_folder_path, well, i)
                

    
#    def focus_picture(self, well_list, focus_values, iterations):
#        
#        session_folder_path = self.images_storage.create_new_session_folder()
#        print('Folder ' + session_folder_path)
#        
#        for i in range (iterations):
#            for well, focus_value in zip(well_list, focus_values):
#                self.z_camera.z_go_to_zero()
#                self.ef.travel_to_well(well)
#                self.frescoXYZ.delta(0, 0, focus_value + 8)
#                self.refine_focus()
#                self.hold_position(2)
#                image_at_focus = self.z_camera.fresco_camera.get_current_image()
#                self.images_storage.save(image_at_focus,
#                                         session_folder_path + '/' + 'focus_test' + str(well) + '_' + str(i) + '.png')
#        return
    
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
    
    def white_led_focus(self, focus_value):
        self.z_camera.z_go_to_zero()
        self.z_camera.fresco_camera.set_exposure(1500)
        self.fresco_xyz.white_led_switch(True)
        self.hold_position(1)
        self.frescoXYZ.delta(0, 0, focus_value + 8)
        self.refine_focus()
        self.hold_position(1)

    def blue_led_picture(self, session_folder_path, well, i):
        self.fresco_xyz.white_led_switch(False)
        self.hold_position(1)
        self.z_camera.fresco_camera.set_exposure(50000)
        self.fresco_xyz.blue_led_switch(False)
        self.hold_position(1)
        image_at_focus = self.z_camera.fresco_camera.get_current_image()
        self.images_storage.save(image_at_focus,
                         session_folder_path + '/' + 'focus_test' + str(well) + '_' + str(i) + '.png')
        self.fresco_xyz.blue_led_switch(True)
        self.hold_position(1)
        