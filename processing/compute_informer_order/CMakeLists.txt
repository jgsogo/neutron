project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

include(conanbuildinfo.cmake)
conan_basic_setup()

# Files in subdirectories
file(GLOB neutron_SRC
    "neutron/*.h"
    "neutron/*.cpp"
)
file(GLOB utils_SRC
    "neutron/utils/*.h"
    "neutron/utils/*.cpp"
)

add_executable(compute_informer_order main.cpp ${neutron_SRC} ${utils_SRC})
target_link_libraries(compute_informer_order ${CONAN_LIBS})
