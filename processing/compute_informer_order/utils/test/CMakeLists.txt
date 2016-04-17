project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

find_package (Boost COMPONENTS system filesystem unit_test_framework REQUIRED)
include_directories (${TEST_SOURCE_DIR}/src
                     ${Boost_INCLUDE_DIRS}
                     )
add_definitions (-DBOOST_TEST_DYN_LINK)
add_executable (test_utils print_helper.hpp 
                           main.cpp
                           test_tuple.cpp
                           test_queryset.cpp
                           test_queryset_list.cpp
                           test_queryset_filter.cpp
                           test_queryset_project.cpp
                           )
target_link_libraries (test_utils
                       #utils
                       ${Boost_FILESYSTEM_LIBRARY}
                       ${Boost_SYSTEM_LIBRARY}
                       ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
                       )

#add_test(NAME TestUtils COMMAND $<TARGET_FILE:test_utils>)
