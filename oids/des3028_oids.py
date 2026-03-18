"""DES-3028"""

OIDS = {
    "sysDescr": ".1.3.6.1.2.1.1.1.0",  # device
    "sysUpTime": ".1.3.6.1.2.1.1.3.0", # uptime
    "ifMDIState": ".1.3.6.1.4.1.171.11.63.6.2.2.2.1.3(.{№port.100})", # enab/disab port | INTEGER other(1),disabled(2),enabled(3)
    "ifOperStatus": ".1.3.6.1.2.1.2.2.1.8.{port}",  # link status on port | INTEGER link-up(1),link-down(2)
    "ifSpeed": ".1.3.6.1.4.1.171.11.63.6.2.2.1.1.5(.{№port.100or101(gig)})",  # speed port | INTEGER link-down(1),half-10Mbps(2),full-10Mbps(3),half-100Mbps(4),full-100Mbps(5),half-1Gigabps(6),full-1Gigabps(7)
    "ifInErrors": "",  # rx errors
    "ifOutErrors": "",  # tx errors
    "dhcpRelayState": ".1.3.6.1.4.1.171.12.42.1.1.0", # dhcp relay state
    "ifDefGateway": ".1.3.6.1.4.1.171.11.63.6.2.1.2.4.0", # default gateway
    "dot1qPvid": ".1.3.6.1.2.1.17.7.1.4.5.1.1(.{port})", # pvid vlan port
    "cpu5s": ".1.3.6.1.4.1.171.12.1.1.6.1.0", # cpu 5 s
    "cpu1m": ".1.3.6.1.4.1.171.12.1.1.6.2.0", # cpu 1 m
    "cpu5m": ".1.3.6.1.4.1.171.12.1.1.6.3.0", # cpu 5 m
}
