import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

class ArduinoPublisher(Node):

    def __init__(self):
        super().__init__('arduino_led_pub')
        
        self.publisher_ = self.create_publisher(String, 'arduino_led', 10)
        
        #arduino serial
        arduino_serial = '/dev/ttyACM0'
        baudrate = 115200
        timer_period = 0.1
        try:
            self.ser = serial.Serial(arduino_serial, baudrate, timeout=1)
            time.sleep(2)  # Attendre reset Arduino
            self.get_logger().info("Arduino connecté")

        except serial.SerialException as e:
            self.get_logger().error(f"Connexion échouée: {e}")
            self.ser = None

        self.colors = ["ROUGE", "VERT", "BLEU", "JAUNE", "CYAN", "MAGENTA", "BLANC"]
        self.i = 0
        self.timer = self.create_timer(timer_period, self.publisher_callback)

    def publisher_callback(self):
        cmd = self.colors[self.i]
        self.i = (self.i + 1) % len(self.colors)

        msg = String()
        msg.data = cmd
        self.publisher_.publish(msg)

        try:
            if self.ser and self.ser.is_open:
                self.ser.write((cmd + "\n").encode("utf-8"))
                self.get_logger().info(f"Sent: {cmd}")
        except serial.SerialException as e:
            self.get_logger().warn(f"Serial error: {e}")

    
    def destroy_node(self):
        if self.ser and self.ser.is_open:
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