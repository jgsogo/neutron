project(neutron)
cmake_minimum_required(VERSION 2.8.12)

add_executable (test_neutron_basic main.cpp
                                   test_informer.cpp
                                   test_region.cpp)
target_link_libraries (test_neutron_basic
                       neutron
                       ${Boost_LIBRARIES}
                       )

add_test(NAME TestModels COMMAND $<TARGET_FILE:test_neutron_basic>)
