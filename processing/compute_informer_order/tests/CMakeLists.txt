project(neutron)
cmake_minimum_required(VERSION 2.8.12)


find_package (Boost COMPONENTS system filesystem unit_test_framework REQUIRED)

include_directories (${TEST_SOURCE_DIR}/src
                     ${Boost_INCLUDE_DIRS}
                    )
#add_definitions (-DBOOST_TEST_DYN_LINK)


# Copy test data
SET(TEST_DATA_PATH ${CMAKE_BINARY_DIR}/bin/test_data)
file(MAKE_DIRECTORY ${TEST_DATA_PATH})
configure_file(config_tests.h.cmake ${CMAKE_CURRENT_LIST_DIR}/config_tests.h)
file(COPY data/informers.tsv DESTINATION ${TEST_DATA_PATH})
file(COPY data/regions.tsv DESTINATION ${TEST_DATA_PATH})

# All tests in one test project.
file(GLOB basic_tests "basic/test_*.cpp")
file(GLOB utils_tests "utils/test_*.cpp")

add_executable (test_neutron_basic main.cpp
                                   ${basic_tests}
                                   ${utils_tests})
target_link_libraries (test_neutron_basic
                       neutron
                       ${Boost_LIBRARIES}
                       )

add_test(NAME TestModels COMMAND $<TARGET_FILE:test_neutron_basic>)

