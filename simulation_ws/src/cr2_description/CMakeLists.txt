cmake_minimum_required(VERSION 2.8.3)
project(cr2_description)

find_package(catkin REQUIRED COMPONENTS
    urdf
    xacro)

catkin_package(
    CATKIN_DEPENDS
        urdf
        xacro)

install(DIRECTORY launch urdf robot params meshes rviz
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
