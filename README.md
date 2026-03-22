# pkg_arduino_connect

Package ROS2 pour la communication entre un Raspberry Pi et un Arduino.  
Contrôle d'une LED RGB, lecture d'une photorésistance et d'un bouton.


---



## Prérequis

- ROS2 Jazzy installé sur le Raspberry Pi: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
- Arduino flashé avec le fichier `arduino_led_photo_button.ino`


---



## Installation

```bash
cd ~/ros2_ws/src
git clone https://github.com/razafiarisonialy/pkg_arduino_connect.git

cd ~/ros2_ws
colcon build --packages-select pkg_arduino_connect
source install/setup.bash
```


---



## Configuration


### Topics

| Topic | Type | Description |
|-------|------|-------------|
| `arduino_led_cmd` | `String` | Commande couleur LED |
| `arduino_photoResistor` | `Int32` | Valeur lumière (0–255) |
| `arduino_bouton` | `Bool` | État du bouton |


### Câblage Arduino

| Broche | Composant |
|--------|-----------|
| Pin 8 | LED Vert |
| Pin 9 | LED Rouge |
| Pin 10 | LED Bleu |
| A0 | Photorésistance |
| Pin 2 | Bouton |


### Connection arduino et raspberry pi

**1. Vérifier le port série :**
```bash
ls /dev/ttyACM*
```
Le port doit afficher `/dev/ttyACM0`. Si ce n'est pas le cas, modifier la variable `arduino_serial` dans `arduino_node.py` avec le bon port.

**2. Vérifier le baudrate :**
```bash
stty -F /dev/ttyACM0
```
La ligne `speed` doit afficher `115200`. Si ce n'est pas le cas, vérifier que le sketch Arduino est bien flashé avec `Serial.begin(115200)`.


---



## Lancement

Ouvrir deux terminaux (sourcer `install/setup.bash` dans chacun) :

**Terminal 1 — bridge Arduino :**
```bash
ros2 run pkg_arduino_connect arduino_node
```

**Terminal 2 — contrôle LED :**
```bash
ros2 run pkg_arduino_connect arduino_led_pub
```

Entrer ensuite une couleur : `ROUGE`, `VERT`, `BLEU`, `JAUNE`, `CYAN`, `MAGENTA`, `BLANC` ou `OFF`.

