"""
Module establishes communication with explorer and agent dashboard
"""

import os
import paho.mqtt.client as mqtt

from nlp.dispatch import on_message

EXPLORER_TOPIC = 'nsf/explorer/command'
AI_TOPIC = 'nsf/ai/response'


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))


# def on_message(client, obj, msg):
#     print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#
#     # TODO(Alex) Remove dev test echo server
#     mqttc.publish(AI_TOPIC, 'echo: ' + str(msg.payload))


def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    print(string)


mqttc = mqtt.Client()


# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# mqttc.on_log = on_log


url_str = os.environ.get('AIRAMQTT_URL', 'preprod-mqtt.aira.io')
port = int(os.environ.get('AIRAMQTT_PORT', '1883'))


mqttc.connect(url_str, port, 60)

mqttc.subscribe(EXPLORER_TOPIC, 0)




if __name__ == '__main__':
    rc = 0

    while rc == 0:
        rc = mqttc.loop()
    print('rc: ' + str(rc))

