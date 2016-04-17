project(Neutron)
cmake_minimum_required(VERSION 2.8.12)


find_package (Boost COMPONENTS system filesystem unit_test_framework REQUIRED)
include_directories (${TEST_SOURCE_DIR}/src
                     ${Boost_INCLUDE_DIRS}
                     )
add_definitions (-DBOOST_TEST_DYN_LINK)

add_subdirectory(models)
add_subdirectory(utils)
