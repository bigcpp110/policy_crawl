import pymongo

from policy_crawl.config import mongodb_ip,mongodb_col,mongodb_db,mongodb_port
from policy_crawl.common.save.save_base import SaveBase


class MongodbSave(SaveBase):
    def __init__(self,ip=mongodb_ip,port=mongodb_port,db=mongodb_db,col=mongodb_col):
        self.client=pymongo.MongoClient(host=ip,port=port)
        self.db=self.client[db]
        self.col=self.db[col]

    def save(self,data):
        #data为字典
        self.col.insert_one(data)

    def __del__(self):
        self.client.close()


