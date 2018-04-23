#!/usr/bin/env python

import json
import os
import sys

from socket import error as socket_error

import paho.mqtt.client as mqtt

from SnipsMqttServer import SnipsMqttServer
sys.path.append('')

class SnipsHotwordServer(SnipsMqttServer):

    def __init__(self,
                 mqtt_hostname=os.environ.get('mqtt_hostname','localhost'),
                 mqtt_port=os.environ.get('mqtt_port',1883),
                 listen_to=os.environ.get('hotword_listen_to','default'),
                 ):
        SnipsMqttServer.__init__(self,mqtt_hostname,mqtt_port)

        self.subscribe_to='hermes/hotword/toggleOff,hermes/hotword/toggleOn'
        self.listen_to = listen_to
        self.clientList = []
        self.allowedClientList = listen_to.split(',')
        #self.set_everloop_color(0,10,0,0)

    def set_everloop_color(self, red, green, blue, white):
        color_array = bytearray()
        for x in range(0,34):
            color_array += bytearray([red, green, blue, white])
        with open('/dev/matrixio_everloop','wb') as bin_file:
            bin_file.write(color_array)
        bin_file.close()

    def on_connect(self, client, userdata, flags, result_code):
        SnipsMqttServer.on_connect(self,client,userdata,flags,result_code)
        # enable to start
        for site in self.allowedClientList:
            self.client.publish('hermes/hotword/toggleOn', payload="{\"siteId\":\"" + site + "\",\"sessionId\":null}", qos=0)
    def on_message(self, client, userdata, msg):
        if msg.topic.endswith('toggleOff'):
            try:
                msgJSON = json.loads(msg.payload)
            except:
                pass
            siteId = msgJSON.get('siteId','default')
            for site in self.allowedClientList:
              if site == siteId:
               self.log('{} toggleOff'.format(site))
               self.set_everloop_color(0,10,0,0)
        elif msg.topic.endswith('toggleOn'):
            msgJSON = {}
            try:
                msgJSON = json.loads(msg.payload)
            except:
                pass
            siteId = msgJSON.get('siteId','default')
            for site in self.allowedClientList:
              if site == siteId:
               self.log('{} toggleOn'.format(site))
               self.set_everloop_color(0,0,0,10)

    def log(self, message):
        print(message)

server = SnipsHotwordServer()
server.start() 
