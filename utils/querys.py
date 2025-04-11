import pymysql

def querylocaldb(sql, params=None, type='no_select'):
    # 确保在此处创建和关闭数据库连接
    conn = None
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='bigdata')
        with conn.cursor() as cursor:
            cursor.execute(sql, params if params is not None else ())
            if type == 'select':
                data_list = cursor.fetchall()
                return data_list
            else:
                conn.commit()
                return '数据库操作成功'
    except pymysql.MySQLError as e:
        print(f"数据库操作出错: {e}")
        return None
    finally:
        if conn:
            conn.close()

# 使用修改后的函数查询本地数据库
# data = querylocaldb('SELECT * FROM weibodata', [], 'select')
# if data:
#     print(data[0])

