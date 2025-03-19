import serial
import time

# Set up the serial connection (Adjust the baudrate if needed)
ser = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)

def send_command(command, expected_length=12):
    """Send command to the fingerprint sensor and get response"""
    ser.write(command)
    time.sleep(0.1)
    
    response = ser.read(expected_length)  # Read expected bytes
    
    if len(response) < expected_length:
        print(f"[-] Incomplete response: {response.hex()}")
        return None  # Return None if response is too short
    
    return response

def capture_fingerprint():
    """Capture a fingerprint image and generate a template"""
    GEN_IMG = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'  # Capture image command
    IMG_TO_TZ1 = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08'  # Convert image to template buffer 1

    print("[*] Capturing fingerprint...")
    response = send_command(GEN_IMG)

    if response is None:
        print("[-] No response from sensor")
        return False

    if len(response) >= 10 and response[9] == 0x00:
        print("[+] Fingerprint captured successfully!")
    else:
        print(f"[-] Failed to capture fingerprint. Response: {response.hex()}")
        return False

    print("[*] Converting image to template...")
    response = send_command(IMG_TO_TZ1)

    if response is None:
        print("[-] No response from sensor")
        return False

    if len(response) >= 10 and response[9] == 0x00:
        print("[+] Template created successfully!")
        return True
    else:
        print(f"[-] Failed to create template. Response: {response.hex()}")
        return False

def store_fingerprint(finger_id):
    """Store fingerprint template in the database"""
    REG_MODEL = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x05\x00\x09'  # Create model from captured fingerprint
    STORE_CMD = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x06\x01' + finger_id.to_bytes(2, 'big') + b'\x00\x00'  # Store fingerprint in memory

    print("[*] Generating fingerprint model...")
    response = send_command(REG_MODEL)
    if response is None or len(response) < 10 or response[9] != 0x00:
        print("[-] Failed to generate model")
        return False

    print(f"[*] Storing fingerprint at ID {finger_id}...")
    response = send_command(STORE_CMD)
    if response is None or len(response) < 10 or response[9] != 0x00:
        print("[-] Failed to store fingerprint")
        return False
    
    print(f"[+] Fingerprint stored successfully at ID {finger_id}!")
    return True

def search_fingerprint():
    """Search fingerprint in the database"""
    SEARCH_CMD = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x08\x04\x01\x00\x00\x00\x03\x00\x0F'
    
    print("[*] Searching fingerprint...")
    response = send_command(SEARCH_CMD)

    if response is None:
        print("[-] No response from sensor")
        return
    
    if len(response) >= 12 and response[9] == 0x00:
        finger_id = response[10] * 256 + response[11]
        print(f"[+] Fingerprint matched! ID: {finger_id}")
        print("[ACCESS GRANTED]")
    else:
        print("[-] No match found")
        print("[ACCESS DENIED]")

# Main menu
if __name__ == "__main__":
    while True:
        print("\nFingerprint Scanner Menu:")
        print("1. Register Fingerprint")
        print("2. Search Fingerprint")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                finger_id = int(input("Enter an ID for this fingerprint (0-199): "))
                if 0 <= finger_id < 200:
                    if capture_fingerprint():
                        store_fingerprint(finger_id)
                else:
                    print("Invalid ID. Please enter a number between 0-199.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "2":
            search_fingerprint()
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, please select again.")
