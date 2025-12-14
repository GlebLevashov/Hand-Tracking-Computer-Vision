# Hand Tracking Robotic Hand Control

This project enables real-time control of a robotic hand using computer vision. It captures video from a webcam, detects hand landmarks using **MediaPipe**, calculates finger bending angles, and sends commands via serial to an **Arduino** to actuate 5 servo motors.

## 🛠️ Hardware Requirements

* **Arduino Board** (Uno)
* **5x Servo Motors** (one for each finger)
* **Webcam**
* **Power Supply** (External 5V supply for servos)
* Jumper wires & Breadboard

## 🔌 Wiring Configuration

| Finger | Arduino Pin |
| :--- | :--- |
| **Thumb** | Pin 13 |
| **Index** | Pin 12 |
| **Middle** | Pin 11 |
| **Ring** | Pin 10 |
| **Pinky** | Pin 9 |

### Circuit Diagram
Here is a wiring example showing two servos connected to an external power supply and an Arduino Uno. This setup should be replicated for all five servos.
![Rotating Spoon Arduino Schematic](Rotating%20Spoon%20Arduino%20Schematic.png)

## 💻 Software Installation

### 1. Python Environment
Install the required dependencies:

```bash
pip install opencv-python mediapipe pyserial tensorflow
