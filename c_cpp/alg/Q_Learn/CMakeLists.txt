cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0076 NEW)
project(q_learning)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)

# Create lib directory if it doesn't exist
file(MAKE_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

# Find the cliff-walking environment library
find_library(CLIFF_WALKING_LIB 
    NAMES cliff_walking_env
    PATHS ${CMAKE_CURRENT_SOURCE_DIR}/../../env/cliff-walking/lib
    REQUIRED
)

# Build Q-Learning shared library
add_library(q_learn SHARED
    Q_Learn.cpp
)

target_include_directories(q_learn 
    PUBLIC 
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/../../env/cliff-walking
)

# Build the cliff walking executable
add_executable(cliff_walking
    cliff_walking.cpp
)

# Link against both libraries
target_link_libraries(cliff_walking
    PRIVATE
        q_learn
        ${CLIFF_WALKING_LIB}
)

# Make sure the cliff walking library can be found at runtime
if(APPLE)
    set_target_properties(cliff_walking PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "@loader_path/lib;@loader_path/../../env/cliff-walking/lib"
    )
else()
    set_target_properties(cliff_walking PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "$ORIGIN/lib:$ORIGIN/../../env/cliff-walking/lib"
    )
endif()