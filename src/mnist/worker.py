import jigeum.seoul
import os 

def run():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 가져오기
    from mnist.db import select,dml 
    sql= "SELECT num FROM image_processing where prediction_result IS NULL"
    result = select(query=sql,size=1)
    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    import random
    rnum= random.randint(0,9) 
    sql= "UPDATE image_processing SET prediction_result=%s WHERE num = %s"
    insert_row=dml(sql,rnum,result[0]['num'])
    # 업데이트 확인용 
    # 동시에 prediction_model, prediction_time 도 업데이트
    sql= "UPDATE image_processing SET prediction_model= %s,prediction_time=%s WHERE num = %s"
    insert_row=dml(sql,f"model{rnum}.pkl",jigeum.seoul.now(),result[0]['num'])

    # STEP 3
    # LINE 으로 처리 결과 전송
    import requests   
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_API_KEY','false')

    headers = {'Authorization':'Bearer '+token}

    message = {
       "message" : f"{jigeum.seoul.now()}:task done successful"
    }

    requests.post(api_url, headers= headers , data = message)

    print(f"작업 요청 시간:{jigeum.seoul.now()}")
