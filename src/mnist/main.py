from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import pymysql.cursors
from datetime import datetime 
from pytz import timezone

app = FastAPI()



@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장 (async, await 비동기 키워드:파일은 즉시 업로드하는게 불가능하기 떄문에)
    img = await file.read()
    file_name  = file.filename
    file_ext = file.content_type.split('/')[-1] 
    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "/home/centa/code/mnist/img"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    import uuid 
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')
    
    with open(file_full_path, "wb") as f:
        f.write(img)
        
    # 파일 저장 경로 DB INSERT
    conn = pymysql.connect(host='172.17.0.1', port=53306, user='mnist', password='1234', db='mnistdb', charset='utf8')
    cur =  conn.cursor(pymysql.cursors.DictCursor)
    # tablename : image_processing
    # 컬럼 정보 : num(초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자(n00)
    query = """
    INSERT INTO image_processing(file_name, file_path,request_time,request_user) VALUES (%s,%s,%s,%s)
    """
    from jigeum.seoul import now
    from mnist.db import dml
    insert_row = dml(query, file_name, file_full_path, now(), 'n05')
    
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트) 

    return {
            "filename": file.filename,   
            "content_type": file.content_type,
            "file_full_path" : file_full_path,
            "insert_row" : insert_row
           }

@app.get("/all")
def all():
    from mnist.db import select  
    # DB 연결 SELECT ALL
    sql = "SELECT * FROM image_processing where num>6" 
    result = select(query=sql, size=-1)
    # 결과값 리턴 
    return result

@app.get("/one")
def one():
    # DB 연결 SELECT  값 중 하나만 리턴 
    from mnist.db import select 
    sql = "SELECT * FROM image_processing where num>6"
    result = select(query=sql,size=1)
    # 결과값 리턴 
    return result

@app.get("/many/{size}")
def many(size:int):
    # DB 연결 SELECT  값 중 하나만 리턴
    from mnist.db import select
    sql = "SELECT * FROM image_processing where num>6"
    result = select(query=sql,size=size)
    # 결과값 리턴
    return result
