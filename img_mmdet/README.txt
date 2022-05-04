########################################################################
#          IPS300+: a Challenging Multimodal Dataset for Intersection Perception System         #
#                                      Huanan Wang    Xinyu Zhang    Jun Li                                           #
#                                   Tsinghua University    Daimler AG Co. Ltd                                         #
#                                  http://www.openmpd.com/column/IPS300                                        #
#                                   published under CC BY-NC-SA 4.0 license                                         #
########################################################################


Label files Discription:
============================================================

The label files contain two formats, the information in these formats are the same and you can 
use any of them.

txt format:

All values (numerical or strings) are separated via spaces, each row corresponds to one object. 
The 19 columns represent:

Value       Name            Type              Description
-------------------------------------------------------------------------------------------------------
   1            type             string             Describes the type of object:, ‘Pedestrian’, ‘Cyclist’, 
                                                       ‘Tricycle’, ‘Minibus’, ‘Largeandmediumsizedpassengercars’,
                                                       ‘Truck’, ‘Engineeringcar’
   1         occluded         float               Indicating occlusion state:
                                                           0.0 = fully visible, 1.0 = partly occluded
                                                           2.0 = largely occluded, 3.0 = unknown # the state number 
                                                           formally as float but only have four values.
   1         reserved         integer            Set to 0
   1          alpha*1           float             Observation angle of object, ranging [-pi..pi]
   4         bbox1*2           float             2D bounding box of object in the image from cam1 
                                                          (0-based index): contains left, top, right, bottom pixel 
                                                          coordinates. 
   4         bbox2*2           float             2D bounding box of object in the image from cam2 
                                                          (0-based index): contains left, top, right, bottom pixel 
                                                          coordinates*2. 
   3       dimensions        float              3D object dimensions: height, width, length (in meters).
   3         location          integer           3D object location x,y,z in lidar coordinates (in meters).
   1      rotation_y*3        float               Rotation ry around Y-axis in camera coordinates [-pi..pi].

*1: Alpha represents the angle between the object direction and the x axis of the lidar in the 
lidar coordinate system, with the lidar origin as the center and the line from the lidar origin 
to the object center as the radius, rotating the object around the lidar y axis to the lidar z axis. 
(Similar with KITTI but take lidar coordinate as the main coordinate).

*2: Since the labeling work was done in lidar coordinate, the bounding box out of the image 
FOV(1920×1080) needs to be cut.

*3: The difference between rotation_y and alpha are, that rotation_y is directly given in camera 
coordinates, while alpha also considers the vector from the camera center to the object center, 
to compute the relative orientation of the object with respect to the camera. For example, a car 
which is facing along the X-axis of the camera coordinate system corresponds to rotation_y=0, 
no matter where it is located in the X/Z plane (bird's eye view), while alpha is zero only, when 
this object is located along the Z-axis of the camera. When moving the car away from the Z-axis,
the observation angle will change.

json format:

The lebel information has been explicitly written in json label files. For the introduction of 
corresponding label, please refer to txt format description.