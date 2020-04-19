from mysqlDataAccess import MysqlDataAccess
import json

def test():
    access = MysqlDataAccess()
    results = access.getData()
    print(results)


test()