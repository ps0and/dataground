import streamlit as st
import pandas as pd
import io


st.header("🔧 데이터프레임 확인하기")

df = pd.read_csv('./data/축구선수(kaggle).csv')

st.subheader("코드")
st.code("df.info()")

st.subheader("실행결과")

st.write("<class 'pandas.core.frame.DataFrame'>")
st.write("RangeIndex: 19239 entries, 0 to 19238")
st.write("Columns: 110 entries, sofifa_id to nation_flag_url")
st.write("dtypes: float64(16), int64(44), object(50)")
st.write("memory usage: 16.1+ MB")



st.write("행 19,239개, 열 110개로 이뤄진 데이터 프레임")
st.write("110개의 열은 실수 16개, 정수 44개, 문자 50개로 이뤄져있다.")

st.divider()
st.header("🎉 컬럼명 확인하기")

st.subheader("코드")
st.code("df.columns")

st.subheader("실행결과")
st.write(df.columns)