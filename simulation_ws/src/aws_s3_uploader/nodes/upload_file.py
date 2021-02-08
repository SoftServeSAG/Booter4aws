#!/usr/bin/env python

import sys

import actionlib
import rospy

from file_uploader_msgs.msg import UploadFilesAction, UploadFilesGoal

ACTION = "/s3_file_uploader/UploadFiles"
FILE_NAME = sys.argv[1]
NODE_NAME = "s3_file_uploader_client"
S3_KEY_PREFIX = "rosbags/test"

rospy.init_node(NODE_NAME)

goal = UploadFilesGoal(
            upload_location=S3_KEY_PREFIX,
            files=[FILE_NAME]
        )

client = actionlib.SimpleActionClient(ACTION, UploadFilesAction)
client.wait_for_server()

client.send_goal(goal)
client.wait_for_result()

print(client.get_result())