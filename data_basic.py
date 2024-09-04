import streamlit as st
import pandas as pd

#페이지 제목
st.header("🎬 제목")
st.divider()

#데이터 가져오기
df = pd.read_csv('./data/축구선수(kaggle).csv')

#코드
st.subheader("코드")

#실행결과
st.subheader("실행결과")

st.divider()
#해보기
st.header('해보기')

#실행결과 출력
st.subheader("실행결과 출력")
