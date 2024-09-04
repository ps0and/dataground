import streamlit as st
import pandas as pd

#페이지 제목
st.header("🎬 결측치")
st.divider()

st.write("데이터셋에서 누락된 값이 있을 때 이를 처리하는 과정이다. 결측값이 있는 데이터를 그대로 사용하면 분석 결과가 왜곡될 수 있다.")

#데이터 가져오기
df = pd.read_csv('./data/타이타닉(kaggle).csv')
df = df[['Survived', 'Name', 'Pclass', 'Gender', 'Age']]
col1, col2, col3 = st.columns([2,1,1])

col1.subheader("데이터 확인하기")
col1.code("df.head()")
col1.write(df.head())
col2.subheader("결측치 확인")
col2.code("df.isnull().sum()")
col2.write(df.isnull().sum())
col3.subheader("결측치가 아닌 데이터 확인")
col3.code("df.notnull().sum()")
col3.write(df.notnull().sum())

st.divider()
#해보기
st.subheader("결측치 처리하기")
c1, c2, c3, c4 = st.columns(4)

c1.write("1. 결측 데이터 제거")
df_drop = df.dropna()
c1.code("df_drop = df.dropna()")

result = pd.DataFrame(df_drop.notnull().sum())
result.columns=['NotNull']
result['Null'] = pd.DataFrame(df_drop.isnull().sum())
c1.write(result)


c2.write("2. 특정 값으로 대체")
df_mean = df
df_mean['Age'].fillna(df_mean['Age'].mean(), inplace=True)
c2.code("""
df_mean = df
mean = df_mean['Age'].mean()
df_mean.['Age'].fillna(mean, inplace=True)""", language='python')


result = pd.DataFrame(df_mean.notnull().sum())
result.columns=['NotNull']
result['Null'] = pd.DataFrame(df_mean.isnull().sum())
c2.write(result)




c3.write("3. 평균값으로 대체")
df_mean = df
df_mean['Age'].fillna(df_mean['Age'].mean(), inplace=True)
c3.code("""
df_mean = df
mean = df_mean['Age'].mean()
df_mean.['Age'].fillna(mean, inplace=True)""", language='python')


result = pd.DataFrame(df_mean.notnull().sum())
result.columns=['NotNull']
result['Null'] = pd.DataFrame(df_mean.isnull().sum())
c3.write(result)


st.header('해보기')

#실행결과 출력
st.subheader("실행결과 출력")
