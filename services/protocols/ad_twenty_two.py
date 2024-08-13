from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
#from services.protocols.cell_passaging import CellPassaging
from services.protocols.base_protocol import BaseProtocol 
from services.extra_functions import ExtraFunctions 
#from services.sc_ad_twenty_two import ScAdTwentyTwo
from datetime import datetime
#from services.webcam_image import WebcamImage 
import datetime
#from services.protocol_state_manager import ProtocolStateManager
import os


class AdTwentyTwo(BaseProtocol):
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage
                 ):
        # super(NewAd, self).__init__(fresco_xyz=fresco_xyz,
        #                                              z_camera=z_camera, images_storage=images_storage)
        self.fresco_xyz = fresco_xyz
        self.images_storage = images_storage
        self.z_camera = z_camera 
        self.extra_functions = ExtraFunctions(fresco_xyz,z_camera,images_storage)
        #self.wcImage = WebcamImage(path='path/to/image', cam_port=0, name='Webcam', cam=0, ret=False, image=None)
        #self.protocol_state_manager = ProtocolStateManager(save_folder=r'C:\Users\heath\Documents\FrescoM-master')
        
        

    def addition(self):
        skip_coordinates = [[12,1]]
        target_coords = self.extra_functions.generate_coordinates(1,12,1,8, skip_coordinates)
        
        for x in target_coords:
            self.extra_functions.travel_to_well(x)
            self.fresco_xyz.delta_pump(6, -350)
            self.hold_position(1)
            self.fresco_xyz.delta_pump(4, 40)
            
            self.fresco_xyz.manifold_delta(-self.lift)
            self.hold_position(1)
            self.fresco_xyz.delta_pump(4,-5)
            self.hold_position(1)
            self.fresco_xyz.manifold_delta(self.lift)
            self.hold_position(1)
            print('1st dose RA Applied', self.extra_functions.get_current_time())
            

    def calibrate(self):
        print("Experiment #22 AD Start Date and Time is", self.extra_functions.get_current_time())
        self.fresco_xyz.go_to_zero_manifold()
        self.hold_position(0.5)
        self.fresco_xyz.go_to_zero()
        self.hold_position(0.5)
        self.extra_functions.move_to_well_12_1()
        self.hold_position(1)
        #self.lid_up()
        self.fresco_xyz.manifold_delta(self.down) #moves to pipetting height, 
                                                    #needs to move to a well after
        
################################################################################
    def perform(self):
        #conditions = ScAdTwentyTwo(self.fresco_xyz, self.z_camera, self.images_storage)
       # conditions.sorting()
        session_folder_path = self.images_storage.create_new_session_folder()
        current_time = self.extra_functions.get_current_time()
    
        self.down = 3250 #was6000
        self.lift = 2500  #changed from 3000
        

        self.extra_functions.calibrate()
        
        ###remove all media then add in RA 
        self.addition()
        #self.hold_position(1)
        print('All wells recieved RA', self.extra_functions.get_current_time())
        self.fresco_xyz.manifold_delta(-self.lift)
        self.hold_position(3)
        self.extra_functions.travel_to_lid()
        self.hold_position(3)
        self.extra_functions.lid_down() #lid down
        
        print('Plate at lid & holding', self.extra_functions.get_current_time())
        
        #self.hold_position(3590) #3590hold for 1hr
        self.extra_functions.lid_up()
        self.hold_position(1)
        self.extra_functions.calibrate()
        
        self.hold_position(1)
        print('Loop beginning', self.extra_functions.get_current_time())
        self.hold_position(1)


