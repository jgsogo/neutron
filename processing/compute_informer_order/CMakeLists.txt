project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED on)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")  # Needed for Travis CI
add_compile_options(-std=c++14) # CMake 2.8.12 or newer

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Files in subdirectories
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

OPTION(SPDLOG_DEBUG_ON "Enable debug logging" OFF) # Disabled by default
IF(SPDLOG_DEBUG_ON)
    ADD_DEFINITIONS(-DSPDLOG_DEBUG_ON)
ENDIF(SPDLOG_DEBUG_ON)

set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_package(Threads REQUIRED)
find_package(Boost COMPONENTS system filesystem REQUIRED)

# Testing
enable_testing()
if (UNIX)
    add_definitions(-Wfatal-errors)
    add_custom_target(check ${CMAKE_COMMAND} -E env CTEST_OUTPUT_ON_FAILURE=1
                      ${CMAKE_CTEST_COMMAND} --verbose
                      WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
else()
    add_custom_target(check ${CMAKE_COMMAND} -E env CTEST_OUTPUT_ON_FAILURE=1
                      ${CMAKE_CTEST_COMMAND} -C $<CONFIG> --verbose
                      WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
endif()


add_subdirectory(neutron)
add_subdirectory(tests)


add_executable(compute_informer_order main.cpp
                                      log_level_param.hpp)
target_include_directories(compute_informer_order PUBLIC ${CONAN_INCLUDE_DIRS_QUERYSET-CPP})
target_link_libraries(compute_informer_order 
                      ${CONAN_LIBS}
                      neutron
                      ${Boost_LIBRARIES}
                      Threads::Threads)
