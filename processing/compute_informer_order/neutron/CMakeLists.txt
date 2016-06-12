project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

file(GLOB neutron_SRC
    "*.h"
    "*.cpp"
    "*.hpp"
)

# source_group (neutron FILES ${neutron_SRC})
add_library(neutron ${neutron_SRC})
target_include_directories(neutron PUBLIC ${CONAN_INCLUDE_DIRS_QUERYSET-CPP})
set_target_properties(neutron PROPERTIES LINKER_LANGUAGE CXX)
