import subprocess


class SnmpSession:
    def __init__(self, host, community, version=2):
        self.host = host
        self.community = community
        self.version = version

    def get(self, oid):
        try:
            cmd = ["snmpget", "-v2c", "-c", self.community, "-Oqv", self.host, oid]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def get_port_info(self, port):
        """get port status and speed"""
        info = {}
        info['status'] = self.get(f".1.3.6.1.2.1.2.2.1.8.{port}")
        info['speed'] = self.get(f".1.3.6.1.2.1.2.2.1.5.{port}")
        return info

    def get_cpu_utilization(self):
        """get CPU load as single string"""
        cpu_oids = {
            '5s': [
                ".1.3.6.1.4.1.171.12.1.1.6.1.0",
                ".1.3.6.1.4.1.171.10.76.29.1.100.1.1.0",
                ".1.3.6.1.4.1.171.10.76.37.1.100.1.1.0",
            ],
            '1m': [
                ".1.3.6.1.4.1.171.12.1.1.6.2.0",
                ".1.3.6.1.4.1.171.10.76.29.1.100.1.2.0",
                ".1.3.6.1.4.1.171.10.76.37.1.100.1.2.0",
            ],
            '5m': [
                ".1.3.6.1.4.1.171.12.1.1.6.3.0",
                ".1.3.6.1.4.1.171.10.76.29.1.100.1.3.0",
                ".1.3.6.1.4.1.171.10.76.37.1.100.1.3.0",
            ]
        }

        cpu_values = {}
        for period, oid_list in cpu_oids.items():
            for oid in oid_list:
                value = self.get(oid)
                if value and value.isdigit():
                    cpu_values[period] = value
                    break

        parts = []
        if '5s' in cpu_values:
            parts.append(f"{cpu_values['5s']}%")
        if '1m' in cpu_values:
            parts.append(f"{cpu_values['1m']}%")
        if '5m' in cpu_values:
            parts.append(f"{cpu_values['5m']}%")

        return " / ".join(parts) if parts else None
