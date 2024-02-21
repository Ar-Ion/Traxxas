import rospy
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_multiply
import numpy as np

class Node:
    def __init__(self):
        self.createPublisher()
        self.createSubscriber()

    def createPublisher(self):
        self.pub = rospy.Publisher('/sensors/IMU_ENU', Imu, queue_size=10)
        rospy.init_node('ned2enu', anonymous=True)

    def createSubscriber(self):
        self.sub = rospy.Subscriber('/sensors/IMU', Imu, self.onImuMessage)

    def onImuMessage(self, data):
        (data.linear_acceleration.x, data.linear_acceleration.y) = (data.linear_acceleration.y, data.linear_acceleration.x)
        data.linear_acceleration.z = -data.linear_acceleration.z

        (data.angular_velocity.x, data.angular_velocity.y) = (data.angular_velocity.y, data.angular_velocity.x)
        data.angular_velocity.z = -data.angular_velocity.z

        quat = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
        quat_out = [quat[1], quat[0], -quat[2], quat[3]]

        data.orientation.x = quat_out[0]
        data.orientation.y = quat_out[1]
        data.orientation.z = quat_out[2]
        data.orientation.w = quat_out[3]

        (r, p, y) = euler_from_quaternion(quat_out)
        
        print("ENU yaw: " + str(y))

        self.pub.publish(data)

if __name__ == '__main__':
    try:
        Node()

        rate = rospy.Rate(1)

        while not rospy.is_shutdown():
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass