import serial
import time

# Настройка на UART
ser = serial.Serial(
    port='/dev/ttyAMA10',  # Увери се, че е правилният порт (може да пробваш и /dev/ttyAMA10)
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2  # Изчаква 2 секунди за отговор
)

def send_command(command):
    """Изпраща команда към сензора и връща отговора."""
    ser.write(command)
    time.sleep(1)  # Изчакване за обработка

    response = ser.read(10)  # Четем до 10 байта отговора
    if response:
        print("Отговор от сензора:", response.hex())  # Показва отговора в HEX
        return response
    else:
        print("❌ Няма отговор от сензора.")
        return None

def verify_fingerprint():
    """Изпраща команда за проверка на отпечатък и анализира отговора."""
    command = bytes([0xBB]) + b'VER' + bytes([0x0D])  # Команда за проверка
    response = send_command(command)

    if response:
        if response[1] == 0x00:  
            print(f"✅ Пръстовият отпечатък е разпознат! ID: {response[2]}")
        elif response[1] == 0x01:  
            print("❌ Пръстовият отпечатък НЕ е разпознат.")
        elif response[1] == 0x09:  
            print("⚠ Няма съвпадение в базата данни.")
        else:  
            print(f"⚠ Неизвестен отговор: {response.hex()}")

# Проверка на отпечатък
print("Поставете пръста си върху сензора за проверка...")
verify_fingerprint()

# Затваряме UART връзката
ser.close()
