import pymysql.cursors

def get_conn():
    conn = pymysql.connect(host='172.17.0.1', port=53306, user='mnist', password='1234', db='mnistdb', cursorclass=pymysql.cursors.DictCursor)
    
    return conn 

def select(query:str,size = -1):
    conn = get_conn()
    # DB 연결 SELECT ALL
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchmany(size)

    return result


def dml(sql, *values):
    conn = get_conn()

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount
