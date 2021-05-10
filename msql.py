import pymysql.cursors

db = pymysql.connect(host="localhost",user='root', password='pass', database='world', cursorclass=pymysql.cursors.DictCursor)
with db.cursor() as cursor:
        sql = "SELECT * FROM `world`.`city` LIMIT 0,10"
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)