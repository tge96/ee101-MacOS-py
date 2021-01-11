import sys
import time
import serial
from serial.tools.list_ports import comports

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

def ask_for_port():
    """\
    Show a list of ports and ask the user for an index choice.
    """
    sys.stderr.write('\nAvailable ports: <index:> <name> <desc> <hwid>\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write('{:2}: {:40} {!r} {!r}\n'.format(n, port, desc, hwid))
        ports.append(port)
    while True:
        port = raw_input('Enter index ')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]
        return port    

# $ python3 -m pip install pyserial
# /dev/cu.usbserial-<XYZ> for mac,
#       ...you can find your XYZ using $ python3 -m serial.tools.list_ports -v
# My XYZ is "FTVHYZXQ", which matches my USB Serial adapter, model no. TTL232RG-VIP
#       ...another option for finding XYZ is to use $ ls /dev/cu.usb*
# Another useful pyserial utility is:  $ python3 -m serial.tools.miniterm

# Here's a simple brute force example:
# ser = serial.Serial("/dev/cu.usbserial-FTVHYZXQ",9600)

# To run:  $ python3 test_ee101_1wire.py

try:
    raw_input
except NameError:
    # pylint: disable=redefined-builtin,invalid-name
    raw_input = input   # in python3 it's "raw"
    unichr = chr  

time.sleep(1)
try:
    # ser.write(("Hello World\r\n".encode()))

    user_selected_port_name = ask_for_port()

    print("You selected " + user_selected_port_name)

    # open serial port
    ser = serial.Serial(user_selected_port_name,9600)

    print("Press CTL+C to exit program")

    i = 0

    while True:
        EE101Text(0,"Hello")
        EE101Text(1,"Tim")
        EE101Text(2,"this")
        EE101Text(3,"is")
        EE101Text(4,"your")
        EE101Text(5,"ee101")
        EE101Text(6,"ported to")
        EE101Text(7,"Python on macOS")

        i += 1

        EE101Value(0, i)
        EE101Value(1, i)
        EE101Value(2, i)
        EE101Value(3, i)
        EE101Value(4, i)
        EE101Value(5, i)
        EE101Value(6, i)
        EE101Value(7, i)

        # When tx>rx loopback is applied, one way to echo tx on rx is:
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
