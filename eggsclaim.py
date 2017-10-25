import serial
from datetime import datetime
from pyfcm import FCMNotification
from xbee import ZigBee

API_KEY = ''
SERIAL_PORT = '/dev/tty.usbserial-143'

egg_was_present = False
push_service = FCMNotification(api_key=API_KEY)

def send_notification(egg_present):
    payload = {
        'timestamp' : datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'egg_present' : egg_present
    }
    extra_kwargs = {
    'priority': 'high'
    }
    result = push_service.notify_topic_subscribers(topic_name="updates", data_message=payload, extra_kwargs=extra_kwargs)

def packet_received(packet):
    global egg_was_present
    print('Packet received!')
    samples = packet['samples'][0]
    egg_is_present = not samples['dio-1'] if 'dio-1' in samples else False

    if egg_is_present != egg_was_present:
        if egg_is_present:
            print('Egg(s) waiting, sending notification!')
        else:
            print('Egg(s) collected, sending notification!')
        send_notification(egg_is_present)
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