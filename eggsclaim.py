import signal
import sys
import serial
import sms
from xbee import ZigBee

SERIAL_PORT = '/dev/tty.usbserial-143'
MOBILE_NUM = '0400000000'
NOTIFICATION_MSG = 'Cock-a-doodle-doo! An egg is waiting for you!'

egg_was_present = False

def packet_received(packet):
    global egg_was_present
    print('Packet received!')
    samples = packet['samples'][0]
    egg_is_present = not samples['dio-1'] if 'dio-1' in samples else False

    if egg_is_present != egg_was_present:
        if egg_is_present:
            print('Egg(s) waiting, sending SMS notification!')
            #sms.send(MOBILE_NUM, NOTIFICATION_MSG) # Uncomment when SMS API is functional
        else:
            print('Egg(s) collected!')
    egg_was_present = egg_is_present

serial_port = serial.Serial(SERIAL_PORT, 9600)
xbee = ZigBee(serial_port, escaped=True)

while True:
    try:
        packet = xbee.wait_read_frame()
        packet_received(packet)
    except serial.serialutil.SerialException:
        pass
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()