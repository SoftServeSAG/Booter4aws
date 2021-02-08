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
This node subscribes to rostopics sent over rosbridge from clients.
It then sets up the corresponding static gazebo model that has the move plugin attached
and also publishes the rostopic that the plugin subscribes to move it.

The topic that it subscribes to is call /client_robot_data for robots running with
rosbridge clients. It connects to /remapped_client_robot_data in case of server.

It has the capability to recognize stale data and remove the objects.
"""

import rospy
import json
import rospkg
import roslib.message

from std_msgs.msg import String
from geometry_msgs.msg import Pose
from subprocess32 import check_output

from rospy_message_converter import message_converter, json_message_converter


class ServerRosBridge:
    def __init__(self):
        
        self._pubs = {}
        
        self.robot_name = rospy.get_param('ROBOT_NAME')
        self.rosbridge_state = rospy.get_param('ROSBRIDGE_STATE')

        self.robot_data_sub = rospy.Subscriber('client_data', String, self.data_callback, queue_size=1)

    def data_callback(self, msg):
        """ This is the callback that gets called by data from all robots. We just update a datastructure
            with the latest data, and create an entry if it doesn't exist."""
        data = json.loads(msg.data)

        # Ignore data from current robot since it's already available
        if data['name'] == self.robot_name:
            pass
        else:
            topic = '/' + data['name'] + data["topic"]
            self.process_msg(topic, data['message_type'], data["payload"].decode('utf_8'))
            
    def process_msg(self, topic, message_type, payload):
        
        # create publisher if we don't have one
        if topic not in self._pubs:
            self._pubs[topic] = rospy.Publisher(topic, roslib.message.get_message_class(message_type), queue_size=1)
        rospy.logdebug("Msg payload: %s", payload)    
        
        # convert json to ROS message
        message = json_message_converter.convert_json_to_ros_message(message_type, payload)
        
        # publish message
        self._pubs[topic].publish(message)

    def main(self):
        rate = rospy.Rate(10.0)

        while not rospy.is_shutdown():
            rate.sleep()


if __name__ == '__main__':
    rospy.init_node('server_rosbridge')
    master = ServerRosBridge()
    master.main()
