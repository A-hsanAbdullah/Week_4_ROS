# Mobile Robotics Lab 4 Deliverables Guide

This workspace contains the complete `my_launch_pkg` package designed to fulfill the tasks for Lab 4. The following guide details the steps you need to perform to generate the required deliverables.

## Step 1: Launch the System

Open a new terminal, navigate to the `Week4` directory, source your environment, and run the launch file:

```bash
cd ~/Desktop/Week4
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch my_launch_pkg turtlesim_launch.py
```

This will automatically launch:
1. `turtlesim_node` (Simulation window)
2. `follow_the_leader` (The node where turtle2 spawns and follows turtle1)
3. A new `gnome-terminal` window for `turtle_teleop_key` (Use this terminal's arrow keys to control turtle1).

> [!IMPORTANT]
> **Deliverable 1:** Take a screenshot of the terminals and the turtlesim window running simultaneously showing the launch process.

## Step 2: Record Data with Rosbag

Open a **new** terminal to record the topic data:

```bash
cd ~/Desktop/Week4
source /opt/ros/humble/setup.bash
source install/setup.bash

# Start recording the requested topics
ros2 bag record /turtle1/cmd_vel /turtle2/cmd_vel /turtle1/pose
```

Once it is recording, go to the teleop terminal and move turtle1 around for a few seconds. You should see turtle2 following turtle1.
Stop the recording in the rosbag terminal by pressing `Ctrl+C`.

> [!IMPORTANT]
> **Deliverable 1 (cont):** Take a screenshot of the `ros2 bag record` process.
> **Deliverable 4:** The `rosbag2_...` folder generated in your `Week4` directory contains the trajectory data. You will need to submit this and write a brief analysis about it.

## Step 3: Visualizing Data with rqt_plot

Open another **new** terminal to visualize the velocity data:

```bash
source /opt/ros/humble/setup.bash
rqt
```

1. In the `rqt` window, select **Plugins** → **Visualization** → **Plot**.
2. In the "Topic" field, type `/turtle1/cmd_vel` and press the `+` button.
3. Move `turtle1` using the teleop terminal and observe the live changes in linear and angular velocity in the plot.

> [!IMPORTANT]
> **Deliverable 6:** Take a screenshot of the `rqt_plot` graph showing `/turtle1/cmd_vel` data.

## Step 4: Gather Your Code Deliverables

All the required code modifications have been made. You need to submit the following files:

- **Deliverable 3 (Modified Launch File):** 
  `~/Desktop/Week4/src/my_launch_pkg/launch/turtlesim_launch.py`
  
- **Deliverable 5 (Follow the Leader Code):** 
  `~/Desktop/Week4/src/my_launch_pkg/my_launch_pkg/follow_the_leader.py`

## Step 5: Write Your Report

Write a short report (Deliverable 2) detailing:
- The approach you took to launch multiple nodes using Python launch files.
- How the follow-the-leader proportional controller works (calculating distance and angle error).
- Your observations regarding the recorded data and plotting.
