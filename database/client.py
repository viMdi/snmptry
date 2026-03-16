import pymysql.cursors

class DatabaseClient:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                db=self.config["database"],
                charset=self.config["charset"],
                cursorclass=pymysql.cursors.DictCursor,
            )
            return True
        except pymysql.Error as e:
            print(f"Ошибка подключения к БД: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()

    def get_user_by_number(self, number):
        results = []
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT SwitchP, PortP FROM users WHERE number = %s"
                cursor.execute(sql, (number,))
                rows = cursor.fetchall()

                for row in rows:
                    user_data = {
                        "switch": row.get("SwitchP") or "",
                        "port": row.get("PortP") or "",
                    }
                    results.append(user_data)
        except pymysql.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
        return results
