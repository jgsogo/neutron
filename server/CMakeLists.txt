cmake_minimum_required(VERSION 3.0)
project(Neutron)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(neutron  CrossPlatformService.cpp
                        stdafx.cpp
                        stdafx.h
                        targetver.h)
target_link_libraries(neutron ${CONAN_LIBS})
