    def get_port_info(self, port):
        info = {}
        info['status'] = self.get(f".1.3.6.1.2.1.2.2.1.8.{port}")
        info['speed'] = self.get(f".1.3.6.1.2.1.2.2.1.5.{port}")

        # скорость/дуплекс (то, что в Settings)
        speed_duplex = self.get(f".1.3.6.1.4.1.171.12.1.1.2.1.4.{port}")

        # ОТЛАДКА
        print(f"DEBUG speed_duplex raw: {repr(speed_duplex)}")

        # преобразуем в читаемый вид
        sd_map = {
            '1': '10M/Half',
            '2': '10M/Full',
            '3': '100M/Half',
            '4': '100M/Full',
            '5': '1000M/Half',
            '6': '1000M/Full',
        }
        info['settings'] = sd_map.get(speed_duplex, 'Auto')

        return info
