import jigeum.seoul
import os 
import numpy as np
from PIL import Image
from keras.models import load_model


def get_model_path():
    # import os ...
    # 이 함수 파일의 절대 경로를 받아온다
    f= __file__
    # 절대 경로를 이용해 model.pkl의 경로를 조합
    dir_name=os.path.dirname(f)
    file_path=os.path.join(dir_name, "mnist240924.keras")
    return file_path

def run():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 가져오기
    from mnist.db import select,dml 
    sql= "SELECT num FROM image_processing WHERE prediction_result IS NULL ORDER BY num LIMIT 1"
    result = select(query=sql,size=1)
    if result == ():
        print(f"작업 요청 시간:{jigeum.seoul.now()}:predict_result=null인 값이 없습니다.")
        return True
    # STEP 2
    # 모델로 예측한 값을  prediction_result 컬럼에 업데이트
    # 모델 로드
    model_path=get_model_path()
    model = load_model(model_path) 
    # 사용자 이미지 불러오기 및 전처리
    def preprocess_image(image_path):
        img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
        img = img.resize((28, 28))  # 크기 조정

        # 흑백 반전
        img = 255 - np.array(img)  # 흑백 반전
    
        img = np.array(img)
        img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
        img = img / 255.0  # 정규화
        return img

    def predict_digit(image_path):
        img = preprocess_image(image_path)
        prediction = model.predict(img)
        digit = np.argmax(prediction)
        return digit
    
    # 사용자 이미지 경로
    from mnist.db import select,dml
    sql= "SELECT file_path FROM image_processing WHERE prediction_result IS NULL ORDER BY num LIMIT 1"
    extract_path = select(query=sql,size=1)
    print(extract_path)
    image_path= extract_path[0]['file_path']

    # 예측 실행
    predicted_digit = predict_digit(image_path)
    print("예측된 숫자:", predicted_digit)
    
    # 동시에 prediction_model, prediction_time 도 업데이트
    sql= "UPDATE image_processing SET prediction_result=%s,prediction_model= %s,prediction_time=%s WHERE num = %s"
    insert_row=dml(sql,predicted_digit,os.path.basename(model_path),jigeum.seoul.now(),result[0]['num'])

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
    
