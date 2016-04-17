project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

add_executable (test_models_utils print_helper.hpp 
                                  main.cpp
                                  test_tuple.cpp
                                  test_queryset.cpp
                                  test_queryset_list.cpp
                                  test_queryset_filter.cpp
                                  test_queryset_project.cpp
                                  )
target_link_libraries (test_models_utils
                       #utils
                       ${Boost_FILESYSTEM_LIBRARY}
                       ${Boost_SYSTEM_LIBRARY}
                       ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
                       )

add_test(NAME TestUtils COMMAND $<TARGET_FILE:test_models_utils>)
