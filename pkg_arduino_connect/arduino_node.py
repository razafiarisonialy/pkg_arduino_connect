import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool
import serial
import json

class ArduinoNode(Node):
    def __init__(self):
        super().__init__('arduino_node')

        # 2 Publishers
        self.pub_photo = self.create_publisher(Int32, 'arduino_phoResistor', 10)
        self.pub_bouton = self.create_publisher(Bool, 'arduino_bouton', 10)

        # Connexion Serial
        arduino_serial = '/dev/ttyACM0'
        baudrate = 115200
        timer_period = 0.03
        self.ser = serial.Serial(arduino_serial, baudrate, timeout=1)

        self.timer = self.create_timer(timer_period, self.publisher_callback)


    def publisher_callback(self):
        if self.ser.in_waiting > 0:
            try:
                ligne = self.ser.readline().decode('utf-8').strip()
                data = json.loads(ligne)

                # Publisher photoResistor
                msg_photo = Int32()
                msg_photo.data = int(data['photoResistor'])
                self.pub_photo.publish(msg_photo)

                # Publisher bouton
                msg_bouton = Bool()
                msg_bouton.data = bool(data['bouton'])
                self.pub_bouton.publish(msg_bouton)

                self.get_logger().info(f'Photo: {msg_photo.data} | Bouton: {msg_bouton.data}')

            except (json.JSONDecodeError, KeyError) as e:
                self.get_logger().warn(f'Erreur lecture: {e}')
    
    def destroy_node(self):
        if self.ser.is_open:
            self.ser.close()
            self.get_logger().info("Serial port closed")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()