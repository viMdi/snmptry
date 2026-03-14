from easysnmp import Session

class SnmpSession:
		def __init__(self, host, community, version=2):
				self.session = Session(hostname=host, community=community, version=version)

		def get(self, oid):
				try:
						# получаем значение напрямую
						return self.session.get(oid).value
				except Exception as e:
						print(f"SNMP error: {e}")
						return None

		def walk(self, oid):
				try:
						return [item.value for item in self.session.walk(oid)]
				except Exception as e:
						print(f"SNMP walk error: {e}")
						return []

		def get_port_status(self, port):
				"""статус порта (1-up, 2-down)"""
				oid = f".1.3.6.1.2.1.2.2.1.8.{port}"
				return self.get(oid)

		def get_port_mac(self, port):
				"""MAC-адреса на порту (альтернативный OID)"""
				# сначала пробуем стандартный
				oid1 = f".1.3.6.1.2.1.17.4.3.1.2.{port}"
				macs = self.walk(oid1)
				if macs:
						return macs

				# если нет, пробуем другой
				oid2 = ".1.3.6.1.4.1.171.11.63.11.2.25.2.1.1"
				all_macs = self.walk(oid2)

				# фильтруем по порту
				port_macs = []
				for i in range(0, len(all_macs), 2):
						if i+1 < len(all_macs) and all_macs[i+1] == str(port):
								port_macs.append(all_macs[i])

				return port_macs
