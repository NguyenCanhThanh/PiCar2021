cmake_minimum_required(VERSION 2.8.3)
project(picat_control)

find_package(catkin REQUIRED COMPONENTS
  roslint
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

roslint_python()
roslint_add_test()