import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib



st.header('🎠 인공지능 놀이터')

st.subheader("모델을 선택하세요")
menu = st.selectbox('모델을 선택하세요', ['타이타닉 데이터', '당뇨병 데이터'], label_visibility='collapsed')

if menu == '타이타닉 데이터':
    # 저장된 모델 불러오기
    new_model = tf.keras.models.load_model('./model/titanic_model.h5')

    # 저장된 Scaler 불러오기
    scaler = joblib.load('./model/titanic_scaler.pkl')

    col1, col2, col3 = st.columns(3)
    나이 = col1.number_input('나이를 입력하세요.', value=30, step=1)
    객실등급 = col2.number_input('객실 등급을 입력하세요', value=2, step=1)
    성별 = col3.selectbox('성별을 선택하세요', ['male', 'female'])

    성별 = 1 if 성별 == 'male' else 0  # 성별을 숫자로 변환 (male: 1, female: 0)

    # 예측을 위한 입력 데이터 구성
    예측 = pd.DataFrame({
        'Pclass': [객실등급],
        'Gender': [성별],
        'Age': [나이]
    })

    # 입력 데이터를 모델이 기대하는 형태로 변환
    예측 = scaler.transform(예측)
    예측_np = np.array(예측, dtype=np.float32)
    
    # 모델 예측
    예측값 = new_model.predict(예측_np)
    
    생존확률 = 예측값[0][0] * 100  # 확률을 퍼센트로 변환
    생존확률 = round(생존확률, 2)  # 소수점 2자리까지 반올림
    문장 = f'당신의 생존확률은 :red[{생존확률}%]입니다.'
    st.header(문장)

elif menu == '당뇨병 데이터':
    new_model = tf.keras.models.load_model('./model/diabetes_model.h5')
    scaler = joblib.load('./model/diabetes_scaler.pkl')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    임신횟수 = col1.number_input('임신횟수를 입력하세요.', value=0, step=1)
    나이 = col2.number_input('나이를 입력하세요', value=20, step=1)
    키 = col3.number_input('키를 입력하세요', value=170, step=1)
    몸무게 = col4.number_input('몸무게를 입력하세요', value=60, step=1)
    혈압 = col5.number_input('혈압을 입력하세요', value=80, step=1)

    bmi = 몸무게 / (키 / 100) ** 2  # BMI 계산 (키를 미터 단위로 변환)

    예측 = pd.DataFrame({
        'Pregnancies': [임신횟수],
        'Age': [나이],
        'BMI': [bmi],
        'BloodPressure': [혈압]
    })

    # 모델 예측을 위해 numpy array로 변환
    예측 = scaler.transform(예측)
    예측_np = np.array(예측, dtype=np.float32)
    
    # 모델 예측
    예측값 = new_model.predict(예측_np)
    확률 = 예측값[0][0] * 100  # 확률을 퍼센트로 변환
    확률 = round(확률, 2)  # 소수점 2자리까지 반올림
    문장 = f'당뇨병 위험 지수는 :red[{확률}%]입니다.'
    st.header(문장)
