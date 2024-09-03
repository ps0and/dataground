import pandas as pd
import tensorflow as tf
import numpy as np
import joblib

# 저장된 모델 불러오기
new_model = tf.keras.models.load_model('./model/titanic_model.h5')

# 저장된 Scaler 불러오기
scaler = joblib.load('./model/titanic_scaler.pkl')

# 새로운 데이터 예시: Pclass=1, Gender='female', Age=30
new_data = pd.DataFrame({
    'Pclass': [1],
    'Gender': [1],  # 'female' is encoded as 0
    'Age': [30]
})

# 데이터 정규화 (scaler를 사용하여 동일하게 변환)
new_data_scaled = scaler.transform(new_data)

# 예측에 사용할 데이터 준비 (float32 타입으로 변환)
예측_data = np.array(new_data_scaled, dtype=np.float32)

# 예측
prediction = new_model.predict(예측_data)

# 결과 출력
predicted_survival = round(prediction[0][0] * 100, 2)
print(f"Predicted Survived: {predicted_survival}%")
