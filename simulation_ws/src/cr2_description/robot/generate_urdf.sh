#!/bin/sh

# run this inside this directory or replace <filename>.xacro with $(find <package_name>...)

rosrun xacro xacro cr2.urdf.xacro --inorder > cr2_new.urdf