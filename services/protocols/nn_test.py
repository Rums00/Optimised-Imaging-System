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
from services.extra_functions import ExtraFunctions


 
class TestFocusWhiteBlue(BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(TestFocusWhiteBlue, self).__init__(fresco_xyz=fresco_xyz,
                                                     z_camera=z_camera,
                                                     images_storage=images_storage)
        self.currentWell = [-1, -1]
        self.ef = ExtraFunctions(self.fresco_xyz,self.z_camera,self.images_storage)
        self.images_storage = images_storage
        self.ef.well12_1_coord_x = -16400
        self.ef.well12_1_coord_y = -56900
        self.well_step_96 = 7200
        
    def perform(self):
        self.fresco_xyz.go_to_zero_manifold()
        self.ef.calibrate()
        

        well_list_1=[[7,2], [7,3]]
        #well_list_1  = [[3,4],[4,4],[5,4],[6,4], [7,4], [8,4], [9,4], [10,4]]
        # well_list_2 = [[5, 6], [6, 6], [7, 6], [7, 7], [6, 7], [5,7]]
        # well_list_3 = [[10,7], [10, 6], [10,5], [10, 4]]
        # well_list_4 = [[9, 2], [10, 2], [11, 2]]
        
        self.focus_picture(well_list_1, 60)
        # self.focus_picture(well_list_2, 10)
        # self.focus_picture(well_list_3, 20)
        # self.focus_picture(well_list_4, 20)

    # Function that takes a list of wells formatted in [column, row]
    # Autofocuses and takes pictures and repeats to number of iterations
    def focus_picture(self, well_list, iterations):
        
        session_folder_path = self.images_storage.create_new_session_folder()
        print('Folder ' + session_folder_path)
        
        for i in range (iterations):
            for well in (well_list):
                self.manipulate_well(well)
                self.white_led_focus()
                self.blue_led_picture(session_folder_path, well, i)


    def white_led_focus(self):
        self.z_camera.z_go_to_zero()
        self.z_camera.fresco_camera.set_exposure(5000)
        self.fresco_xyz.white_led_switch(True)
        self.hold_position(1)
        self.z_camera.focus_on_current_object()
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

     
    def manipulate_well(self, well_num):
        #self.ef.calibrate()
        self.ef.travel_to_well(well_num)
        print ("well num")
        print (well_num)
        #do stuff
       
        #autofocus
        #take a pic
        return
     