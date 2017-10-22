import signal
import sys
import serial
import sms
from xbee import XBee

SERIAL_PORT = '/dev/tty.usbserial-143'
MOBILE_NUM = '0400000000'
NOTIFICATION_MSG = 'Cock-a-doodle-doo! An egg is waiting for you!'

egg_was_present = False

def signal_handler(signal, frame):
    xbee.halt()
    serial_port.close()
    sys.exit(0)

def packet_received(packet):
    samples = packet['samples'][0]
    egg_is_present = samples['dio-1'] if 'dio-1' in samples else False

    if egg_is_present and egg_is_present != egg_was_present:
        sms.send(MOBILE_NUM, NOTIFICATION_MSG)
    egg_was_present = egg_is_present

signal.signal(signal.SIGINT, signal_handler)

serial_port = serial.Serial(SERIAL_PORT, 9600)
xbee = XBee(serial_port, callback=packet_received)