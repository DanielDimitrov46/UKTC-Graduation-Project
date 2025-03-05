import serial
import time

# Set up the serial connection
ser = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)

def send_command(command):
    """Send command to the fingerprint sensor"""
    ser.write(command)
    time.sleep(0.1)
    return ser.read(12)  # Read response

def capture_fingerprint():
    """Capture a fingerprint image and generate a template"""
    GEN_IMG = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'  # Capture image command
    IMG_TO_TZ1 = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08'  # Convert image to template buffer 1

    print("[*] Capturing fingerprint...")
    response = send_command(GEN_IMG)
    
    if response[9] == 0x00:
        print("[+] Fingerprint captured successfully!")
    else:
        print("[-] Failed to capture fingerprint")
        return False

    print("[*] Converting image to template...")
    response = send_command(IMG_TO_TZ1)
    
    if response[9] == 0x00:
        print("[+] Template created successfully!")
        return True
    else:
        print("[-] Failed to create template")
        return False

def search_fingerprint():
    """Search fingerprint in the database"""
    SEARCH_CMD = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x08\x04\x01\x00\x00\x00\x03\x00\x0F'
    
    print("[*] Searching fingerprint...")
    response = send_command(SEARCH_CMD)
    
    if response[9] == 0x00:
        finger_id = response[10] * 256 + response[11]
        print(f"[+] Fingerprint matched! ID: {finger_id}")
    else:
        print("[-] No match found")

# Run fingerprint capture and search
if __name__ == "__main__":
    if capture_fingerprint():
        search_fingerprint()
