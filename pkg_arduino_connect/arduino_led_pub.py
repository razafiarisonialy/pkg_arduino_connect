import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import time

class LedColorNode(Node):
    def __init__(self):
        super().__init__('led_color_node')

        self.pub_led = self.create_publisher(String, 'arduino_led_cmd', 10)

        self.colors_valides = ["ROUGE", "VERT", "BLEU", "JAUNE", "CYAN", "MAGENTA", "BLANC", "OFF"]

        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

        self.get_logger().info("LedColorNode démarré")
        self.get_logger().info(f"Couleurs disponibles: {self.colors_valides}")

    def input_loop(self):
        while rclpy.ok():
            try:
                color = input("Entrer une couleur: ").upper().strip()

                if color in self.colors_valides:
                    self.publish_color(color)
                else:
                    print(f"Couleur invalide. Choisir parmi: {self.colors_valides}")

            except EOFError:
                break

    def publish_color(self, color):
        msg      = String()
        msg.data = color
        self.pub_led.publish(msg)
        self.get_logger().info(f"Couleur publiée: {color}")

    def destroy_node(self):
        self.publish_color("OFF")
        time.sleep(0.1)
        self.get_logger().info("OFF envoyé")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LedColorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()