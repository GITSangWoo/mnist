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
    time = datetime.now(timezone('Asia/Seoul'))
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    # 파일 저장 (async, await 비동기 키워드:파일은 즉시 업로드하는게 불가능하기 떄문에)
    img = await file.read()
    file_name  = file.filename
    upload_dir = "./photo"
    file_full_path = os.path.join(upload_dir, file_name)
    os.makedirs(upload_dir,exist_ok=True)
    
    with open(file_full_path, "wb") as f:
        f.write(img)
        
    # 파일 저장 경로 DB INSERT
    conn = pymysql.connect(host='172.17.0.1', port=13306, user='food', password='1234', db='fooddb', charset='utf8')
    cur =  conn.cursor(pymysql.cursors.DictCursor)
    # tablename : image_processing
    # 컬럼 정보 : num(초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자(n00)
    query = """
    INSERT INTO image_processing(file_name, file_path,request_time,request_user) VALUES (%s,%s,%s,%s)
    """
    cur.execute(query,(file_name,file_full_path,time,"n05"))
    conn.commit()

    
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트) 

    return {
            "filename": file.filename,   
            "content_type": file.content_type,
            "file_full_path" : file_full_path
           }
