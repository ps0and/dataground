import streamlit as st
import pandas as pd



st.header('🔧 데이터 전처리 체험하기')
st.subheader("0. 데이터 가져오기")
st.code("""import pandas as pd
df = pd.read_csv('데이터.csv')""", language='python')
df = pd.read_csv('./data/축구선수(kaggle).csv')
st.divider()
st.subheader("1. 데이터 확인")
st.write('csv파일을 데이터프레임으로 잘 가져왔는지, 오류는 없는지 일부 데이터를 확인한다.')
st.write('df.head() : 데이터의 상위 5개 데이터를 확인할 수 있다.')
st.write('df.tail() : 데이터의 상위 5개 데이터를 확인할 수 있다.')

데이터확인 = st.radio("데이터를 확인하기 위한 코드", ('df.head()', 'df.tail()' ), horizontal = True)
if 데이터확인 == 'df.head()':
    st.dataframe(df.head())
elif 데이터확인 == 'df.tail()':
    st.write(df.tail())
st.divider()
st.subheader('2. 데이터프레임 정보 확인')


