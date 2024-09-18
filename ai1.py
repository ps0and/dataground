import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 예시 데이터 (공부 시간에 따른 성적)
df = pd.read_csv("./data/와인품질데이터(kaggle).csv")

st.header("회귀분석")
st.subheader("회귀분석을 이용한 와인품질 예측")

st.write("와인품질데이터")
st.write(df.head())

#Target 분리
st.write("1. 예측할 값 정하기")
st.write("데이터프레임에서 예측할 열을 선정하고 데이터프레임에서 분리한다.")
st.code("""#예측할 값(quality)을 제거하고 X에 저장.
X = df.drop('quality', axis=1)
#예측할 값(quality)을 y로 저장.
y = df['quality']""", language="python")

X = df.drop('quality', axis=1)  # All features except the target 'quality'
y = df['quality']  # Target is 'quality'

c1, c2 = st.columns([1,3])
c1.write("예측할 값(y)")
c1.write(y.head())

c2.write("입력 데이터(X)")
c2.write(X.head())


st.write("2. 평가를 위한 데이터 분리")
st.write("전체 데이터에서 80%는 학습에 활용하고 20%는 학습된 모델을 평가하기 위해 분리한다.")
# Train-test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
st.code("""X_train, X_test, y_train, y_test = train_test_split(
                                    X, 
                                    y, 
                                    test_size=0.2, 
                                    random_state=42)""", language='python')

st.write("모델 제작 및 fit")
st.write("선형회귀(LinearRegression)모델을 적용하시기 위해 데이터 셋을 알맞게 변환한다.")
# Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)
st.code("""
model = LinearRegression()
model.fit(X_train, y_train)""")


st.write("예측하기")
# Predictions on the test set
y_pred = model.predict(X_test)
st.code("y_pred = model.predict(X_test)", language='python')

st.write("평가하기")
# Model evaluation
st.code("""
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)""", language='python')
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Display results
st.write(f"평균 제곱 오차: {mse:.2f}")
st.write(f"평균 제곱근 편차: {rmse:.2f}")
st.write(f"결정계수: {r2:.2f}")

# Show some predictions vs actual
comparison_df = pd.DataFrame({'와인 품질': y_test, '예측한 와인 품질': y_pred})
st.write(comparison_df)

