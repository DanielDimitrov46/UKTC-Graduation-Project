import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RFIDReader:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def read_rfid(self):
        try:
            id, text = self.reader.read()
            return text.strip().lower() == "admin"
        except:
            return False
        finally:
            GPIO.cleanup()