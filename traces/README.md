This folder contains packet traces used for the testing of our algorithm. Here follows a quick description of the traffic contained by each trace.

Ping of Death 1

	- IP: 192.168.1.165
	- Initial timestamp: 1527922140

	- Ideal Parameters:
		Best epoch: 2
		Best alpha: 0.94
		Best Key: ['dst','proto']
		Best Threshold: 0.54

	- Ideal Parameters:
		Best epoch: 4
		Best alpha: 0.91
		Best Key: ['src', 'dst', 'proto']
		Best Threshold: 0.54

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 20

Ping of Death 2

	- IP: 192.168.1.248
	- Initial timestamp: 1527938417

	- Ideal Parameters:
		Best epoch: 4
		Best alpha: 0.9
		Best Key: ['dst', 'proto']
		Best Threshold: 0.25

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 1

Smurf 1

	- IP: 192.168.1.118
	- Initial timestamp: 1540283108

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 25

Smurf 2

	- IP: 192.168.1.248
	- Initial timestamp: 1527965037

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.4
		False Positives: 10

SNMP Reflection 1 (Trace starts 6 seconds before the attack - not useful for bigger epochs)

	- IP: 192.168.1.248
	- Initial timestamp: 1528003135

SNMP Reflection 2

	- IP: 192.168.1.248
	- Initial timestamp: 1527958226

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 10

	- Ideal Parameters:
		Best epoch: 15
		Best alpha: 0.97
		Best Key: ['src', 'dst', 'proto']
		Best Threshold: 0.64
		False Positives: 2

TCP SYN 1

	- IP: 192.168.1.119
	- Initial timestamp: 1540309095
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.3
		False Positives: 242

TCP SYN 2

	- IP: 192.168.1.119
	- Initial timestamp: 1540462848
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 16

TCP SYN 3

	- IP: 192.168.1.223
	- Initial timestamp: 1527916395
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.87
		Best Key: ['src', 'dst', 'proto']
		Best Threshold: 0.88
		False Positives: 0

TCP SYN 4

	- IP: 192.168.1.241
	- Initial timestamp: 1527902817
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.8
		Best Key: ['src', 'dst', 'proto']
		Best Threshold: 0.82
		False Positives: 3

UDP Flood 1

	- IP: 192.168.1.239
	- Initial timestamp: 1540305374


UDP Flood 2

	- IP: 192.168.1.239
	- Initial timestamp: 1540251009

UDP Flood 3

	- IP: 192.168.1.165
	- Initial timestamp: 1527948284