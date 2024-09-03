import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# 데이터 로드 (당뇨병 데이터셋)
df = pd.read_csv('./data/당뇨병(kaggle).csv')

# 필요한 열만 선택
df = df[['Pregnancies', 'Age', 'BMI', 'BloodPressure', 'Outcome']]

# 입력(X)과 출력(y) 데이터 분리
X = df.drop('Outcome', axis=1)  # 'Outcome' 열을 예측 대상(y)으로 설정
y = df['Outcome']

# 학습용과 테스트용 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 데이터 정규화
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Scaler 저장
joblib.dump(scaler, './model/scaler.pkl')

# 모델 정의
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 모델 구조 확인
model.summary()

# 모델 학습
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

# 모델 평가
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy:.2f}')

# 모델 저장
model.save('./model/diabetes_model.h5')
