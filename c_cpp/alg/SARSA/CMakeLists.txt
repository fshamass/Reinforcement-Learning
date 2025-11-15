cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0076 NEW)
project(SARSA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)

# Create lib directory if it doesn't exist
file(MAKE_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

# Find the cliff-walking environment library
find_library(GORGE_WALKING_LIB 
    NAMES gorge_walking_env
    PATHS ${CMAKE_CURRENT_SOURCE_DIR}/../../env/gorge-walking/lib
    REQUIRED
)

# Build Q-Learning shared library
add_library(sarsa SHARED
    sarsa.cpp
)

target_include_directories(sarsa 
    PUBLIC 
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/../../env/gorge-walking
)

# Build the cliff walking executable
add_executable(gorge_walking
    gorge_walking.cpp
)

# Link the executable against the SARSA library and the gorge-walking environment library
target_link_libraries(gorge_walking
    PRIVATE
        sarsa
        ${GORGE_WALKING_LIB}
)

# Make sure the cliff walking library can be found at runtime
if(APPLE)
    set_target_properties(gorge_walking PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "@loader_path/lib;@loader_path/../../env/gorge-walking/lib"
    )
else()
    set_target_properties(gorge_walking PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "$ORIGIN/lib:$ORIGIN/../../env/gorge-walking/lib"
    )
endif()