#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>

// Функция за инициализиране на UART
int init_uart(const char *device, int baudrate) {
    int uart_fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if (uart_fd == -1) {
        perror("Неуспешно отваряне на UART");
        return -1;
    }

    struct termios options;
    tcgetattr(uart_fd, &options);

    cfsetispeed(&options, baudrate);
    cfsetospeed(&options, baudrate);

    options.c_cflag = CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;

    tcflush(uart_fd, TCIFLUSH);
    tcsetattr(uart_fd, TCSANOW, &options);

    return uart_fd;
}

// Функция за изпращане на команда към сензора
void send_command(int uart_fd, unsigned char *command, int length) {
    int bytes_written = write(uart_fd, command, length);
    if (bytes_written < 0) {
        perror("Грешка при изпращане на данни");
    }
}

// Функция за четене на отговор от сензора
int read_response(int uart_fd, unsigned char *response, int length) {
    int bytes_read = read(uart_fd, response, length);
    if (bytes_read < 0) {
        perror("Грешка при четене на отговор");
        return -1;
    } else if (bytes_read == 0) {
        printf("❌ Няма отговор от сензора.\n");
        return -1;
    } else {
        printf("Отговор: ");
        for (int i = 0; i < bytes_read; i++) {
            printf("%02X ", response[i]);
        }
        printf("\n");
        return bytes_read;
    }
}

// Функция за проверка на пръстов отпечатък
void verify_fingerprint(int uart_fd) {
    unsigned char command[] = {0xBB, 'V', 'E', 'R', 0x0D}; // Команда за проверка на отпечатък
    send_command(uart_fd, command, sizeof(command));

    unsigned char response[10]; // Буфер за отговор
    int bytes_received = read_response(uart_fd, response, sizeof(response));

    if (bytes_received > 0) {
        if (response[1] == 0x00) { 
            printf("✅ Пръстовият отпечатък е РАЗПОЗНАТ! (ID: %d)\n", response[2]); 
        } else if (response[1] == 0x01) { 
            printf("❌ Отпечатъкът НЕ е разпознат.\n"); 
        } else if (response[1] == 0x09) { 
            printf("⚠ Няма съвпадение в базата данни.\n"); 
        } else { 
            printf("⚠ Неизвестен отговор: %02X\n", response[1]); 
        }
    }
}

// Главна програма
int main() {
    const char *uart_device = "/dev/serial0"; // UART портът
    int uart_fd = init_uart(uart_device, B9600); // Инициализация на UART

    if (uart_fd == -1) {
        return 1;
    }

    printf("Поставете пръста си върху сензора за проверка...\n");
    verify_fingerprint(uart_fd);

    close(uart_fd); // Затваряне на UART
    return 0;
}
