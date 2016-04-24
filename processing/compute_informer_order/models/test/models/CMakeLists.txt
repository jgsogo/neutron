project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

add_executable (test_models print_helper.hpp 
                            main.cpp
                            test_class_queryset_filter.cpp
                            test_class_queryset_groupby.cpp)
target_link_libraries (test_models
                       #utils
                       ${Boost_FILESYSTEM_LIBRARY}
                       ${Boost_SYSTEM_LIBRARY}
                       ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
                       )

add_test(NAME TestModels COMMAND $<TARGET_FILE:test_models>)
