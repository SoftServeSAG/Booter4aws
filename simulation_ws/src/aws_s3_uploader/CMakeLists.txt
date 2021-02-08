cmake_minimum_required(VERSION 2.8.3)
project(aws_s3_uploader)

find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()
catkin_python_setup()

catkin_install_python(PROGRAMS 
  nodes/upload_manager.py
  nodes/upload_file.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
install(DIRECTORY launch config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})