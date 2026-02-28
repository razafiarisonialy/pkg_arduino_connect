import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class ArduinoPublisher(Node):

    def __init__(self):
        super().__init__('arduino_publisher')
        
        self.publisher_ = self.create_publisher(String, 'arduino_led', 10)
        
        #arduino serial
        arduino_serial = '/dev/ttyACM0'
        baudrate = 115200
        timer_period = 0.03
        self.ser = serial.Serial(arduino_serial, baudrate, timeout=1)


        self.colors = ["ROUGE", "VERT", "BLEU", "JAUNE", "CYAN", "MAGENTA", "BLANC"]
        self.i = 0
        self.timer = self.create_timer(timer_period, self.publisher_callback)

    def publisher_callback(self):
        cmd = self.colors[self.i]
        self.i = (self.i + 1) % len(self.colors)

        msg = String()
        msg.data = cmd

        self.publisher_.publish(msg)

        # Arduino attend une ligne terminée par \n
        self.ser.write((cmd + "\n").encode("utf-8"))
        self.get_logger().info(f"Sent to Arduino: {cmd}")
    
    def destroy_node(self):
        if self.ser.is_open:
            self.ser.close()
            self.get_logger().info("Serial port closed")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()