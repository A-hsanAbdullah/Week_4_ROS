#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

class FollowTheLeader(Node):
    def __init__(self):
        super().__init__('follow_the_leader')
        
        self.turtle1_pose = None
        self.turtle2_pose = None
        
        # Subscribe to turtle1's pose
        self.pose_subscriber1 = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.turtle1_pose_callback,
            10
        )
        
        # Subscribe to turtle2's pose
        self.pose_subscriber2 = self.create_subscription(
            Pose,
            '/turtle2/pose',
            self.turtle2_pose_callback,
            10
        )
        
        # Publisher for turtle2's velocity
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/turtle2/cmd_vel',
            10
        )
        
        # Call spawn service for turtle2
        self.spawn_turtle()

        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)

    def spawn_turtle(self):
        client = self.create_client(Spawn, '/spawn')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn service not available, waiting again...')
        
        request = Spawn.Request()
        request.x = 2.0
        request.y = 2.0
        request.theta = 0.0
        request.name = 'turtle2'
        
        future = client.call_async(request)
        future.add_done_callback(self.spawn_callback)

    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Spawned turtle: {response.name}')
        except Exception as e:
            self.get_logger().error(f'Failed to spawn turtle: {e}')

    def turtle1_pose_callback(self, data):
        self.turtle1_pose = data

    def turtle2_pose_callback(self, data):
        self.turtle2_pose = data

    def control_loop(self):
        if self.turtle1_pose is None or self.turtle2_pose is None:
            return

        # Calculate distance between turtle1 and turtle2
        distance = math.sqrt(
            (self.turtle1_pose.x - self.turtle2_pose.x)**2 +
            (self.turtle1_pose.y - self.turtle2_pose.y)**2
        )

        vel_msg = Twist()
        
        # If turtle2 is not close to turtle1, move towards it
        if distance > 0.5:
            # Linear velocity proportional to distance
            vel_msg.linear.x = 1.5 * distance

            # Angle from turtle2 to turtle1
            angle_to_goal = math.atan2(
                self.turtle1_pose.y - self.turtle2_pose.y,
                self.turtle1_pose.x - self.turtle2_pose.x
            )
            
            # Difference between current angle and goal angle
            angle_diff = angle_to_goal - self.turtle2_pose.theta
            
            # Normalize angle between -pi and pi
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
                
            # Angular velocity proportional to angle difference
            vel_msg.angular.z = 4.0 * angle_diff
        else:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0

        self.velocity_publisher.publish(vel_msg)

def main(args=None):
    rclpy.init(args=args)
    node = FollowTheLeader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
