# Cliff Walking (C++)

This folder contains a small C++ implementation of the Cliff Walking environment (classic RL example). The code is intended as a compact environment/agent example for experimentation and learning.

## Contents

- `cliff-walking.cpp` — implementation source file(s) for the environment and logic.
- `cliff-walking.hpp` — header(s) declaring the environment, actions, and API.
- `main.cpp` — example runner that uses the environment (entry point).
- `main` — may be an existing compiled binary (if present). Remove or ignore if you prefer to build from source.

## Requirements

- A C++17-compatible compiler (g++, clang++).
- No external libraries are required; the project uses the C++ standard library.

## Build

Open a terminal and change to this directory. If your path contains special characters (for example `C:C++`), wrap the path in quotes:

```bash
cd "C:C++/env/cliff-walking"
```

Compile with a standard command (example using g++ / clang++):

```bash
g++ -std=c++17 -O2 main.cpp cliff-walking.cpp -o cliff_walking
```

If your project splits implementation across more files, add them to the compile line or use a Makefile.

## Run

After building, run the binary:

```bash
./cliff_walking
```

If there's an existing `main` binary in the folder (committed by mistake), you can run it directly, but rebuilding from source is recommended.

## Expected behavior

- The runner (`main.cpp`) typically demonstrates environment steps, possible random or deterministic agent moves, and prints state transitions and rewards.
- Exact output depends on the implementation in `main.cpp` (look at the file to see what is printed).

## Contributing

If you add features, please:

- Add or update this README with any new build or runtime requirements.
- Keep changes focused (new agent implementations or experiments should go into their own subfolder).
