from database.client import DatabaseClient
from config import DB_CONFIG, SNMP_COMMUNITY_RO, SNMP_VERSION
from snmp_client import SnmpSession


def main():
    db = DatabaseClient(DB_CONFIG)
    if not db.connect():
        print("Database connection error")
        return

    try:
        while True:
            number = input("\nuser number: ").strip()

            if number.lower() in ["exit", "quit", "q"]:
                print("Exit")
                break

            if not number:
                print("Enter number")
                continue

            users = db.get_user_by_number(number)

            if not users:
                print("User not found")
                continue

            user = users[0]
            switch_ip = user["switch"]
            port = user["port"]

            if not switch_ip or not port:
                print("No switch IP or port number")
                continue

            print(f"\n  USER DIAGNOSTICS | port: {port} switch: {switch_ip}\n")

            snmp = SnmpSession(switch_ip, SNMP_COMMUNITY_RO, SNMP_VERSION)

            sys_descr = snmp.get(".1.3.6.1.2.1.1.1.0")
            print(f"  Device: {sys_descr}")

            info = snmp.get_port_info(port)

            if info["speed"] and info["speed"].isdigit():
                speed = int(info["speed"]) // 1000000
            else:
                speed = "unknown"

            status_display = 'up' if info.get('status') == '1' else 'down' if info.get('status') == '2' else 'unknown'
            print(f"  Link: {status_display}")
            print(f"  Speed: {speed} Mbps")

            if info["in_errors"] and info["in_errors"].isdigit():
                print(f"  RX Errors: {info['in_errors']}")
            if info["out_errors"] and info["out_errors"].isdigit():
                print(f"  TX Errors: {info['out_errors']}")

            cpu = snmp.get_cpu_utilization()
            if cpu:
                print(f"  CPU: {cpu}")

            dhcp_relay = snmp.get_dhcp_relay_state()
            if dhcp_relay:
                print(f"  DHCP Relay: {dhcp_relay}")

    except KeyboardInterrupt:
        print("\nExit")
    finally:
        db.close()


if __name__ == "__main__":
    main()
