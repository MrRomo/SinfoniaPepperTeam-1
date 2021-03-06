#!/usr/bin/env python
# license removed for brevity
"""
//======================================================================//
//  This software is free: you can redistribute it and/or modify        //
//  it under the terms of the GNU General Public License Version 3,     //
//  as published by the Free Software Foundation.                       //
//  This software is distributed in the hope that it will be useful,    //
//  but WITHOUT ANY WARRANTY; without even the implied warranty of      //
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..  See the      //
//  GNU General Public License for more details.                        //
//  You should have received a copy of the GNU General Public License   //
//  Version 3 in the file COPYING that came with this distribution.     //
//  If not, see <http://www.gnu.org/licenses/>                          //
//======================================================================//
//                                                                      //
//      Copyright (c) 2019 SinfonIA Pepper RoboCup Team                 //
//      Sinfonia - Colombia                                             //
//      https://sinfoniateam.github.io/sinfonia/index.html              //
//                                                                      //
//======================================================================//
"""
import rospy
import sys
from Class.characterization import Characterization
from Class.utils import Utils
from sinfonia_pepper_tools_interaction.srv import FaceDetector
from sinfonia_pepper_tools_interaction.srv import FaceMemorize
from sinfonia_pepper_tools_interaction.srv import FaceRecognize
from sinfonia_pepper_robot_toolkit.srv import TakePicture
from sensor_msgs.msg import Image


class FaceID():
    def __init__(self, camera, person):
        self.imagePub = rospy.Publisher('/faceImage', Image, queue_size=10)
        self.person = Characterization(person)
        self.source = camera
        self.utils = Utils(self.source, self.person.percent_of_face)

    def detectFace(self, req):
        frame = self.utils.take_picture_source()
        people = self.person.detect_person(frame)
        res = self.utils.add_features_to_image(frame, people)
        if req.cvWindow:
            self.imagePub.publish(res["frame"])
        return res["isInFront"]

    

if __name__ == '__main__':
    try:
        rospy.init_node('robot_face_node')
        if(len(sys.argv) > 2):
            face = FaceID(int(sys.argv[1]), str(sys.argv[2]))
        else:
            face = FaceID(3,'cloud')

        rospy.Service('robot_face_detector', FaceDetector, face.detectFace)
        print("robot face node started")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
