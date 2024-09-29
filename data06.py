import streamlit as st
import pandas as pd
#데이터 가져오기

st.header("🎈결측치 처리")
st.divider()
df = pd.DataFrame({
    '이름': ['지민', '사나', '태연', '민호', '제니'],
    '나이': [28, 22, None, 35, 30],
    '키': [173, None, 160, 182, 163],
    '점수': [85, 90, 78, None, 95]
})

df_drop = df.copy()
df_value = df.copy()
df_mean = df.copy()
df_median = df.copy()
st.subheader("데이터 확인하기")
st.write(df)
st.subheader("결측치 처리하기")
c1, c3, c4 = st.columns(3)

c1.write("1. 결측 데이터 제거")
df_drop.dropna(inplace=True)
c1.code("df_drop.dropna(inplace=True)")
c1.write(df_drop)


c3.write("3. 평균값으로 대체")

df_mean['나이'].fillna(df_mean['나이'].mean(), inplace=True)
c3.code("""
df_mean = df
mean = df_mean['나이'].mean()
df_mean.['나이'].fillna(mean, inplace=True)""", language='python')
c3.write(df_mean)


c4.write("4. 중앙값으로 대체")
df_median['나이'].fillna(df_median['나이'].median(), inplace=True)
c4.code("""
df_mean = df
median = df_mean['나이'].median()
df_mean.['나이'].fillna(median, inplace=True)""", language='python')
c4.write(df_median)


st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("data05.py")

if next_btn:
    st.switch_page("analysis01.py")