#####EDIT TO APPLY TO ALL WELL AND THEN START CONDITIONS 

       # ###START CONDITIONS 
       #  # Initialize current index to 0 if no saved state file exists
       #  # Load saved state if available
       #  self.protocol_state_manager.load_state()

         
       #  if not os.path.exists(r"C:\Users\heath\Documents\FrescoM-master\protocol_state.pkl"):
       #      print('No state file found, starting from the beginning')
       #      self.protocol_state_manager.update_current_index(0)
       #  else:
       #      print('State file found, continuing from the saved state')

            
       #  #for a in range(len(conditions.deltaTime)):
       #  for a in range(self.protocol_state_manager.current_index, len(conditions.deltaTime)):
       #      for x in range(6): #CHANGE WHEN NECESSARY, specify number of coordinates per condition
                
                
            
       #              self.extra_functions.travel_to_well((conditions.all_conditions[a][x])) #go to well
       #              print('Media Removal', self.extra_functions.get_current_time())

       #              self.fresco_xyz.delta_pump(conditions.removal_pump[a], 
       #                                     conditions.removal_steps[a])

       #              self.hold_position(1)

       #              current_condition = a % 2 #alternate between RA and media 
       #              if current_condition == 0:
       #                  print('Media Addition', self.extra_functions.get_current_time())
       #                  self.hold_position(1)
       #                  self.fresco_xyz.delta_pump(conditions.media_pump[a], 
       #                                             conditions.pump_steps[a])
                    
       #                  print('Empty tubing'), self.extra_functions.get_current_time()
       #                  self.fresco_xyz.manifold_delta(-self.lift)
       #                  self.hold_position(1)
       #                  self.fresco_xyz.delta_pump(conditions.media_pump[a],
       #                                             conditions.empty_steps[a])
       #                  self.hold_position(1)
       #                  self.fresco_xyz.manifold_delta(self.lift)
       #                  self.hold_position(1)
       #              else:
       #                  print('RA Application', self.extra_functions.get_current_time())
       #                  self.hold_position(1)
       #                  self.fresco_xyz.delta_pump(conditions.application_pump[a], 
       #                                     conditions.pump_steps[a])
                    
       #                  print('Empty tubing'), self.extra_functions.get_current_time()
       #                  self.fresco_xyz.manifold_delta(-self.lift)
       #                  self.hold_position(1)
       #                  self.fresco_xyz.delta_pump(conditions.application_pump[a],
       #                                             conditions.empty_steps[a])
       #                  self.hold_position(1)
       #                  self.fresco_xyz.manifold_delta(self.lift)
                    
       #               ####new
                    

       #           # focus and image every 6 hours, saves with condition number and current time 
       #          # elapsed_time = self.extra_functions.get_current_time()
       #          # if elapsed_time % 6 == 0:
       #          #     self.z_camera.focus_on_current_object() 
       #          #     self.hold_position(1)
       #          #     image_after_application = self.z_camera.fresco_camera.get_current_image()
       #          #     self.hold_position(1)
       #          #     self.images_storage.save(image_after_application,
       #          #                              session_folder_path + '/' + 'PI_a_' +  str(a) + '' + str(current_time) + '_' + str(1) + '.png')
       #          # self.hold_position(1)
                    
       #              if conditions.deltaTime[a] > 0:
       #                  self.fresco_xyz.manifold_delta(-self.lift)
       #                  self.hold_position(1)
       #                  self.extra_functions.travel_to_lid()
       #                  self.hold_position(1)
       #                  self.extra_functions.lid_down() #lid down
                        
       #                  print('Plate at lid & holding', self.extra_functions.get_current_time())
       #                  #self.extra_functions.image()
       #                  self.protocol_state_manager.update_current_index(a)
       #                  self.hold_position((conditions.deltaTime[a]))
       #                  self.protocol_state_manager.update_current_index(a)
                        
       #                  self.extra_functions.lid_up() #lid up
       #                  self.hold_position(1)
       #                  self.extra_functions.move_to_well_12_1()
       #                  self.hold_position(1)
       #                  self.fresco_xyz.manifold_delta(self.lift)
       #              else:
       #                  self.hold_position((conditions.deltaTime[a]))
                