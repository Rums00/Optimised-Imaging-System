from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from services.protocols.base_protocol import BaseProtocol
from datetime import datetime
#from services.webcam_image import WebcamImage 

###add this line in def init of each new protocol 
####self.extra_functions = ExtraFunctions(fresco_xyz,z_camera,images_storage)
class ExtraFunctions(BaseProtocol):
    
    def __init__ (self, fresco_xyz: FrescoXYZ, z_camera: ZCamera, images_storage: ImagesStorage):
        super(ExtraFunctions, self).__init__(fresco_xyz=fresco_xyz, z_camera=z_camera, images_storage=images_storage)
        self.images_storage = images_storage
        
    # def image(self, target_coords):
    #     self.wcImage = WebcamImage(path='path/to/image', cam_port=0, name='Webcam', cam=0, ret=False, image=None)
    #     self.wcImage.take_image(target_coords)
    #     print('Image Taken', self.get_current_time())
        

    def travel_to_well(self, target_coords):
        self.down = 4500 #was7000
        self.lift = 3000
        #self.current_coords = [12, 1]
        print((target_coords))
        self.hold_position(1)
        self.fresco_xyz.manifold_delta(-self.lift)
        
        y_delta = target_coords[0] - self.current_coords[0]
        self.current_coords[0] += y_delta
        x_delta = target_coords[1] - self.current_coords[1]
        self.current_coords[1] += x_delta
        self.fresco_xyz.delta(y_delta*self.well_step_96, x_delta*self.well_step_96, 0)
        self.hold_position(1)
        
        self.fresco_xyz.manifold_delta(self.lift)
        
    def calibrate(self):
        self.down = 4500 #was6000
        self.lift = 3000
        
        print("Experiment #7 AD Start Date and Time is", self.get_current_time())
        self.fresco_xyz.go_to_zero_manifold()
        self.hold_position(0.5)
        self.fresco_xyz.go_to_zero()
        self.hold_position(0.5)
        self.move_to_well_12_1()
        print('at 12:1')
        self.hold_position(1)
        #self.lid_up()
        self.fresco_xyz.manifold_delta(self.down) #moves to pipetting height, 
                                                        #needs to move to a well after

    def move_to_well_12_1 (self):
        self.well12_1_coord_x = -14000 #-1150
        self.well12_1_coord_y = -62400 #-18000 
        self.fresco_xyz.go_to_zero()
        self.hold_position(1)
        self.fresco_xyz.set_position(self.well12_1_coord_x,self.well12_1_coord_y, 0) 
        self.current_coords = [12, 1]
    
    def get_current_time(self):
        return datetime.now()
    
    def travel_to_lid(self):
        self.fresco_xyz.go_to_zero()
        self.hold_position(1)
        self.fresco_xyz.delta(-16000,1000, 0)
        
    def lid_up(self):
         self.fresco_xyz.delta_pump(3, -6000)
         
    def lid_down(self):
         self.fresco_xyz.delta_pump(3, 6000)
         
    #def generate_coordinates(self,start_col, end_col, start_row, end_row, skip_cols = None,skip_rows = None):
    #    if not skip_cols and not skip_rows:
    #        return [[col, row] for col in range(start_col, end_col + 1) 
    #                for row in range(start_row, end_row + 1)]
    #    else:
    #        return [[col, row] for col in range(start_col, end_col + 1) 
    #                if (not skip_cols or col not in skip_cols) 
    #                for row in range(start_row, end_row + 1) 
    #                if (not skip_rows or row not in skip_rows)]
    
    def generate_coordinates(self, start_col, end_col, start_row, end_row, skip_coordinates=None):
        if not skip_coordinates:
            skip_coordinates = []

        return [[col, row] for col in range(start_col, end_col + 1)
                for row in range(start_row, end_row + 1)
                if [col, row] not in skip_coordinates]

    def trituration(self, pump):
        for i in range(self.precision_factor):
            if pump==4:
                self.fresco_xyz.delta(0,0,0-self.cover_volume[pump])
                self.fresco_xyz.delta(0,0,self.cover_volume[pump])
            else:
                self.fresco_xyz.delta_pump(pump, 0-self.cover_volume[pump])
                self.fresco_xyz.delta_pump(pump, self.cover_volume[pump])

    def pumping(self, direction_sign, level, pump_used):
        for i in range(level):
            if pump_used==4:
                self.fresco_xyz.delta(0,0,direction_sign*self.cover_volume[pump_used])
            else:
                self.fresco_xyz.delta_pump(pump_used, direction_sign*self.cover_volume[pump_used])
        
    # def addition(self, pump, cover_level=1*self.precision_factor, coordinate_list=self.coordinate_list_all):
    #     if pump in self.control_dict.keys():
    #         addition(self, pump=self.control_fluid, cover_level=cover_level, coordinate_list=self.control_dict[fluid])
    #         coordinate_list = list(set(coordinate_list) - set(self.control_dict[fluid]))
    #         sign = 1
    #         self.fresco_xyz.manifold_delta(self.pumping_height)
    
    #     for well_coords in coordinate_list:
    #         travel_to_well(self, target_coords=well_coords)
    #         pumping(self, direction_sign=sign, level=cover_level, pump_used=pump)
    #         self.fresco_xyz.go_to_zero_manifold()
                
                
    # def removal(self, pump=self.waste, triturate=False, removal_level=3*self.precision_factor, coordinate_list=self.coordinate_list_all):
    #     self.fresco_xyz.manifold_delta(self.pumping_height)
    #     sign= 0-1
    
    #     for well_coords in coordinate_list:
    #         travel_to_well(self, target_coords=well_coords)
    #     if triturate:
    #         trituration(self, pump=pump)
    #         pumping(self, direction_sign=sign, level=removal_level, pump_used=pump)
    #         self.fresco_xyz.go_to_zero_manifold()


    # def wash(self, cycles, washing_fluid, coordinate_list=self.coordinate_list_all):
    #     for i in range(cycles):
    #         addition(self, pump=washing_fluid, cover_level=3*self.precision_factor, coordinate_list=coordinate_list)
    #         self.hold_position(10)
    #         removal(self, coordinate_list=coordinate_list)


    # def treatment(self, fluid, pause_length, coordinate_list=self.coordinate_list_all):
    #     addition(self, fluid=fluid, coordinate_list=coordinate_list)
    #     self.hold_position(pause_length)
    #     removal(self, coordinate_list=coordinate_list)
