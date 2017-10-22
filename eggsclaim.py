import signal
import sys
import serial
import sms
from xbee import XBee

egg_was_present = False

def signal_handler(signal, frame):
    xbee.halt()
    serial_port.close()
    sys.exit(0)

def packet_received(packet):
    samples = packet['samples'][0]
    egg_is_present = samples['dio-4'] if 'dio-4' in samples else False

    if egg_is_present and egg_is_present != egg_was_present:
        sms.send_sms("", "Cock-a-doodle-doo! An egg is waiting for you!")
    egg_was_present = egg_is_present

signal.signal(signal.SIGINT, signal_handler)

serial_port = serial.Serial('/dev/ttyp0', 9600)
xbee = XBee(serial_port, callback=packet_received)