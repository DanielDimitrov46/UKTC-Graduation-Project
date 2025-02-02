import time

import RPi.GPIO as GPIO

# Set up the GPIO pins
RELAY1_PIN = 23
RELAY2_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY1_PIN, GPIO.OUT)
GPIO.setup(RELAY2_PIN, GPIO.OUT)

# Function to control the relays
def control_relay(relay, state):
    GPIO.output(relay, state)

try:
    while True:
        command = input("Enter command (1/2/on/off): ")
        if command == "1":
        # Turn on Relay 1
            control_relay(RELAY1_PIN, GPIO.HIGH)
            print("Relay 1 ON")
            control_relay(RELAY2_PIN, GPIO.LOW)
            print("Relay 2 OFF")
        elif command == "2":
            control_relay(RELAY1_PIN, GPIO.LOW)
            print("Relay 1 OFF")
            control_relay(RELAY2_PIN, GPIO.HIGH)
            print("Relay 2 ON")
        elif command == "on":
            control_relay(RELAY1_PIN, GPIO.HIGH)
            print("Relay 1 ON")
            control_relay(RELAY2_PIN, GPIO.HIGH)
            print("Relay 2 ON")
        elif command == "off":
            control_relay(RELAY1_PIN, GPIO.LOW)
            print("Relay 1 off")
            control_relay(RELAY2_PIN, GPIO.LOW)
            print("Relay 2 off")
except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()