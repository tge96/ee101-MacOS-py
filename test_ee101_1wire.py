import time
import serial

def EE101Text(channel, text):
    EE101_SYNC = 0x50
    EE101_TEXT_TYPE = 0x00
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_TEXT_TYPE]))
    ser.write(text.encode())
    ser.write(bytes([0]))

def EE101Value(channel, value):
    EE101_SYNC = 0x50
    EE101_VALUE_TYPE = 0x80
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_VALUE_TYPE]))
    ser.write(bytes([(int(value >> 24))]))
    ser.write(bytes([(int(value >> 16))]))
    ser.write(bytes([(int(value >> 8))]))
    ser.write(bytes([(int(value) & 0xFF)]))

print("Press CTL+C to exit program")

# $ python3 -m pip install pyserial
# /dev/cu.usbserial<XYZ> for mac,
#       ...find XYZ using $ ls /dev/cu.usb*
# $ python3 test_ee101_1wire.py
ser = serial.Serial("/dev/cu.usbserial-FTVHYZXQ",9600)

# /dev/serial0 for raspberry pi 3B+
#ser = serial.Serial("/dev/serial0",
#                    baudrate=9600,
#                    parity=serial.PARITY_NONE,
#                    stopbits=serial.STOPBITS_ONE,
#                    bytesize=serial.EIGHTBITS
#                    )

time.sleep(1)
try:
    #ser.write(("Hello World\r\n".encode()))

    i = 0

    #print ("Apply loopback wire from header pins 8 (uart.tx) to 10 (uart.rx)")
    while True:
        EE101Text(0,"Hello")
        EE101Text(1,"Tim")
        EE101Text(2,"this")
        EE101Text(3,"is")
        EE101Text(4,"your")
        EE101Text(5,"ee101")
        EE101Text(6,"ported to")
        EE101Text(7,"Python on MacOS")

        i += 1
        #if i == 256:
        #    i = 0
        EE101Value(0, i)
        EE101Value(1, i)
        EE101Value(2, i)
        EE101Value(3, i)
        EE101Value(4, i)
        EE101Value(5, i)
        EE101Value(6, i)
        EE101Value(7, i)

        # tx>rx loopback wire applied on header pins 8 and 10
        #if ser.inWaiting() > 0:
        #    data = ser.read()
        #    print(data)

except KeyboardInterrupt:
    print("Exiting Program")

except:
    print("Error Occurs, Exiting Program")

finally:
    ser.close()
pass
