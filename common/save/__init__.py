from policy_crawl.common.save import save_mongodb,save_mysql
from policy_crawl.config import save_db

DB={"mongodb":save_mongodb.MongodbSave,
    "mysql":save_mysql.MysqlSave}

def save(data,*args,**kwargs):
    for db in save_db:
        # try:
        DB[db](*args,**kwargs).save(data)
        # except:
        #     raise ValueError("no such method")