import time
from sensors.face_recognition import FaceRecognition
from sensors.rfid_read import RFIDReader
from sensors.fingerprint_recognition_response import FingerprintReader
import relay_control

def trigger_relay():
    print("🔓 Задействане на релето...")
    relay_control.control_relay(relay_control.RELAY1_PIN, relay_control.GPIO.LOW)
    time.sleep(5)
    relay_control.control_relay(relay_control.RELAY1_PIN, relay_control.GPIO.HIGH)


def main():
    face = FaceRecognition().run_recognition()
    rfid = RFIDReader()
    fingerprint = FingerprintReader()

    while True:
        if face.run_recognition():
            print("✅ Лице разпознато.")
            trigger_relay()
        elif rfid.read_rfid():
            print("✅ RFID съвпадение.")
            trigger_relay()
        elif fingerprint.verify_fingerprint():
            print("✅ Пръстов отпечатък съвпадение.")
            trigger_relay()

        time.sleep(1)


if __name__ == "__main__":
    main()