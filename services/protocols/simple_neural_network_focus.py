from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from services.extra_functions import ExtraFunctions
import matplotlib.pyplot as plt
import math
import random
import time
import tensorflow as tf
import cv2
import numpy as np
import operator



 
class SimpleNeuralNetworkFocus(BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(SimpleNeuralNetworkFocus, self).__init__(fresco_xyz=fresco_xyz,
                                                     z_camera=z_camera,
                                                     images_storage=images_storage)
        self.currentWell = [-1, -1]
        self.ef = ExtraFunctions(self.fresco_xyz,self.z_camera,self.images_storage)
        self.images_storage = images_storage
        self.ef.well12_1_coord_x = -16400
        self.ef.well12_1_coord_y = -56900
        self.well_step_96 = 7200
        
    def perform(self):
    
        self.z_camera.fresco_camera.set_exposure(30000)
        
        
        session_folder_path = self.images_storage.create_new_session_folder()
        print('Folder ' + session_folder_path)
        iterations = 150
#        
        for i in range (iterations):
            self.z_camera.z_go_to_zero()
            self.fresco_xyz.delta(0, 0, -7905)
            self.fresco_xyz.blue_led_switch(False)
            self.hold_position(1)
            self.focus_by_model()
            self.hold_position(1)
            self.fresco_xyz.delta(0, 0, 2)
            self.hold_position(1)
            image_2 = self.z_camera.fresco_camera.get_current_image()
            self.images_storage.save(image_2,
                         session_folder_path + '/' + 'focus_test' + 'well_1' + '_' + str(i) + '.png')
            self.fresco_xyz.delta(1 * self.well_step_96,0, 0)
            self.z_camera.z_go_to_zero()
            self.fresco_xyz.delta(0, 0, -7885)
            self.hold_position(1)
            self.focus_by_model()
            self.hold_position(1)
            self.fresco_xyz.delta(0, 0, 2)
            self.hold_position(1)
            image_1 = self.z_camera.fresco_camera.get_current_image()
            self.images_storage.save(image_1, 
                        session_folder_path + '/' + 'focus_test' + 'well_2' + '_' + str(i) + '.png')
            self.fresco_xyz.delta(-1 * self.well_step_96,0, 0)
            self.fresco_xyz.blue_led_switch(True)
            self.hold_position(12)
            
#        self.z_camera.fresco_camera.set_exposure(50000)
#        self.fresco_xyz.blue_led_switch(False)
#        
#        session_folder_path = self.images_storage.create_new_session_folder()
#        print('Folder ' + session_folder_path)
#        iterations = 100
#        
#        for i in range(iterations):
#            # 5 wells down
#            for well in range(1, 5):
#                self.focus_by_model()
#                self.fresco_xyz.delta(0, 0, 1)
#                self.hold_position(1)
#                image = self.z_camera.fresco_camera.get_current_image()
#                self.images_storage.save(image, 
#                                         session_folder_path + '/' + 'focus_test' + 'well_' + str(well) + '_' + str(i) + '.png')
#                self.fresco_xyz.delta(0, 1 * self.well_step_96, 5)
#    
#            # Move one well across
#            self.fresco_xyz.delta(1 * self.well_step_96, 0, 5)
#    
#            # 5 wells up
#            for well in range(5, 10):
#                self.focus_by_model()
#                self.fresco_xyz.delta(0, 0, 1)
#                self.hold_position(1)
#                image = self.z_camera.fresco_camera.get_current_image()
#                self.images_storage.save(image, 
#                                         session_folder_path + '/' + 'focus_test' + 'well_' + str(well) + '_' + str(i) + '.png')
#                self.fresco_xyz.delta(0, -1 * self.well_step_96, 5)


#        self.z_camera.fresco_camera.set_exposure(50000)
#        self.fresco_xyz.blue_led_switch(False)
#        
#        session_folder_path = self.images_storage.create_new_session_folder()
#        print('Folder ' + session_folder_path)
#        iterations = 240
#        
#        for i in range (iterations):
#            self.hold_position(0.5)
#            self.focus_by_model()
#            self.fresco_xyz.delta(0, 0, 2)
#            self.hold_position(1)
#            image_2 = self.z_camera.fresco_camera.get_current_image()
#            self.images_storage.save(image_2,
#                         session_folder_path + '/' + 'focus_test' + 'well_1' + '_' + str(i) + '.png')
#            self.fresco_xyz.delta(1 * self.well_step_96, 0, 10)
#            self.hold_position(0.5)
#            self.focus_by_model()
#            self.fresco_xyz.delta(0, 0, 2)
#            self.hold_position(1)
#            image_1 = self.z_camera.fresco_camera.get_current_image()
#            self.images_storage.save(image_1, 
#                        session_folder_path + '/' + 'focus_test' + 'well_2' + '_' + str(i) + '.png')
#            self.fresco_xyz.delta(0, 1 * self.well_step_96, 14)
#            self.hold_position(0.5)
#            self.focus_by_model()
#            self.fresco_xyz.delta(0, 0, 2)
#            self.hold_position(1)
#            image_1 = self.z_camera.fresco_camera.get_current_image()
#            self.images_storage.save(image_1, 
#                        session_folder_path + '/' + 'focus_test' + 'well_3' + '_' + str(i) + '.png')
#
#            self.fresco_xyz.delta(-1 * self.well_step_96, 0, 2)
#            self.hold_position(0.5)
#            self.hold_position(1)
#            self.focus_by_model()
#            self.fresco_xyz.delta(0, 0, 2)
#            self.hold_position(1)
#            image_1 = self.z_camera.fresco_camera.get_current_image()
#            self.images_storage.save(image_1, 
#                        session_folder_path + '/' + 'focus_test' + 'well_4' + '_' + str(i) + '.png')
#            self.fresco_xyz.delta(0, -1 * self.well_step_96, -2)
#            self.hold_position(0.5)

                    
        
    def focus_by_model(self):
       
        self.modelTuned = tf.keras.models.load_model('imageRegressionTunedConstrained.h5')
            
        oldsteps = 100
        #go back 10 steps and use finely tuned model
#        self.fresco_xyz.delta(0,0,10)
        for a in range (40):
            image = self.z_camera.fresco_camera.get_current_image()
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            resize = tf.image.resize(image, (256, 256))
            steps = self.modelTuned.predict(np.expand_dims(resize/255, 0))[0][0]
            print(steps)
            if steps <=oldsteps:
                self.fresco_xyz.delta(0,0,-1)
                oldsteps = steps
            else:
                break
            print(steps)
        
     