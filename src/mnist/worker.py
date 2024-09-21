import jigeum.seoul

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
    sql= "UPDATE  image_processing SET prediction_result=%s WHERE num = %s"
    insert_row=dml(sql,rnum,result[0]['num'])
    # 업데이트 확인용 
    # 동시에 prediction_model, prediction_time 도 업데이트

    # STEP 3
    # LINE 으로 처리 결과 전송

    print(f"작업 요청 시간:{jigeum.seoul.now()}, 작업한 행: {insert_row}")
