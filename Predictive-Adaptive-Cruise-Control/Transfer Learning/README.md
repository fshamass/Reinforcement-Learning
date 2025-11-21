# Transfer Learning: Simulation to Real-World Deployment

This directory documents the transfer learning pipeline for deploying the Predictive Adaptive Cruise Control (PACC) system from Webots simulation to physical hardware. The goal is to transfer the trained SAC policy to real RC vehicles while maintaining the learned behaviors.

## 🎯 Project Goal

Transfer the trained RL policy from Webots simulation to physical hardware, enabling real-world adaptive cruise control with:
- Real-time sensor processing (camera + radar)
- Robust object detection and tracking
- Smooth control adaptation to physical vehicle dynamics
- Safe operation in real-world conditions

## 📋 Development Phases

### Phase 1: Hardware Selection ✅

**Objective**: Select appropriate hardware platforms for lead and ego vehicles.

#### Lead Vehicle
**Selected**: [KEYESTUDIO Smart Car Kit](https://www.amazon.com/KEYESTUDIO-Bluetooth-Controller-Ultrasonic-Programming/dp/B08276N3D9)
- **Specs**:
  - Differential drive robot platform
  - Programmable speed control (Arduino-based)
  - Bluetooth/WiFi control capability
  - Max speed: ~2 m/s (7.2 km/h)
- **Rationale**:
  - Cost-effective solution for hardware validation
  - Programmable for constant speed testing (calibration)
  - AprilTag detection is faster (2-5ms) and more reliable than YOLO
  - Easy to add speed controller for fixed-velocity testing
  - Can be upgraded with GPS module for closed-loop speed control if needed

#### Ego Vehicle
**Selected**: [Hiwonder JetAcker (Advanced Variant)](https://www.hiwonder.com/products/jetacker?variant=41203656327255)
- **Compute**: NVIDIA Jetson Orin 8GB
- **Sensors**:
  - Front-facing camera (object detection, lane tracking)
  - Lidar sensor (Substitute for Radar distance and velocity measurement)
  - IMU for vehicle dynamics
- **Rationale**:
  - Jetson Orin provides sufficient compute for:
    - Real-time object detection (YOLOv8/v11)
    - RL policy inference
    - Sensor fusion
  - Pre-integrated ROS2 support
  - Built-in motor controllers
  - Expandable for additional sensors

**Status**: ✅ Hardware selected, pending procurement

---

### Phase 2: Simulation Migration to ROS2 🔄

**Objective**: Port the existing Webots simulation to ROS2 architecture to match the hardware platform.

#### 2.1 ROS2 Learning & Familiarization
**Prerequisites**:
- Install ROS2 Humble (Ubuntu 22.04 on UTM VM)
- Complete ROS2 tutorials:
  - Nodes, topics, services, actions
  - rclpy/rclcpp basics
  - Launch files and parameter management
  - Intermediate (and possibly advanced if needed) level learning

**Resources**:
- [ROS2 Official Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS2 Navigation Stack](https://navigation.ros.org/)
- [Webots ROS2 Interface](https://github.com/cyberbotics/webots_ros2)

**Estimated Duration**: 3-4 weeks

#### 2.2 Webots-ROS2 Integration
**Expected Tasks**:
1. Install Webots ROS2 package: `ros-humble-webots-ros2`
2. Convert Webots supervisor controller to ROS2 node
3. Implement ROS2 topics for:
   - `/ego/camera/image_raw` (sensor_msgs/Image)
   - `/ego/lidar/scan` (sensor_msgs/LaserScan or custom lidar message)
   - `/ego/cmd_vel` (geometry_msgs/Twist)
   - `/ego/odom` (nav_msgs/Odometry)
   - `/lead/odom` (nav_msgs/Odometry)
4. Replace gRPC communication with ROS2 pub/sub
5. Implement ROS2 launch files for simulation startup

**Expected Deliverables**:
- ROS2-compatible Webots simulation
- ROS2 launch files
- Topic/message documentation

**Estimated Duration**: 3-4 weeks

#### 2.3 RL Training Pipeline Integration
**Expected Tasks**:
1. Create ROS2-compatible Gym environment wrapper
2. Integrate Stable-Baselines3 with ROS2:
   - Use `ros2 topic` interface in environment
   - Synchronize step timing with ROS2 clock
3. Validate training performance matches original implementation
4. Test policy inference through ROS2 action server

**Validation Criteria**:
- Training convergence similar to original gRPC implementation
- Real-time inference latency < 50ms
- Smooth policy execution in simulation

**Estimated Duration**: 2-3 weeks

**Status**: 🔄 Not started

---

### Phase 3: Algorithm Deployment to Hardware 🔜

**Objective**: Deploy the trained RL policy to the JetAcker platform and establish the complete perception-control pipeline.

#### 3.1 Hardware Setup & ROS2 Configuration
**Expected Tasks**:
1. Configure network communication (WiFi/Ethernet)
2. Calibrate sensors:
   - Camera intrinsics/extrinsics
   - Lidar mounting position and FOV
   - IMU calibration
3. Test individual ROS2 drivers:
   - Camera node
   - Lidar node
   - Motor controller node

**Safety Considerations**:
- Implement emergency stop mechanism
- Set conservative speed limits initially
- Test in controlled environment

#### 3.2 Perception Pipeline Implementation
**Expected Tasks**:
1. Validate object detection model (YOLOv8/v11):
   - Detect and track lead vehicle
   - Export to ONNX/TensorRT for Jetson optimization
2. Implement sensor fusion node:
   - Fuse camera detections with lidar measurements
   - Publish lead vehicle state (distance, relative velocity, lateral offset)


**Performance Targets (Critical Real-Time Constraint)**:

The simulation currently runs in synchronous/stepped mode with 20ms timesteps - the supervisor pauses Webots until perception and policy inference complete. However, on real hardware there is no "pause button" - the control loop must complete within 20ms to maintain real-time operation.

**Estimated Latency Budget Breakdown**:
- Camera frame capture: ~2-3ms
- Object detection (YOLOv8-nano/tiny + TensorRT): ~8-12ms ⚠️ **Primary bottleneck**
- Lidar scan reading: ~1ms
- Sensor fusion (distance, relative velocity, lateral offset): ~2-3ms
- RL policy inference: ~2-4ms
- Motor control commands: ~1ms
- **Total: ~16-24ms** (tight fit, will most likely require optimization)

**Mitigation Strategies**:
1. **Simulation Latency Training** (Phase 2.3):
   - Add 1-2 timestep observation delays (20-40ms) during ROS2 simulation retraining
   - Train policy to be robust to perception-action latency
   - This will close the sim-to-real gap for timing

2. **Model Optimization** (Phase 3.2):
   - Use YOLOv8-nano with TensorRT FP16 quantization on Jetson
   - Target: 8-10ms inference time for object detection

3. **Reduced Detection Rate** (if needed):
   - Run object detection at 25-30 Hz (every 30-40ms)
   - Use temporal filtering/Kalman filter to interpolate between detections
   - Policy receives smoothed state estimates

4. **Async Processing Pipeline**:
   - Overlap perception and control using previous frame's detection
   - Reduces effective latency at cost of slight staleness

5. **Fallback Option**:
   - Accept 30-40ms control loop rate and retrain with longer timestep
   - Reduces real-time pressure but requires additional training

**Success Criteria**:
- ✅ Maintain 20ms (50Hz) control loop rate on Jetson Orin 8GB
- ✅ Policy successfully performs ACC + vehicle following with real-world latency
- ✅ Smooth steering control (no excessive jitter from pipeline delays)
- ✅ Safe following distance maintained (3-4m target gap)

#### 3.3 Control Pipeline Deployment
**Tasks**:
1. Load trained SAC policy on Jetson
2. Create ROS2 action server for RL policy inference
3. Implement low-level motor controllers:
   - Steering servo control
   - Throttle/brake control
4. Add safety layers:
   - Minimum safe distance override
   - Maximum speed limiter
   - Collision imminent emergency brake
5. Implement control smoothing (low-pass filter if RL does not learn smooth steering)

**Testing Protocol**:
1. Static tests (vehicle stationary)
2. Solo driving (no lead vehicle)
3. Fixed-speed following
4. Variable-speed following
5. Curve following
6. Emergency stop scenarios

**Status**: 🔜 Not started

---

### Phase 4: Model Fine-Tuning & Sim-to-Real Adaptation 🔜

**Objective**: Bridge the sim-to-real gap through domain adaptation and fine-tuning.

#### 4.1 Sim-to-Real Gap Analysis
**Identify Discrepancies**:
- Vehicle dynamics differences (friction, steering response, acceleration)
- Sensor noise and reliability
- Latency in perception-control loop
- Environmental variations (lighting, surface conditions)

**Measurement Approach**:
- Collect real-world driving data
- Compare sensor readings to simulation
- Analyze policy performance metrics
- Identify failure modes

#### 4.2 Domain Randomization (Pre-deployment)
**Simulation Enhancements**:
- Randomize vehicle dynamics parameters (mass, friction, drag)
- Add sensor noise models (camera blur, radar dropouts)
- Vary lighting conditions in simulation
- Introduce latency in control loop

**Goal**: Train more robust policy before hardware deployment

#### 4.3 Real-World Fine-Tuning
**Approach Options**:

**Option A: Online Fine-Tuning**
- Continue training on real hardware with safety constraints
- Use human demonstrations for safe exploration
- Implement safe RL techniques (CPO, PPO-Lagrangian)

**Option B: Offline Fine-Tuning**
- Collect real-world trajectory data
- Train residual policy using offline RL (CQL, IQL)
- Combine base policy with residual corrections

**Option C: Imitation Learning Bridge**
- Collect expert demonstrations on hardware
- Use behavioral cloning to adapt policy
- Fine-tune with RL in safe scenarios

**Validation Metrics**:
- Success rate: % of episodes with safe following
- Following accuracy: Mean distance error from target
- Smoothness: Jerk in steering and throttle
- Safety: Number of interventions needed

#### 4.4 Iterative Improvement
**Process**:
1. Collect failure cases from real-world testing
2. Reproduce failures in simulation
3. Augment training with failure scenarios
4. Retrain and validate in simulation
5. Deploy updated policy to hardware
6. Repeat until performance targets met

**Performance Targets**:
- Maintain 4m ± 0.5m following distance
- Smooth steering (max jerk < 2 rad/s³)
- Safe operation in 95% of test scenarios
- Handle lead vehicle speeds: 0-25 km/h

**Status**: 🔜 Not started

---

## 🛠️ Technical Stack

### Software
- **Simulation**: Webots 2025a
- **Middleware**: ROS2 Humble
- **ML Framework**: Stable-Baselines3, PyTorch
- **Computer Vision**: OpenCV, YOLOv8/v11
- **Inference Optimization**: ONNX Runtime, TensorRT
- **Development**: Python 3.10+, C++ (for performance-critical nodes)

### Hardware
- **Compute**: NVIDIA Jetson Orin 8GB
- **Sensors**: Camera, Lidar, IMU
- **Platforms**: JetAcker (ego), RC Drift Car (lead)

---

## 📊 Success Metrics

### Simulation Metrics (Phase 2)
- ✅ Training convergence equivalent to original implementation
- ✅ Real-time inference latency < 20ms in ROS2 setup
- ✅ Smooth policy execution without communication delays

### Hardware Metrics (Phase 3-4)
- 🎯 End-to-end latency: perception → policy → control < 20ms
- 🎯 Following distance accuracy: ±0.5m from 4m target
- 🎯 Lateral tracking error: < 0.3m in curves
- 🎯 Safe operation: 0 collisions in 100+ test runs
- 🎯 Velocity matching: within 2 km/h of lead vehicle

---

## 🚧 Known Challenges & Mitigation Strategies

### Challenge 1: Sim-to-Real Gap
**Impact**: Policy may not transfer directly due to dynamics mismatch
**Mitigation**:
- Domain randomization in simulation
- System identification of real vehicle
- Residual policy learning
- Progressive deployment (stationary → slow → full speed)

### Challenge 2: Real-Time Performance on Jetson
**Impact**: Inference + perception may exceed timing requirements
**Mitigation**:
- Model optimization (TensorRT quantization)
- Parallel processing of perception and control
- Frame skipping if necessary
- C++ implementation of critical nodes

### Challenge 3: Sensor Reliability
**Impact**: Noisy/missing sensor data in real world
**Mitigation**:
- Robust sensor fusion
- Timeout handling and failsafes
- Degraded mode operation (e.g., radar-only mode)
- Extensive field testing

### Challenge 4: Safety in Real-World Testing
**Impact**: Potential for collisions during learning/testing
**Mitigation**:
- Start with very conservative policies
- Manual emergency stop always available
- Test in controlled environments first
- Gradual increase in difficulty

---

## 📝 Next Steps

1. **Immediate**: Begin ROS2 learning curriculum (Phase 2.1)
2. **Short-term**: Set up Webots-ROS2 integration environment (Phase 2.2)
3. **Medium-term**: Hardware procurement and initial setup (Phase 1 completion)
4. **Long-term**: Staged deployment and fine-tuning (Phases 3-4)

---

## 📚 References & Resources

### ROS2 Resources
- [ROS2 Documentation](https://docs.ros.org/)
- [Webots ROS2 Interface](https://github.com/cyberbotics/webots_ros2)
- [Nav2 Documentation](https://navigation.ros.org/)

### Transfer Learning & Sim-to-Real
- [Sim-to-Real Transfer for RL (OpenAI)](https://openai.com/research/learning-dexterity)
- [Domain Randomization Techniques](https://arxiv.org/abs/1703.06907)
- [Safe RL for Robotics](https://arxiv.org/abs/2112.07701)

### Jetson Optimization
- [TensorRT Documentation](https://developer.nvidia.com/tensorrt)
- [Jetson AI Courses](https://developer.nvidia.com/embedded/learn/jetson-ai-certification-programs)

---

## 🔗 Related Documentation

- [Main Project README](../README.md)
- [Simulation Architecture](../README.md#system-architecture)
- [Training Results](../README.md#-results-and-analysis)

---

*Last Updated: 2025-01-20*
