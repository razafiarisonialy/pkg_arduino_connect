import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool, String
import serial
import json
import time
class ArduinoNode(Node):
    def __init__(self):
        super().__init__('arduino_node')

        self._init_publishers()
        self._init_subscribers()
        self._init_serial()

        self.current_color = "OFF"
        self.previous_color = None 
        self.create_timer(0.1, self.publisher_callback)

    def _init_publishers(self):
        self.pub_photo  = self.create_publisher(Int32,  'arduino_photoResistor', 10)
        self.pub_bouton = self.create_publisher(Bool,   'arduino_bouton', 10)
        self.get_logger().info("Publishers initialisés")

    def _init_subscribers(self):
        self.sub_color = self.create_subscription(
            String,
            'arduino_led_cmd',
            self.subscriber_callback,
            10
        )
        self.get_logger().info("Subscribers initialisés")

    def _init_serial(self):
        try:
            arduino_serial = '/dev/ttyACM0'
            baudrate = 115200
            self.ser = serial.Serial(arduino_serial, baudrate, timeout=1)
            time.sleep(2)
            self.get_logger().info("Arduino connecté sur /dev/ttyACM0")
        except serial.SerialException as e:
            self.get_logger().error(f"Connexion échouée: {e}")
            self.ser = None
    
    def subscriber_callback(self, msg):
        couleurs_valides = ["ROUGE", "VERT", "BLEU", "JAUNE", "CYAN", "MAGENTA", "BLANC", "OFF"]
        color = msg.data.upper().strip()

        if color in couleurs_valides:
            self.current_color = color
            self.get_logger().info(f"Couleur reçue: {color}")
        else:
            self.get_logger().warn(f"Couleur invalide: {color}")
    
    def publisher_callback(self):
        if not self.ser or not self.ser.is_open:
            return
        self.send_color()
        self.read_serial()

    def send_color(self):
        if self.current_color == self.previous_color:
            return
        
        try:
            self.ser.write((self.current_color + "\n").encode("utf-8"))
            self.previous_color = self.current_color
            self.get_logger().info(f"Couleur envoyée: {self.current_color}")
        except serial.SerialException as e:
            self.get_logger().error(f"Erreur Serial write: {e}")
            self.ser = None

    def read_serial(self):
        if self.ser.in_waiting == 0:
            return

        try:
            ligne = self.ser.readline().decode('utf-8').strip()
            data  = json.loads(ligne)

            self.publish_photo(data)
            self.publish_bouton(data)

        except json.JSONDecodeError:
            self.get_logger().warn("JSON invalide, ligne ignorée")
        except KeyError as e:
            self.get_logger().warn(f"Clé manquante: {e}")
        except serial.SerialException as e:
            self.get_logger().error(f"Erreur Serial read: {e}")
            self.ser = None

    def publish_photo(self, data):
        msg       = Int32()
        msg.data  = int(data['photoResistor'])
        self.pub_photo.publish(msg)
        self.get_logger().info(f"Photo: {msg.data}")

    def publish_bouton(self, data):
        msg       = Bool()
        msg.data  = bool(data['bouton'])
        self.pub_bouton.publish(msg)
        self.get_logger().info(f"Bouton: {msg.data}")
    
    def destroy_node(self):
        try:
            if self.ser and self.ser.is_open:
                off = "OFF"
                self.ser.write((off + "\n").encode("utf-8"))
                self.get_logger().info("LED éteinte")
                time.sleep(0.1) 
                self.ser.close()
                self.get_logger().info("Serial port closed")
        except serial.SerialException as e:
            self.get_logger().error(f"Erreur Serial: {e}")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()