import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RFIDReader:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def read_rfid(self):
        try:
            text = self.reader.read()
            if text.strip().lower() == "admin":
                return True
            else:
                return False
        except:
            return False
        finally:
            GPIO.cleanup()