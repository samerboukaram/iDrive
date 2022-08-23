
import serial

ser = serial.Serial(port="/dev/serial0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

while True:
    data_buf = ser.read(16)
    data = data_buf[2:]
