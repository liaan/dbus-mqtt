See https://github.com/mpvader/ccgx-messaging/wiki for more info.

this is a test project to get a bit familiar with mqtt, and see how it could link
into a CCGX and its dbus structure.

To install on a CCGX, first install git:

	root@bpp3:~# opkg install git
	Package git (1.7.7-r2) installed in root is up to date.

Then install the rest:

	root@bpp3:~# cd /data/

	root@bpp3:/data# git clone https://github.com/mpvader/dbus-mqtt.git
	Cloning into dbus-mqtt...
	remote: Counting objects: 22, done.
	remote: Compressing objects: 100% (19/19), done.
	remote: Total 22 (delta 2), reused 14 (delta 0), pack-reused 0
	Unpacking objects: 100% (22/22), done.

	root@bpp3:/data# cd dbus-mqtt/

	root@bpp3:/data/dbus-mqtt# git submodule update --init
	Submodule 'ext/velib_python' (https://github.com/victronenergy/velib_python.git)                                                                                                                      registered for path 'ext/velib_python'
	Cloning into ext/velib_python...
	remote: Counting objects: 386, done.
	remote: Compressing objects: 100% (9/9), done.
	remote: Total 386 (delta 3), reused 0 (delta 0), pack-reused 377
	Receiving objects: 100% (386/386), 113.30 KiB | 81 KiB/s, done.
	Resolving deltas: 100% (223/223), done.
	Submodule path 'ext/velib_python': checked out '882118b5133ce64a0e76b366fe6f86b73d4a9155'

Run it:

	root@bbp3:/data/dbus-mqtt# ./dbus-mqtt.py
	INFO:__main__:./dbus-mqtt.py v0.01 is starting up
	INFO:__main__:Loglevel set to DEBUG
	INFO:dbusmonitor:===== Search on dbus for services that we will monitor starting... =====
	INFO:dbusmonitor:Found: com.victronenergy.battery.ttyO1 matches com.victronenergy.battery, scanning and storing items
	INFO:dbusmonitor:       com.victronenergy.battery.ttyO1 has device instance 0
	INFO:dbusmonitor:===== Search on dbus for services that we will monitor finished =====
	DEBUG:__main__:our client id (and also topic) is 08002705350c
	INFO:__main__:Starting mainloop, responding on only events
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:connected! client=<client.Client object at 0xb696fe6c>, userdata=None, flags={'session present': 0}, rc=0
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"
	DEBUG:__main__:publishing on topic "/08002705350c", data "hello world!"

And this in another one (make sure to change the client id with yours, see above):

	$ mosquitto_sub -h test.mosquitto.org -t "/08002705350c" -v
	/08002705350c hello world!
	/08002705350c hello world!
	/08002705350c hello world!
	/08002705350c hello world!
	/08002705350c hello world!
	/08002705350c hello world!
	/08002705350c hello world!
	/08002705350c hello world!

In case you do not see those hello worlds comming, it is perhaps because you didn't completely follow these
instructions, and chose to run dbus-mqtt on a PC instead of a CCGX? No problem, to make something happen on
a PC, open a third terminal and run ./test/dummy_vebus.py
