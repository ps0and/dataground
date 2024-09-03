import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

# 저장된 모델 불러오기
new_model = tf.keras.models.load_model('./model/diabetes_model.h5')

# Scaler 불러오기 (학습 시 사용한 Scaler를 저장한 경우)
scaler = joblib.load('./model/diabetes_scaler.pkl')

# 새로운 데이터 예시
new_data = pd.DataFrame({
    'Pregnancies': [2],
    'Age': [25],
    'BMI': [30.0],
    'BloodPressure': [70]
})

# 데이터 정규화 (scaler를 사용하여 동일하게 변환)
new_data_scaled = scaler.transform(new_data)

# 예측에 사용할 데이터 준비 (float32 타입으로 변환)
예측_data = np.array(new_data_scaled, dtype=np.float32)

# 예측
prediction = new_model.predict(예측_data)

# 결과 출력
predicted_probability = round(prediction[0][0] * 100, 2)
print(f"Predicted Diabetes Probability: {predicted_probability}%")
