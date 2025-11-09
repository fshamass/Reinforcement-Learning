# Q-Learning Implementation

This directory contains the Q-Learning algorithm implementation and a cliff walking example using the environment from `../../env/cliff-walking`.

## Prerequisites

Before building this project:
1. First build the cliff-walking environment library:
```bash
cd ../../env/cliff-walking
mkdir build && cd build
cmake ..
make
```

## Build Instructions

1. Create and enter the build directory:
```bash
mkdir build
cd build
```

2. Configure CMake:
```bash
cmake ..
```

3. Build the library and executable:
```bash
make
```

This will create:
- `lib/libq_learn.dylib` (or `.so` on Linux) - The Q-Learning algorithm library
- `cliff_walking` - Executable demonstrating Q-Learning on the cliff walking environment

## Directory Structure After Build

```
Q_Learn/
├── lib/
│   └── libq_learn.dylib      # Q-Learning library
├── cliff_walking             # Main executable
├── Q_Learn.cpp
├── Q_Learn.hpp
├── cliff_walking.cpp
├── CMakeLists.txt
└── build/
    └── ...
```

## Running the Example

From the Q_Learn directory:
```bash
./cliff_walking

# Run with custom number of episodes
./cliff_walking 500

# Show usage information
./cliff_walking --help
```

### Command-line Arguments

- `[num_episodes]`: Optional. Number of training episodes (default: 100)
  - Must be a positive integer
  - Examples: `./cliff_walking 200`, `./cliff_walking 1000`

## Troubleshooting

If you get library loading errors:
1. Make sure you've built the cliff-walking environment first
2. Verify both libraries exist:
   - `../../env/cliff-walking/lib/libcliff_walking_env.dylib`
   - `./lib/libq_learn.dylib`
3. If needed, set `DYLD_LIBRARY_PATH` (macOS) or `LD_LIBRARY_PATH` (Linux):
```bash
# macOS
export DYLD_LIBRARY_PATH="$PWD/lib:$PWD/../../env/cliff-walking/lib:$DYLD_LIBRARY_PATH"

# Linux
export LD_LIBRARY_PATH="$PWD/lib:$PWD/../../env/cliff-walking/lib:$LD_LIBRARY_PATH"
```