import serial
import time

# Настройка на UART порта
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Или /dev/ttyAMA10, ако използваш него
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2
)

def verify_fingerprint():
    """Чете отговора от сензора и проверява дали има съвпадение."""
    response = ser.read(10)  # Четем до 10 байта отговора

    if response:
        print(f"⬅ Отговор от сензора: {response.hex()}")  # Принтира отговора в HEX

        # Проверяваме дали първите 4 байта са "BB F O K"
        if len(response) >= 5 and response[0] == 0xBB and response[1] == ord('F') and response[2] == ord('O') and response[3] == ord('K'):
            fp_number = response[4]  # ID на разпознатия отпечатък
            print(f"✅ Пръстовият отпечатък е разпознат! ID: {fp_number}")
            return fp_number
        else:
            print("❌ Пръстовият отпечатък НЕ е разпознат.")
            return None
    else:
        print("⚠ Няма отговор от сензора.")
        return None

# Безкраен цикъл за следене на пръстови отпечатъци
print("📡 Чакаме пръстов отпечатък...")
while True:
    fingerprint_id = verify_fingerprint()
    if fingerprint_id:
        print("🔓 Отваряне на вратата...")
        break  # Излизаме от цикъла при разпознат отпечатък

    time.sleep(2)  # Изчакване преди нова проверка

# Затваряме порта (ако кодът някога завърши)
ser.close()
