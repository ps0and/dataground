import streamlit as st
import pandas as pd
import io


st.header("🔧 데이터프레임 확인하기")
st.divider()
st.write("csv파일로 불러온 데이터는 pandas의 DataFrame 형식으로 저장된다.")
st.write("각각의 데이터가 어떤 자료형으로 저장되었는지? 데이터의 개수는 몇개인지 확인하는 과정이 필요하다.")
df = pd.read_csv('./data/축구선수(kaggle).csv')

st.subheader("코드")
st.code("df.info()", language='python')

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
st.code("df.columns", language='python')

st.subheader("실행결과")
st.write(df.columns)


st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("data01.py")

if next_btn:
    st.switch_page("data03.py")
