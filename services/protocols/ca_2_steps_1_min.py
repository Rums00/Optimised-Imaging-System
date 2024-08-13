from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage

import time

class Ca2Steps1Min(BaseProtocol):
    
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage
                 ):
        super(Ca2Steps1Min, self).__init__(fresco_xyz=fresco_xyz,
                                                    z_camera=z_camera,
                                                    images_storage=images_storage)
        self.images_storage = images_storage
        self.pump_index = 1  # todo: fix, temp solution, number of used  pump should be taken from protocol
        #self.manifold_offset = 19800  # todo: setup actual number
        self.solution_portion_in_steps = 50  # todo: make customizable
        self.manifold_offset = 0  # todo: setup actual number
        self.solution_portion_in_steps = 50  # todo: make customizable
        


    def perform(self):
        super(Ca2Steps1Min, self).perform()
        #self.fresco_xyz.manifold_delta(-1*self.manifold_offset)
        session_folder_path = self.images_storage.create_new_session_folder()
        print('Folder ' + session_folder_path)
        
        for row_number in range(0, 1):
        #for row_number in range(0, self.plate_size_96[0] - 2):
            
            start = time.time()
            
        
          
            
            for frame_number in range (0, 170):
    
    		#switch blue light on
                self.fresco_xyz.blue_led_switch(False)
        		#wait 100 ms
                self.hold_position(1)	
                image_after_solution = self.z_camera.fresco_camera.get_current_image()
        		#switch blue light off
                self.hold_position(1)
                self.fresco_xyz.blue_led_switch(True) 
                self.images_storage.save(image_after_solution,
                                                     session_folder_path + '/' + 'PI_a_' + str(row_number) + '_' + str(1) + str(frame_number) + '.png')
                        
                        #timedelta = time.time() - start
                self.hold_position(1)
                print(frame_number)
           
                

               
            #self.fresco_xyz.manifold_delta(-1*self.manifold_offset)         
            #self.fresco_xyz.delta(-1 * self.well_step_96, 0, 0)
        