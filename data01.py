import streamlit as st
import pandas as pd



st.header("🔧 데이터 불러오기")
st.divider()
st.write("csv파일로 저장된 데이터를 python에서 편집할 수 있도록 불러오자!")

st.subheader("코드")
st.code("""import pandas as pd
df = pd.read_csv('데이터.csv')
df.head()""", language='python')
df = pd.read_csv('./data/축구선수(kaggle).csv')


st.write('csv파일을 데이터프레임으로 잘 가져왔는지, 오류는 없는지 일부 데이터를 확인한다.')
st.write('df.head() : 데이터의 상위 5개 데이터를 확인할 수 있다.')
st.write('df.tail() : 데이터의 상위 5개 데이터를 확인할 수 있다.')

st.subheader("불러온 데이터 확인하기")

데이터확인 = st.radio("head(), tail()을 선택해 데이터를 확인해보자.", ('df.head()', 'df.tail()' ), horizontal = True)
if 데이터확인 == 'df.head()':
    st.dataframe(df.head())
elif 데이터확인 == 'df.tail()':
    st.write(df.tail())
st.divider()



