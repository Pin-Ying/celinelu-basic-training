import pymysql


class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(100),
            date DATE,
            url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_post(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        values = tuple(kwargs.values())

        sql = f"INSERT INTO posts ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
