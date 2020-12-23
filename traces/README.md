This folder contains packet traces used for the testing of our algorithm. Here follows a quick description of the traffic contained by each trace.

Ping of Death 1 - ping-of-death-100k-1.pcap

	- IP: 192.168.1.165
	- Initial timestamp: 1527922140

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 20

Ping of Death 2 - ping-of-death-100k-2.pcap

	- IP: 192.168.1.248
	- Initial timestamp: 1527938417

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 1

Smurf 1 - smurf-100k-1.pcap

	- IP: 192.168.1.118
	- Initial timestamp: 1540283108

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 27

Smurf 2 - smurf-100k-2.pcap

	- IP: 192.168.1.248
	- Initial timestamp: 1527965037

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.4
		False Positives: 10

SNMP Reflection 1 - snmp-reflection-100k-1.pcap

	- IP: 192.168.1.248
	- Initial timestamp: 1528003135

SNMP Reflection 2 - snmp-reflection-100k-2.pcap

	- IP: 192.168.1.248
	- Initial timestamp: 1527958226

	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 10

TCP SYN 1 - tcp-syn-100k-1.pcap

	- IP: 192.168.1.119
	- Initial timestamp: 1540309095
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.3
		False Positives: 242

TCP SYN 2 - tcp-syn-100k-2.pcap

	- IP: 192.168.1.119
	- Initial timestamp: 1540462848
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.6
		Best Key: ['src', 'sport', 'dst', 'dport', 'proto']
		Best Threshold: 0.5
		False Positives: 16

TCP SYN 3 - tcp-syn-100k-3.pcap

	- IP: 192.168.1.223
	- Initial timestamp: 1527916395
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.87
		Best Key: ['src', 'dst', 'proto']
		Best Threshold: 0.88
		False Positives: 0

TCP SYN 4 - tcp-syn-100k-4.pcap

	- IP: 192.168.1.241
	- Initial timestamp: 1527902817
	- Ideal Parameters:
		Best epoch: 20
		Best alpha: 0.8
		Best Key: ['src', 'dst', 'proto']
		Best Threshold: 0.82
		False Positives: 3

UDP Flood 1 - udp-flood-100k-1.pcap

	- IP: 192.168.1.239
	- Initial timestamp: 1540305374


UDP Flood 2 - udp-flood-100k-2.pcap

	- IP: 192.168.1.239
	- Initial timestamp: 1540251009

UDP Flood 3 - udp-flood-100k-3.pcap

	- IP: 192.168.1.165
	- Initial timestamp: 1527948284

MULTIPLE 1 - multiple-1-2M.pcap

	TCP SYN
		
		- IP: 192.168.1.241
		- Initial timestamp: 1527901207

	TCP SYN

		- IP: 192.168.1.165
		- Initial timestamp: 1527908393

	TCP SYN

		- IP: 192.168.1.223
		- Initial timestamp: 1527913194

	TCP SYN

		- IP: 192.168.1.248
		- Initial timestamp: 1527917995

	Ping-of-death

		- IP: 192.168.1.165
		- Initial timestamp: 1527918925

MULTIPLE 2 - multiple-2-1M.pcap

	Ping-of-death
		
		- IP: 192.168.1.223
		- Initial timestamp: 1527923756

	TCP SYN

		- IP: 192.168.1.227
		- Initial timestamp: 1527924398

	TCP SYN

		- IP: 192.168.1.241
		- Initial timestamp: 1527927598

	Ping-of-death

		- IP: 192.168.1.248
		- Initial timestamp: 1527935202


MULTIPLE 3 - multiple-3-1M.pcap

	SNMP

		- IP: 192.168.1.248
		- Initial timestamp: 1527956626

	Smurf

		- IP: 192.168.1.227
		- Initial timestamp: 1527956962

	Smurf

		- IP: 192.168.1.248
		- Initial timestamp: 1527961822

	SNMP

		- IP: 192.168.1.248
		- Initial timestamp: 1527968269