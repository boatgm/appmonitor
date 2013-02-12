import pymongo
from crawler.settings import MONGODB
class mongo():
    db = None
    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.db = pymongo.Connection(MONGODB['host'],MONGODB['port'])[MONGODB['name']]
        return cls.db
