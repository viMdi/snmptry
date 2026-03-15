from snmp_client import SnmpSession
from config import SNMP_COMMUNITY_RO, SNMP_VERSION

def test_basic_connection(host):
    print(f"\nТестируем базовое SNMP к {host}...")

    snmp = SnmpSession(host, SNMP_COMMUNITY_RO, SNMP_VERSION)

    # пробуем несколько базовых OID
    oids = [
        (".1.3.6.1.2.1.1.1.0", "sysDescr"),
        (".1.3.6.1.2.1.1.5.0", "sysName"),
        (".1.3.6.1.2.1.1.4.0", "sysContact"),
        (".1.3.6.1.2.1.1.6.0", "sysLocation"),
    ]

    for oid, name in oids:
        value = snmp.get(oid)
        print(f"  {name}: {value}")

    # проверим порт
    port_status = snmp.get_port_status(5)
    print(f"  Port 5 status: {port_status}")

if __name__ == "__main__":
    test_basic_connection("10.134.128.178")
