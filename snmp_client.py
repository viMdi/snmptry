import subprocess

class SnmpSession:
		def __init__(self, host, community, version=2):
				self.host = host
				self.community = community
				self.version = version

		def get(self, oid):
				"""get single value by OID using snmpget"""
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
				info['in_errors'] = self.get(f".1.3.6.1.2.1.2.2.1.14.{port}")
				info['out_errors'] = self.get(f".1.3.6.1.2.1.2.2.1.20.{port}")
				return info

		def get_port_errors_detailed(self, port):
				"""get detailed error counters for port"""
				errors = {}
				errors['crc'] = self.get(f".1.3.6.1.2.1.16.1.1.1.8.{port}")
				errors['undersize'] = self.get(f".1.3.6.1.2.1.16.1.1.1.9.{port}")
				errors['oversize'] = self.get(f".1.3.6.1.2.1.16.1.1.1.10.{port}")
				errors['fragment'] = self.get(f".1.3.6.1.2.1.16.1.1.1.11.{port}")
				errors['jabber'] = self.get(f".1.3.6.1.2.1.16.1.1.1.12.{port}")
				errors['drop'] = self.get(f".1.3.6.1.2.1.16.1.1.1.3.{port}")
				return errors

		def get_dhcp_relay_state(self):
				"""get DHCP relay status (enabled/disabled)"""
				state = self.get(".1.3.6.1.4.1.171.12.42.1.1")
				if state == "1":
						return "Enabled"
				elif state == "2":
						return "Disabled"
				return None

		def get_cpu_utilization(self):
				"""get CPU load as single string"""
				cpu_oids = {
						'5s': [
								".1.3.6.1.4.1.171.12.1.1.6.1.0",  # DES-3028, DGS-3000, DGS-3120
						],
						'1m': [
								".1.3.6.1.4.1.171.12.1.1.6.2.0",
						],
						'5m': [
								".1.3.6.1.4.1.171.12.1.1.6.3.0",
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
