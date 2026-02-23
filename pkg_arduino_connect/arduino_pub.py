import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class ArduinoPublisher(Node):

    def __init__(self):
        super().__init__('arduino_publisher')
        
        self.publisher_ = self.create_publisher(String, 'cmd_arduino', 10)
        
        #arduino serial
        arduino_serial = '/dev/ttyUSB0'
        # Capture at 30fps
        timer_period = 0.03
        # Port série (adapter selon ton PC)
        self.ser = serial.Serial(arduino_serial, 115200, timeout=1)
        
        self.timer = self.create_timer(timer_period, self.publisher_callback)

    def publisher_callback(self):
        msg = String()
        msg.data = '1'
        
        self.publisher_.publish(msg)
        self.ser.write(msg.data.encode())
        
        self.get_logger().info(f'Sent: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()