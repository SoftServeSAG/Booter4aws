cmake_minimum_required(VERSION 2.8.3)
project(cr2_gazebo)

find_package(catkin REQUIRED COMPONENTS)

catkin_package(
    CATKIN_DEPENDS
        gazebo_ros
        gazebo_ros_control
        cr2_description)

install(DIRECTORY launch meshes models worlds
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})