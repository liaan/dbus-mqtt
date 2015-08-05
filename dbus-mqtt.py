#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# Code is a quite raw copy from the pubnub code, but then with mqtt,

import os
import sys
import signal
import gobject
import argparse
import threading
import time
import json
import logging

logger = logging.getLogger(__name__)

from dbus.mainloop.glib import DBusGMainLoop

# Victron imports
sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext/velib_python'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext/paho-mqtt-client'))
from dbusmonitor import DbusMonitor
import datalist
from ve_utils import get_vrm_portal_id, exit_on_error

import client as mqtt

softwareversion = '0.02'
# Mqtt sever details
mqtt_host = "test.mosquitto.org"
mqtt_port = 1883

# The DataUpdateSender class receives all the dbus-dataupdate-events, and forwards them to mqtt
# if and when necessary.
class DbusMqtt:
	def __init__(self):
		d = DbusMonitor(datalist.vrmtree, self._value_changed_on_dbus)

		
		self._mqtt = mqtt.Client(client_id=get_vrm_portal_id(), clean_session=True, userdata=None)
		self._mqtt.loop_start()  # creates new thread and runs Mqtt.loop_forever() in it.
		self._mqtt.on_connect = self._on_connect
		self._mqtt.on_message = self._on_message
		self._mqtt.connect_async(mqtt_host, port=mqtt_port, keepalive=60, bind_address="")
		logger.debug('our client id (and also topic) is %s' % get_vrm_portal_id())

	#   servicename: for example com.victronenergy.dbus.ttyO1
	#   path: for example /Ac/ActiveIn/L1/V
	#   props: the dictionary containing the properties from the vrmTree
	#   changes: the changes, a tuple with GetText() and GetValue()
	#   instance: the deviceInstance
	def _value_changed_on_dbus(self, servicename, path, props, changes, instance):
		
		self._publish(path,changes['Value'])

	def _on_message(self, client, userdata, msg):
		logger.debug('message! userdata: %s, message %s' % (userdata, msg.topic+" "+str(msg.payload)))

	def _on_connect(self, client, userdata, flags, rc):
		"""
		RC definition:
		0: Connection successful
		1: Connection refused - incorrect protocol version
		2: Connection refused - invalid client identifier
		3: Connection refused - server unavailable
		4: Connection refused - bad username or password
		5: Connection refused - not authorised
		6-255: Currently unused.
		"""
		logger.debug('connected! client=%s, userdata=%s, flags=%s, rc=%s' % (client, userdata, flags, rc))

		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		# client.subscribe("$SYS/#")

	def _someone_watching(self):
		return True  # (self.lastKeepAliveRcd + self.ttl) > int(time.time())

	def _marshall_says_go(self):
		return (self._last_publish + self.ttm) < int(time.time())

	def _publish(self,topic,value):
		
		topic = '/victron' + topic
		payload = value
		logger.debug('publishing on topic "%s", data "%s"' % (topic, payload))

		self._mqtt.publish(topic, payload=payload, qos=0, retain=False)

def main():
	global mqtt_host
	global mqtt_port
	# Argument parsing
	parser = argparse.ArgumentParser(
		description='vrmmqttpub v%s: Mqtt publisher of D-Bus on the CCGX.' % softwareversion
	)

	parser.add_argument("-d", "--debug", help="set logging level to debug",
						action="store_true")

	parser.add_argument("-s", "--server", help='Mqtt Server, Default: %s ' % mqtt_host)
	parser.add_argument("-p", "--port", help="Mqtt Port, Default:  %s" % mqtt_port)

	
	args = parser.parse_args()

	# Init logging
	logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))
	
	if args.server:
		mqtt_host = args.server
    		logger.debug("Host: %s"%mqtt_host)
	if args.port:
		mqtt_port = args.port		    		
		logger.debug("Port: %s"%mqtt_port)	


	logger.info("%s v%s is starting up" % (__file__, softwareversion))
	logLevel = {0: 'NOTSET', 10: 'DEBUG', 20: 'INFO', 30: 'WARNING', 40: 'ERROR'}
	logger.info('Loglevel set to ' + logLevel[logging.getLogger().getEffectiveLevel()])

	# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
	DBusGMainLoop(set_as_default=True)

	dbusmqtt = DbusMqtt()

	# Start and run the mainloop
	logger.info("Starting mainloop, responding on only events")
	mainloop = gobject.MainLoop()
	mainloop.run()


if __name__ == "__main__":
	main()
