# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 17:40:03 2024

@author: md1avn
"""

from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from services.fresco_camera import FrescoCamera
import matplotlib.pyplot as plt
import math
import random
import time
from services.extra_functions import ExtraFunctions


 
class TestRobotLongTime(BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(TestRobotLongTime, self).__init__(fresco_xyz=fresco_xyz,
                                                     z_camera=z_camera,
                                                     images_storage=images_storage)
        self.currentWell = [-1, -1]
        self.ef = ExtraFunctions(self.fresco_xyz,self.z_camera,self.images_storage)
        self.images_storage = images_storage
        self.ef.well12_1_coord_x = -16400
        self.ef.well12_1_coord_y = -56900
        self.well_step_96 = 7200
        
    def perform(self):
        self.fresco_xyz.white_led_switch(True)
        self.ef.calibrate()
        

        
        well_list_1  = [[5,2],[5,3],[5,4],[6,4], [7,4], [7,3], [7,2], [6,2]]
        # well_list_2 = [[5, 6], [6, 6], [7, 6], [7, 7], [6, 7], [5,7]]
        # well_list_3 = [[10,7], [10, 6], [10,5], [10, 4]]
        # well_list_4 = [[9, 2], [10, 2], [11, 2]]
        
        self.focus_picture(well_list_1, 10)
        # self.focus_picture(well_list_2, 10)
        # self.focus_picture(well_list_3, 20)
        # self.focus_picture(well_list_4, 20)

    # Function that takes a list of wells formatted in [column, row]
    # Autofocuses and takes pictures and repeats to number of iterations
    def focus_picture(self, well_list, iterations):
        
        session_folder_path = self.images_storage.create_new_session_folder()
        print('Folder ' + session_folder_path)
        
        for i in range (iterations):
            for column_row in (well_list):
                self.manipulate_well(column_row)
                self.z_camera.focus_on_current_object()
                self.hold_position(3)
                image_at_focus = self.z_camera.fresco_camera.get_current_image()
                self.images_storage.save(image_at_focus,
                                         session_folder_path + '/' + 'focus_test' + str(column_row) + '_' + str(i) + '.png')
        
    
        
            # for a in range (100):
            #       self.manipulate_well([1,3])
        #       #self.ef.travel_to_well([1,2])
        #       self.z_camera.focus_on_current_object()
        #       self.hold_position(1)
        #       image_at_focus = self.z_camera.fresco_camera.get_current_image()
        #       self.images_storage.save(image_at_focus,
        #                                session_folder_path + '/' + 'focus_test' + str(1) + '_' + str(3) + '.png')
        #       self.manipulate_well([1,7])
        #       self.z_camera.focus_on_current_object()
        #       #self.ef.travel_to_well([1,2])
        #       self.hold_position(1)
        #       self.images_storage.save(image_at_focus,
        #                                session_folder_path + '/' + 'focus_test' + str(1) + '_' + str(7) + '.png')
        #       self.manipulate_well([12,6])
        #       self.z_camera.focus_on_current_object()
        #       self.hold_position(1)
        #       self.images_storage.save(image_at_focus,
        #                                session_folder_path + '/' + 'focus_test' + str(12) + '_' + str(6) + '.png')
        #       self.manipulate_well([12,2])
        #       self.z_camera.focus_on_current_object()
        #       self.hold_position(1)
        #       self.images_storage.save(image_at_focus,
        #                                session_folder_path + '/' + 'focus_test' + str(12) + '_' + str(2) + '.png')

        #       print (a)
        return
     
    def manipulate_well(self, well_num):
        #self.ef.calibrate()
        self.ef.travel_to_well(well_num)
        print ("well num")
        print (well_num)
        #do stuff
       
        #autofocus
        #take a pic
        return
     
        