#!/usr/bin/env python
#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

"""
This nodes job is to collect position info and sends it over /client_robot_data via rosbridge.
To grab data of all other robots as a client, subscribe to /client_robot_data and remap
it to /remapped_client_robot_data. If you are a server, you have all the data in
/client_robot_data already
"""

import rospy
import roslibpy
import roslib.message
import json
from std_msgs.msg import String

from rospy_message_converter import message_converter, json_message_converter

class SendData:
    def __init__(self):

        self.topic = rospy.get_param('~topic')
        self.message_type = rospy.get_param('~message_type')
        
        self.data_to_rosbridge = {}
        self.data_to_rosbridge['name'] = rospy.get_param('ROBOT_NAME')
        self.data_to_rosbridge['payload'] = {}
        self.data_to_rosbridge['topic'] = self.topic 
        self.data_to_rosbridge['message_type'] = self.message_type 
        
        self.rosbridge_ip = rospy.get_param('ROSBRIDGE_IP')
        self.rosbridge_state = rospy.get_param('ROSBRIDGE_STATE')
        
        self.client = roslibpy.Ros(host=self.rosbridge_ip, port=9090)
        self.client.run()

        # if self.rosbridge_state == 'CLIENT':
        #     self.remap_pub = rospy.Publisher('remapped_client_robot_data', String, queue_size=1)
        #     self.robot_data_listener = roslibpy.Topic(self.client, 'client_robot_data', 'std_msgs/String')
        #     self.robot_data_listener.subscribe(self.remap_subscriber)

        self.sub = rospy.Subscriber(self.topic, roslib.message.get_message_class(self.message_type), self.data_callback)
        self.init_rosbridge_talkers()


    def init_rosbridge_talkers(self):
        self.laser_scan_talker = roslibpy.Topic(self.client, 'client_data', 'std_msgs/String')
        
    def data_callback(self, msg):
        rospy.logdebug("Data received: %s", msg)
        
        # convert message to json string
        self.data_to_rosbridge['payload'] = json_message_converter.convert_ros_message_to_json(msg)
        
        # publish message over rosbridge
        self.laser_scan_talker.publish(roslibpy.Message( {'data': json.dumps(self.data_to_rosbridge)} ))

    def main(self):
        rate = rospy.Rate(10.0)

        while not rospy.is_shutdown():
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('laser_scan_rosbridge')
    send_data = SendData()
    send_data.main()


