import pymysql

from policy_crawl.config import mysql_table_name,mysql_database,mysql_ip,mysql_username,mysql_password
from policy_crawl.common.save.save_base import SaveBase


class MysqlSave(SaveBase):
    def __init__(self,ip=mysql_ip,database=mysql_database,table_name=mysql_table_name):
        self.db=pymysql.connect(ip,mysql_username,mysql_password,charset="utf-8",db=database)
        self.cursor=self.db.cursor()
        self.tb=table_name

    def save(self,data):
        #data为字典
        data=[(k,v) for k,v in data.items()]# 转为元组
        sql = 'insert %s (' % self.tb + ','.join(i[0] for i in data) + \
              ') values (' + ','.join('%r' % i[1] for i in data) + ');'
        self.cursor.execute(sql)
        self.db.commit()

    def __del__(self):
        self.cursor.close()
        self.tb.close()



