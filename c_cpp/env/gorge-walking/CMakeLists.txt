cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0076 NEW)
project(gorge_walking)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)

# Create lib directory if it doesn't exist
file(MAKE_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

# Build shared library from environment source
add_library(gorge_walking_env SHARED
    ${CMAKE_CURRENT_SOURCE_DIR}/gorge_walking.cpp
)

target_include_directories(gorge_walking_env PUBLIC .)

# Build demo executable from main.cpp
add_executable(gorge_walking_demo
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
)

target_link_libraries(gorge_walking_demo PRIVATE gorge_walking_env)