import pymysql


class MysqlUtil(object):

    def __init__(self, database):
        self._host = database['host']
        self._user = database['user']
        self._password = database['password']
        self._database = database['database']
        if database['charset'] is None:
            self._charset = 'utf8'
        else:
            self._charset = database['charset']
        self._tableName = ''
        self._SQL = ''
        self._query = ''
        self._queryNum = 0
        self._excute = None
        self._data = ''

    def teble(self, table):
        self._tableName = table
        return self

    def select(self):
        self._SQL = 'SELECT * FROM {table}'.format(table=self._tableName)
        self._excute = self.__select_excute
        return self

    def update(self, data):
        str_data = ['{0}=\'{1}\''.format(k, v) for k, v in data.items() if type(v) is str]
        other_data = ['{0}={1}'.format(k, v) for k, v in data.items() if type(v) is not str]
        self._data = ','.join(str_data + other_data)
        self._SQL = 'UPDATE {teble} SET {data}'.format(table=self._tableName, data=self._data)
        self._excute = self.__insert_excute

    def insert(self, data):
        if type(data) is dict:
            for k, v in data.items():
                if type(v) is str:
                    data[k] = '\'{0}\''.format(v)
                else:
                    data[k] = str(v)
            columns = ','.join(data.keys())
            values = ','.join(data.values())
            self._SQL = 'INSERT INTO {table}({columns}) VALUES({datas})'.format(table=self._tableName, columns=columns, datas=values)
        elif type(data) is list:
            for i in range(len(data)):
                if type(data[i]) is str:
                    data[i] = '\'{0}\''.format(data[i])
                else:
                    data[i] = str(data[i])
            values = ','.join(data)
            self._SQL = 'INSERT INTO {table} VALUES({data})'.format(table=self._tableName, data=values)
        self._SQL = self._SQL.replace('None', 'NULL')
        self._SQL = self._SQL.replace('False', 'false')
        self._SQL = self._SQL.replace('True', 'true')
        self._excute = self.__insert_excute
        return self

    def delete(self):
        pass

    def eq(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} = {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def ne(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} != {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def gt(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} > {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def lt(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} < {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def ge(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} >= {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def le(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} <= {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def le(self, column, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} <= {data}'.format(column=column, data=data)
        self._eqNum += 1
        return self

    def printSql(self):
        print(self._SQL)
        return self

    def excute(self):
        return self._excute()

    def __insert_excute(self):
        self.printSql()
        conn = pymysql.connect(host=self._host, user=self._user, password=self._password, database=self._database,
                               charset=self._charset)
        cursor = conn.cursor()
        num = cursor.execute(self._SQL)
        conn.commit()
        cursor.close()
        conn.close()
        self._SQL = ''
        return num

    def __select_excute(self):
        self.printSql()
        conn = pymysql.connect(host=self._host, user=self._user, password=self._password, database=self._database,
                               charset=self._charset)
        cursor = conn.cursor()
        cursor.execute(self._SQL)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        self._SQL = ''
        return results

database = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'test',
    'charset': 'utf8'
}

data = {
    'ID': '123',
    'CONTENT': '测试数据',
    'TYPE': '1',
    'REMARK': '这是备注',
    'DISABLED': 0
}

s = MysqlUtil(database).teble('userinfo').insert(data).excute()
s = MysqlUtil(database).teble('userinfo').select().eq('ID', '123').excute()
