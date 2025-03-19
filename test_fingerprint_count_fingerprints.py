import serial
import time

# Configure UART
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Make sure this is the correct port
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2  # Allow time for response
)

def send_command(command):
    """Send a command to the fingerprint sensor and read the response."""
    ser.write(command)
    time.sleep(0.5)  # Give sensor time to process

    # Try reading the response from the sensor
    response = ser.read(20)  # Read up to 20 bytes (adjust if needed)
    if response:
        print("Response:", response.hex())  # Print response in hex format
    else:
        print("No response received.")

# Construct the fingerprint count request command
command = bytes([0xBB]) + b'TMP' + bytes([0x0D])

# Send the command
send_command(command)

# Close the serial connection
ser.close()
