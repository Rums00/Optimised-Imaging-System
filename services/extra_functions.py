from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from services.protocols.base_protocol import BaseProtocol
from datetime import datetime

###add this line in def init of each new protocol 
####self.extra_functions = ExtraFunctions(fresco_xyz,z_camera,images_storage)

class ExtraFunctions(BaseProtocol):
    
    def __init__ (self, fresco_xyz: FrescoXYZ, z_camera: ZCamera, images_storage: ImagesStorage):
        super(ExtraFunctions, self).__init__(fresco_xyz=fresco_xyz, z_camera=z_camera, images_storage=images_storage)
        self.images_storage = images_storage
        self.well12_1_coord_x = -12200 #change to your specifications
        self.well12_1_coord_y = -60900 #change to your specifications
        self.down = 4500 #change to your specifications
        self.lift = 3000 #change to your specifications

    def travel_to_well(self, target_coords):


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


        print("Experiment #X AD Start Date and Time is", self.get_current_time())
        self.fresco_xyz.go_to_zero_manifold()
        self.hold_position(0.5)
        self.fresco_xyz.go_to_zero()
        self.hold_position(0.5)
        self.move_to_well_12_1()
        self.hold_position(1)
        #self.lid_up()
        self.fresco_xyz.manifold_delta(self.down) #moves to pipetting height, 
                                                        #needs to move to a well after

    def move_to_well_12_1 (self):
        
        self.fresco_xyz.go_to_zero()
        self.hold_position(1)
        self.fresco_xyz.set_position(self.well12_1_coord_x,self.well12_1_coord_y, 0) 
        self.current_coords = [12, 1]
    
    def get_current_time(self):
        return datetime.now()
    

    def generate_coordinates(self, start_col, end_col, start_row, end_row, skip_coordinates=None):
        if not skip_coordinates:
            skip_coordinates = []

        return [[col, row] for col in range(start_col, end_col + 1)
                for row in range(start_row, end_row + 1)
                if [col, row] not in skip_coordinates]