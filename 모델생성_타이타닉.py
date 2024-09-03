import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# 데이터 로드
df = pd.read_csv('./data/타이타닉(kaggle).csv')

# 필요한 열만 선택
df = df[['Survived', 'Pclass', 'Gender', 'Age']]

# 결측치 처리 (Age의 결측치를 평균으로 대체)
df['Age'].fillna(df['Age'].mean(), inplace=True)

# 범주형 데이터 인코딩
df['Gender'] = LabelEncoder().fit_transform(df['Gender'])  # 'male': 1, 'female': 0

# 입력(X)과 출력(y) 데이터 분리
X = df.drop('Survived', axis=1)
y = df['Survived']

# 학습용과 테스트용 데이터로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 데이터 정규화
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Scaler 저장
joblib.dump(scaler, './model/titanic_scaler.pkl')

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
loss, accuracy = model
