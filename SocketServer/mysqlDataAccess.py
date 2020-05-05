import pymysql 

MYSQL_HOST = 'localhost'
MYSQL_DB = 'covid19'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = 3306


class MysqlDataAccess:
    def __init__(self,host = MYSQL_HOST,database=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWORD,port=MYSQL_PORT):
        try:
            self.db = pymysql.connect(host,user,password,database,charset='utf8',port=port)
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        except  pymysql.MySQLError as e :
            print(e.args)

    def updateCountryPosition(self,name,lng,lat,type):
        sql_update = 'insert into dic_lnglat (name,lng,lat,type) values(%s,%s,%s,%s) on duplicate key update'
        sql_update += ' name= %s,lng=%s,lat=%s,type=%s'
        try:
            self.cursor.execute(sql_update,(name,lng,lat,type) * 2)
            self.db.commit()
            print(name)
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()

    def getData(self):
        sql_query = 'SELECT a.name,b.lng,b.lat,IFNULL(a.new,0) as new,IFNULL(a.now,0) as now,IFNULL(a.total,0) as total,IFNULL(a.cure,0) as cure,IFNULL(a.death,0) as death from covid19  a inner join dic_lnglat b on a.`name`=b.`name`'
        try:
            self.cursor.execute(sql_query)
            return self.sql_fetch_json()
        except pymysql.MySQLError as e:
            print(e.args)

    def getOverviewData(self):
        sql_query ='select SUM(IFNULL(new,0)) as new , SUM(now) as now,SUM(total) as total,SUM(cure) as cure,SUM(death) as death,MIN(time) as time from covid19 where parent = "全球"'
        try:
            self.cursor.execute(sql_query)
            return self.sql_fetch_json()
        except pymysql.MySQLError as e:
            print(e.args)

    def getRankData(self):
        sql_query = 'select *  from covid19 where parent in ("国内","海外")  order by  CAST(new AS UNSIGNED) DESC LIMIT 3 '
        try:
            self.cursor.execute(sql_query)
            return self.sql_fetch_json()
        except pymysql.MySQLError as e:
            print(e.args)

    def sql_fetch_json(self):
        keys = []
        for column in self.cursor.description:
            keys.append(column[0])
        key_number = len(keys)

        json_data = []
        for row in self.cursor.fetchall():
            item = dict()
            for q in range(key_number):
                item[keys[q]] = row[keys[q]]
            json_data.append(item)

        return json_data


