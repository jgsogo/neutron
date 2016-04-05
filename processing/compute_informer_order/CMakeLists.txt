project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED on)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")  # Needed for Travis CI
add_compile_options(-std=c++14) # CMake 2.8.12 or newer

include(conanbuildinfo.cmake)
conan_basic_setup()

# Files in subdirectories
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Testing
enable_testing()

add_subdirectory(utils)
add_subdirectory(neutron)


add_executable(compute_informer_order main.cpp)
target_link_libraries(compute_informer_order ${CONAN_LIBS} neutron)
