import pymysql


class MysqlUtil(object):

    def __init__(self, database):
        # 地址
        self._host = database['host']
        # 账号
        self._user = database['user']
        # 密码
        self._password = database['password']
        # 数据库
        self._database = database['database']
        # 默认编码utf-8
        if database['charset'] is None:
            self._charset = 'utf8'
        else:
            self._charset = database['charset']
        # 表名
        self._tableName = ''
        # SQL主体
        self._SQL = ''
        # where条件部分
        self._query = ''
        # 条件计数，为零时拼接条件前加where关键字，大于零时条件前加and关键字
        self._queryNum = 0
        # 暂存执行语句方法
        self._excute = None
        # 参数
        self._data = ''
        # 字段名
        self._column = ''

    '''
    功能：暂存表名
    参数：表名
    '''
    def teble(self, table):
        self._tableName = table
        return self

    '''
    功能：拼接select语句
    '''
    def select(self):
        # 拼接sql
        self._SQL = 'SELECT * FROM {table}'
        # 暂存执行方法
        self._excute = self.__select_excute
        return self

    '''
    功能：拼接update语句
    参数：
        dict类型，key为字段名，value为值
    '''
    def update(self, data):
        # 过滤str类型字段，值添加单引号，拼接sql
        str_data = ['{0}=\'{1}\''.format(k, v) for k, v in data.items() if type(v) is str]
        # 过滤非str类型字段，拼接sql
        other_data = ['{0}={1}'.format(k, v) for k, v in data.items() if type(v) is not str]
        self._data = ','.join(str_data + other_data)
        print(self._data)
        # 拼接sql
        self._SQL = 'UPDATE {table} SET ' + self._data
        # 暂存执行方法
        self._excute = self.__insert_excute
        return self

    '''
    功能：拼接insert语句
    参数：
        1.为dict类型时，根据键值对拼接字段与values中的值，可以少插入字段，key为字段名，value为值
        2.为list类型时，必须包含所有列的值
    '''
    def insert(self, data):
        if type(data) is dict:
            # dict类型时
            for k, v in data.items():
                if type(v) is str:
                    # 值添加单引号
                    data[k] = '\'{0}\''.format(v)
                else:
                    # 转为str类型
                    data[k] = str(v)
            # 拼接逗号
            self._column = ','.join(data.keys())
            self._data = ','.join(data.values())
            # 拼接sql
            self._SQL = 'INSERT INTO {table}'
            self._query ='({column}) VALUES({data})'.format(column=self._column, data=self._data)
        elif type(data) is list:
            # list类型时
            for i in range(len(data)):
                if type(data[i]) is str:
                    data[i] = '\'{0}\''.format(data[i])
                else:
                    data[i] = str(data[i])
            self._data = ','.join(data)
            self._SQL = 'INSERT INTO {table}'
            self._query = ' VALUES({data})'.format(data=self._data)
        self._excute = self.__insert_excute
        return self

    '''
    功能：拼接delete语句
    '''
    def delete(self):
        self._SQL = 'DELETE FROM {table}'
        self._excute = self.__insert_excute
        return self

    '''
    功能：调用拼接条件的方法，传入运算符=
    参数：
        column：字段名
        data：值
    '''
    def eq(self, column, data):
        return self.__compare_query(column, '=', data)

    '''
    功能：调用拼接条件的方法，传入运算符!=
    参数：
        column：字段名
        data：值
    '''
    def ne(self, column, data):
        return self.__compare_query(column, '!=', data)

    '''
    功能：调用拼接条件的方法，传入运算符>
    参数：
        column：字段名
        data：值
    '''
    def gt(self, column, data):
        return self.__compare_query(column, '>', data)

    '''
    功能：调用拼接条件的方法，传入运算符<
    参数：
        column：字段名
        data：值
    '''
    def lt(self, column, data):
        return self.__compare_query(column, '<', data)

    '''
    功能：调用拼接条件的方法，传入运算符>=
    参数：
        column：字段名
        data：值
    '''
    def ge(self, column, data):
        return self.__compare_query(column, '>=', data)

    '''
    功能：调用拼接条件的方法，传入运算符<=
    参数：
        column：字段名
        data：值
    '''
    def le(self, column, data):
        return self.__compare_query(column, '<=', data)

    '''
    功能：拼接IN条件
    参数：
        column：字段名
        data：list类型
    '''
    def In(self, column, data):
        return self.__In(column, 'IN', data)

    '''
    功能：拼接NOT IN条件
    参数：
        column：字段名
        data：list类型
    '''
    def notIn(self, column, data):
        return self.__In(column, 'NOT IN', data)

    '''
    功能：拼接OR条件
    '''
    def Or(self, data):
        calculate = {
            'eq': '=',
            'gt': '>',
            'lt': '<',
            'ne': '!=',
            'ge': '>=',
            'le': '<=',
            'in': 'IN',
            'notin': 'NOT IN'
        }
        datas = []
        for item in data:
            if type(item['data']) is str:
                item['data'] = '\'{0}\''.format(item['data'])
            elif type(item['data']) is list:
                item['data'] = str(item['data']).replace('[', "(").replace(']', ')')
            else:
                item['data'] = str(item['data'])
            datas.append('{column} {calculate} {data}'.format(column=item['column'], data=item['data'], calculate=calculate[item['calculate'].lower()]))
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' ({data})'.format(data=' OR '.join(datas))
        return self

    '''
    功能：可以通过这个方法执行自己编写的sql
    '''
    def setSQL(self, sql):
        self._SQL = sql

    '''
    功能：打印SQL
    返回值：sql
    '''
    def printSql(self):
        # 打印SQL
        print(self._SQL)
        return self._SQL

    '''
    功能：拼接table，调用执行sql的方法，重置内部数据
    返回值：SQL运行结果
    '''
    def excute(self):
        if self._tableName != '':
            # 拼接表名
            self._SQL = (self._SQL + self._query).format(table=self._tableName)
        # 修改python与MySQL不同的类型
        self._SQL = self._SQL.replace('None', 'NULL')
        self._SQL = self._SQL.replace('False', 'false')
        self._SQL = self._SQL.replace('True', 'true')
        # 打印SQL
        self.printSql()
        # 执行SQL，inster或update或delete返回影响行数，select返回查询到的数据集合
        obj = self._excute()
        # 重置内部数据
        self._tableName = ''
        self._SQL = ''
        self._query = ''
        self._queryNum = 0
        self._excute = None
        self._data = ''
        self._column = ''
        # 返回执行结果
        return obj

    def __In(self, column, calculate, data):
        # str_data = ['\'{0}\''.format(x) for x in data if type(x) is str]
        # other_data = [str(x) for x in data if type(x) is not str]
        # data = '({data})'.format(data=','.join(str_data + other_data))
        data = str(data).replace('[', '(').replace(']', ')')
        return self.__query(column, calculate, data)

    '''
    功能：封装比较运算条件的参数
    参数：
        column：字段名
        calculate：运算符
        data：值
    '''
    def __compare_query(self, column, calculate, data):
        if type(data) is str:
            data = '\'{0}\''.format(data)
        return self.__query(column, calculate, data)

    '''
    功能：拼接查询条件
    参数：
        column：字段名
        calculate：运算符
        data：值
    '''
    def __query(self, column, calculate, data):
        if 0 == self._queryNum:
            self._query = ' WHERE'
        else:
            self._query += ' AND'
        self._query += ' {column} {calculate} {data}'.format(column=column, data=data, calculate=calculate)
        self._queryNum += 1
        return self

    '''
    功能：执行insert或update或delete语句
    返回值：SQL运行影响的行数
    '''
    def __insert_excute(self):
        # 连接数据库
        conn = pymysql.connect(host=self._host, user=self._user, password=self._password, database=self._database,
                               charset=self._charset)
        # 获取光标
        cursor = conn.cursor()
        # 执行SQL语句
        num = cursor.execute(self._SQL)
        # 提交
        conn.commit()
        # 关闭光标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return num

    '''
    功能：执行select语句
    返回值：SQL查询到的内容
    '''
    def __select_excute(self):
        # 连接数据库
        conn = pymysql.connect(host=self._host, user=self._user, password=self._password, database=self._database,
                               charset=self._charset)
        # 获取光标
        cursor = conn.cursor()
        # 执行SQL语句
        cursor.execute(self._SQL)
        # 获取全部返回值
        results = cursor.fetchall()
        # 关闭光标
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return results

# 示例
# database = {
#     'host': '127.0.0.1',
#     'user': 'root',
#     'password': '123456',
#     'database': 'test',
#     'charset': 'utf8'
# }
# data = {
#     'ID': '123',
#     'CONTENT': '测试数据',
#     'TYPE': '1',
#     'REMARK': '这是备注',
#     'DISABLED': 0
# }
# s = MysqlUtil(database).teble('userinfo').insert(data).excute()
# s = MysqlUtil(database).teble('userinfo').select().ne('ID', '123').In('TYPE', ['1', '2', '3']).notIn('TYPE', ['1', '2', '3']).excute()
# d = [{'column': 'TYPE', 'data': '1', 'calculate': 'eq'}, {'column': 'TYPE', 'data': ['1', '2'], 'calculate': 'in'}]
# s = MysqlUtil(database).teble('userinfo').select().ne('ID', '123').In('TYPE', [False, 2, '3']).Or(d).excute()
# s = MysqlUtil(database).teble('userinfo').update(data).excute()
