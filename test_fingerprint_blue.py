import serial
import time

# Configure UART
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Use the correct port that worked for you
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1  # Increase timeout to wait for response
)

def send_command(command):
    """Send a command to the fingerprint sensor and read the response."""
    ser.write(command)
    time.sleep(0.2)  # Delay to allow processing

    # Read available response data
    response = ser.read(10)  # Adjust if needed
    if response:
        print("Response:", response.hex())  # Print response in hex format
    else:
        print("No response received.")

# Construct the LED BLUE command
command = bytes([0xBB]) + b'BLU' + bytes([0x0D])

# Send the command
send_command(command)

# Close the serial connection
ser.close()
