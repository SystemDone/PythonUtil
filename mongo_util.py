from pymongo import MongoClient


class MongoUtil(object):

    def __init__(self, host, port=27017, username=None, password=None, database=None, authType='SCRAM-SHA-256'):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__authType = authType
        self.__client = MongoClient(host, port)
        self.__db = self.__client[database]
        if username is not None and password is not None:
            self.__db.authenticate(self.__username, self.__password, mechanism=self.__authType)

    def find(self, data, table):
        return self.__db[table].find(data)

    def insert(self, data, table):
        self.__db[table].insert(data)

    def update(self):
        pass

    def close(self):
        self.__client.close()




