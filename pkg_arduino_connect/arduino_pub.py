import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class ArduinoPublisher(Node):

    def __init__(self):
        super().__init__('arduino_publisher')
        
        self.publisher_ = self.create_publisher(String, 'cmd_arduino', 10)
        
        #arduino serial
        arduino_serial = '/dev/ttyACM0'
        baudrate = 115200

        # Capture at 30fps
        timer_period = 0.03
        # Port série (adapter selon ton PC)
        self.ser = serial.Serial(arduino_serial, baudrate, timeout=1)
        
        self.timer = self.create_timer(timer_period, self.publisher_callback)

        self.colors = ["ROUGE", "VERT", "BLEU", "JAUNE", "CYAN", "MAGENTA", "BLANC"]
        self.i = 0

    def publisher_callback(self):
        cmd = self.colors[self.i]
        self.i = (self.i + 1) % len(self.colors)

        msg = String()
        msg.data = cmd

        self.publisher_.publish(msg)

        # Arduino attend une ligne terminée par \n
        self.ser.write((cmd + "\n").encode("utf-8"))

        self.get_logger().info(f"Sent to Arduino: {cmd}")


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()