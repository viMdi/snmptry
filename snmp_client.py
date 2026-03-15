import subprocess
import re

class SnmpSession:
    def __init__(self, host, community, version=2):
        self.host = host
        self.community = community
        self.version = version

    def get(self, oid):
        """получить одно значение по OID через snmpget"""
        try:
            cmd = ["snmpget", "-v2c", "-c", self.community, "-Oqv", self.host, oid]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)

            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None

    def walk(self, oid):
        """получить все значения по OID через snmpwalk"""
        try:
            cmd = ["snmpwalk", "-v2c", "-c", self.community, "-Oqv", self.host, oid]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                return [line.strip() for line in result.stdout.splitlines() if line.strip()]
            return []
        except:
            return []

    def get_port_status(self, port):
        oid = f".1.3.6.1.2.1.2.2.1.8.{port}"
        return self.get(oid)

    def get_port_mac(self, port):
        oid = ".1.3.6.1.4.1.171.11.63.11.2.25.2.1.1.3"
        return self.walk(oid)
