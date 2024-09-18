import streamlit as st
import pandas as pd

st.header("상관관계")
st.write("**상관관계** 분석은 두 컬럼 간의 관계를 파악하여 하나의 변수 값이 증가할 때 다른 변수 값이 어떻게 변하는지 이해하기 위해 사용한다.")

st.subheader("상관계수")
st.write("상관계수는 두 컬럼 간의 선형관계를 나타내며 값은 -1에서 1사이이다. 1에 가까울수록 강한 양의 상관관계, -1에 가까울수록 강한 음의 상관관계를 나타낸다. 0에 가까울수록 상관이 없다는 것을 의미한다.")




df = pd.read_csv('./data/축구선수(kaggle).csv')
df = df[['value_eur','age','overall','shooting','defending','passing','dribbling','physic']]
df = df.dropna()
st.write("축구선수 능력치 데이터")
st.write(df)


st.subheader("특정 컬럼의 상관관계 확인하기")
c1, c2 = st.columns(2)


c1.write("연봉과 나이")
c1.code("df[['value_eur','age']].corr()")
c1.write(df[['value_eur','age']].corr())
c2.write("연봉과 슈팅능력")
c2.code("df[['value_eur','overall']].corr()")
c2.write(df[['value_eur','overall']].corr())


st.write("가치(value_eur)와 나이(age)를 분석한 결과 상관계수 0.0479로 가치와 나이는 상관관계가 매우 적고 가치와 종합능력치(overall)는 비교적 높은 상관관계를 갖고 있다.")

st.subheader("데이터프레임의 상관관계 확인하기")
st.write(df.corr())
st.write("가치(value_eur)의 상관관계를 확인한 결과 나이(age)의 상관계수가 0.0479으로 가장 낮고 종합능력치(overall)이 0.5643으로 가장 높은 양의 상관관계를 보였다.")

st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("analysis02.py")

if next_btn:
    st.switch_page("graph01.py")