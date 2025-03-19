import serial
import time

# Configure UART
ser = serial.Serial(
    port='/dev/ttyAMA0',  
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2
)

def send_command(command):
    """Send command to fingerprint sensor and read response."""
    ser.write(command)
    time.sleep(1)  # Wait for processing

    response = ser.read(20)  # Read up to 20 bytes
    if response:
        print("Raw Response:", response.hex())  # Print raw hex response
    else:
        print("No response received.")

# Alternative fingerprint recognition command
command = bytes([0xBB]) + b'SEA' + bytes([0x0D])

print("Place your finger on the sensor...")
send_command(command)

ser.close()
