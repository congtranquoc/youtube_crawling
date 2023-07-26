import logging

import mysql.connector

import utils


class MysqlManager:
    __instance = None

    @staticmethod
    def getInstance():
        if MysqlManager.__instance is None:
            MysqlManager.__instance = MysqlManager()
        return MysqlManager.__instance

    def __init__(self):
        if MysqlManager.__instance is not None:
            raise Exception("This class is a singleton!")
        # read file env.yaml and parse config
        self.env = utils.getEnv()
        self.query = self.env['mysql.query']
        # Lấy thông tin kết nối từ biến môi trường
        self.user = self.env['mysql.username']
        self.password = self.env['mysql.password']
        self.host = self.env['mysql.host']
        self.database = self.env['mysql.database']
        self.mysql_cnx = None
        self.mysql_cursor = None
        MysqlManager.__instance = self

    def is_connected(self):
        # Kiểm tra xem đã kết nối tới MySQL hay chưa
        if self.mysql_cnx:
            return self.mysql_cnx.is_connected()
        return False

    def connect(self):
        # Kiểm tra kết nối tới MySQL
        try:
            self.mysql_cnx = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                # database=self.database  # Thêm thông tin cơ sở dữ liệu vào kết nối
            )
            self.mysql_cursor = self.mysql_cnx.cursor()
        except mysql.connector.Error as err:
            print(f"Lỗi khi kết nối tới MySQL: {err}")
            # Thực hiện xử lý lỗi tại đây (ví dụ: ghi log, thông báo lỗi, vv.)
            logging.error(err)
            raise

    def close_mysql(self):
        if self.is_connected():
            # Đóng con trỏ và kết nối MySQL
            self.mysql_cursor.close()
            self.mysql_cnx.close()