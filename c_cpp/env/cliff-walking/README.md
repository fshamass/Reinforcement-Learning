# Cliff Walking (C++)

This folder contains a small C++ implementation of the Cliff Walking environment (classic RL example). The code is intended as a compact environment/agent example for experimentation and learning.

## Contents

- `cliff_walking.cpp` — implementation source file(s) for the environment and logic
- `cliff_walking.hpp` — header(s) declaring the environment, actions, and API
- `main.cpp` — example runner that uses the environment (entry point)
- `CMakeLists.txt` — CMake build configuration file

## Requirements

- A C++17-compatible compiler (g++, clang++)
- CMake 3.10 or higher (recommended build method)
- No external libraries are required; the project uses the C++ standard library

## Build

### Using CMake (Recommended)

1. Create and enter a build directory:
```bash
mkdir build
cd build
```

2. Configure the project:
```bash
cmake ..
```

3. Build the library and demo:
```bash
make
```

This will create:
- A shared library (`libcliff_walking_env.dylib` on macOS, `.so` on Linux) in the `../lib/` directory
- An executable named `cliff_walking_demo` in the current directory

The resulting directory structure will be:
```
cliff-walking/
├── lib/                          # Created automatically
│   └── libcliff_walking_env.dylib  # Shared library
├── cliff_walking_demo            # Executable
├── cliff_walking.cpp
├── cliff_walking.hpp
├── main.cpp
├── CMakeLists.txt
└── build/                        # Build artifacts
    └── ...
```

### Manual Compilation (Alternative)

If you prefer not to use CMake, you can compile directly:

```bash
g++ -std=c++17 -O2 main.cpp cliff-walking.cpp -o cliff_walking
```

## Run

After building with CMake, from the cliff-walking directory:
```bash
./cliff_walking_demo
```

If you built manually:
```bash
./cliff_walking
```

Note: When running the CMake-built executable, make sure you're in the main cliff-walking directory, not the build directory, as the executable is placed in the source directory.

## Expected Behavior

- The runner (`main.cpp`) demonstrates environment steps, possible random or deterministic agent moves, and prints state transitions and rewards
- Exact output depends on the implementation in `main.cpp`

## Project Structure

The project is built as a shared library with a demo executable:
- `cliff_walking_env` - shared library containing the environment implementation
- `cliff_walking_demo` - executable that demonstrates using the environment

## Troubleshooting

Common issues and solutions:

1. CMake build fails:
   - Ensure you're running `cmake ..` from inside the `build` directory
   - Check that all source files exist and are named correctly
   - Remove the `build` directory and try again if you get unusual errors

2. Compiler errors:
   - Ensure you have a C++17 compatible compiler
   - Check that all required headers are included
   - Verify that namespace qualifiers are correct (e.g., `std::`)

## Contributing

If you add features, please:

- Add or update this README with any new build or runtime requirements
- Keep changes focused (new agent implementations or experiments should go into their own subfolder)
- Update the CMakeLists.txt if you add new source files
