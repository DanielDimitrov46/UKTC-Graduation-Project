import serial
import time

# Configure UART
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Change to the correct port if needed
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

def send_command(command):
    """Send a command to the fingerprint sensor."""
    ser.write(command)
    time.sleep(0.2)  # Equivalent to _delay_ms(200) in C
    response = ser.read(10)  # Adjust based on expected response length
    print("Response:", response.hex())  # Print response in hex format

# Constructing the LED RED command
command = bytes([0xBB]) + b'RED' + bytes([0x0D])

# Send the command
send_command(command)

# Close the serial connection
ser.close()
