cmake_minimum_required(VERSION 2.8.3)
project(cr2_multifleet)

cmake_policy(SET CMP0054 NEW)

include_directories(${GAZEBO_INCLUDE_DIRS})
list(APPEND CMAKE_CXX_FLAGS "${GAZEBO_CXX_FLAGS}")

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
  gazebo_ros
  )

# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

add_library(move_object_plugin src/move_object.cc)
target_link_libraries(move_object_plugin ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

catkin_package(
  CATKIN_DEPENDS
    roscpp
    gazebo_ros
)

  
catkin_install_python(PROGRAMS
  scripts/client_rosbridge.py
  scripts/gazebo_model_mover.py
  scripts/data_client_rosbridge.py
  scripts/data_server_rosbridge.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY static_models_w_plugin 
DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(TARGETS move_object_plugin
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)