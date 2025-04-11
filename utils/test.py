import pymysql

# 创建到本地MySQL数据库的连接
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bigdata')

def querylocaldb(sql, params, type='no_select'):
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        if type != 'no_select':
            data_list = cursor.fetchall()
            conn.commit()
            return data_list
        else:
            conn.commit()
            return '数据库查询成功'

# 使用修改后的函数查询本地数据库
data = querylocaldb('SELECT * FROM weibodata', [], 'select')
print(data[0])

# 关闭数据库连接
conn.close()
