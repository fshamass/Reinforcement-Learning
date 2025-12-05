# Reinforcement Learning Research & Development

This repository showcases my work in reinforcement learning, ranging from a comprehensive autonomous vehicle control system to foundational experiments exploring RL algorithms and implementation techniques.

## Featured Project

### Predictive Adaptive Cruise Control (PACC)

A production-scale reinforcement learning system that implements intelligent vehicle following with traffic flow optimization. This project represents a complete end-to-end RL application, from simulation training to real-world hardware deployment.

**Project Highlights**:
- Multi-modal RL agent performing ACC, stop-and-go traffic handling, and smooth curve following
- Custom neural network architecture achieving jitter-free continuous control
- Webots simulation environment with gRPC communication pipeline
- Comprehensive sim-to-real transfer learning roadmap using ROS2
- Hardware deployment on NVIDIA Jetson Orin with real-time perception pipeline

**Status**: Active development - simulation training complete, currently migrating to ROS2 for hardware deployment

**[View Full Project Documentation](Predictive-Adaptive-Cruise-Control/README.md)**

Key technical achievements:
- Solved complex multi-objective optimization (safety, comfort, traffic efficiency)
- Developed custom SAC architecture eliminating steering jitter without post-processing
- Designed robust reward function balancing collision avoidance and following performance
- Built scalable simulation-to-reality pipeline for physical robot deployment

---

## Supporting Experiments & Research

Beyond the main PACC project, this repository contains foundational experiments and prototypes that explore specific RL concepts, algorithms, and implementation patterns. These are smaller, self-contained studies designed to:

- Isolate and understand specific RL algorithms and techniques
- Provide modular, reusable building blocks for larger projects
- Document learning progress and experimental findings
- Serve as educational reference implementations

### Structure

- **`c_cpp/`**: C++ implementations focusing on performance-critical components
- **`python/`**: Python experiments with various RL algorithms and frameworks
- Each experiment includes its own README with setup instructions and usage notes

### Philosophy

These experiments prioritize clarity and educational value over production optimization. They're designed to be:
- Easy to read, modify, and extend
- Self-contained with minimal dependencies
- Suitable as starting points for your own projects

---

## Repository Purpose

This repository serves multiple goals:

1. **Showcase**: Demonstrate end-to-end RL system development through the PACC project
2. **Document**: Track research progress, experiments, and lessons learned
3. **Share**: Provide reference implementations and reusable components
4. **Learn**: Maintain a structured approach to exploring new RL techniques

---

## Getting Started

### For the Main PACC Project
See the [comprehensive documentation](Predictive-Adaptive-Cruise-Control/README.md) including system architecture, training results, and deployment roadmap.

### For Individual Experiments
Navigate to the specific experiment folder (`c_cpp/` or `python/`) and follow the README instructions in each subdirectory.

---

## Technical Stack

**PACC Project**:
- Simulation: Webots 2025a
- Middleware: ROS2 Humble (migration in progress)
- ML Framework: Stable-Baselines3, PyTorch
- Deployment: NVIDIA Jetson Orin, custom RC platforms

**Experiments**:
- Languages: Python 3.10+, C++17
- Frameworks: Various (documented per experiment)

---

## Notes

- This is an active research repository under continuous development
- Code (if provided) is for educational and research purposes
- The PACC project is designed for eventual hardware deployment with comprehensive safety considerations
- Supporting experiments are snapshots of learning progress and may not represent production-quality code


