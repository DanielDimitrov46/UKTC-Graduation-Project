import serial
import time

# Configure UART
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Make sure this is the correct port
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2  # Increased timeout for response
)

def send_command(command):
    """Send a command to the fingerprint sensor and read the response."""
    ser.write(command)
    time.sleep(0.5)  # Delay to allow processing

    # Try reading a response from the sensor
    response = ser.read(20)  # Adjust based on expected response length
    if response:
        print("Response:", response.hex())  # Print response in hex format
    else:
        print("No response received.")

# Construct the ADD Fingerprint command
command = bytes([0xBB]) + b'ADD' + bytes([0x0D])

# Send the command
send_command(command)

# Close the serial connection
ser.close()
