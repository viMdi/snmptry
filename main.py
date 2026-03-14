from config import DB_CONFIG, SNMP_COMMUNITY_RO, SNMP_COMMUNITY_RW, SNMP_VERSION
from snmp_client import SnmpSession


def test_snmp_connection(host, port):
    print(f"\nТестируем SNMP к {host}... и проверяем порт {port}")

    snmp = SnmpSession(host, SNMP_COMMUNITY_RO, SNMP_VERSION)

    sys_descr = snmp.get(".1.3.6.1.2.1.1.1.0")  # описание устройства
    status_link = snmp.get_port_status(port)
    mac_fdb = snmp.get_port_mac(port)

    status_txt = "up" if status_link == "1" else "down" if status_link == "2" else "unknown"

    if sys_descr:
        print(f"  Name sw: {sys_descr}")
        print(f"  Link status: {status_txt}")
        print(f"  Mac on port: {mac_fdb}")
        return True
    else:
        print("  Не удалось подключиться по SNMP")
        return False


def main():
    print("Snmp diaga statr")
    test_snmp_connection("10.134.128.178", 5)


if __name__ == "__main__":
    main()
