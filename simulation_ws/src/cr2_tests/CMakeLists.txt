cmake_minimum_required(VERSION 2.8.3)
project(cr2_tests)

find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()

install(
  DIRECTORY launch routes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

