/*********************************************************
***************** PARSER *********************************
**********************************************************/

parser MyParser(packet_in packet,
	 	out headers hdr,
		inout metadata meta,
		inout standard_metadata_t standard_metadata) {

    state start {
	transition parse_ethernet;
    }

    state parse_ethernet {
	packet.extract(hdr.ethernet);
	transition select(hdr.ethernet.etherType) {
	    TYPE_IPV4: parse_ipv4;
	    default: accept;
	}
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.fragOffset, hdr.ipv4.ihl,
                          hdr.ipv4.protocol) {
            (13w0x0, 4w0x5, IP_PROTOCOLS_TCP): parse_tcp;
            (13w0x0, 4w0x5, IP_PROTOCOLS_UDP): parse_udp;
            default: accept;
        }
    }

    state parse_tcp {
	packet.extract(hdr.tcp);
	transition accept;
    }

    state parse_udp {
	packet.extract(hdr.udp);
	transition accept;
    }
}