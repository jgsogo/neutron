project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

file(GLOB models_SRC
    "*.h"
    "*.cpp"
    "*.hpp"
)

# source_group (utils FILES ${models_SRC})
add_library(models ${models_SRC})
set_target_properties(models PROPERTIES LINKER_LANGUAGE CXX)

# Testing
add_subdirectory(utils)
add_subdirectory(test)
