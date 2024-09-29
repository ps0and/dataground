import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.header("📈 꺾은선 그래프")
st.write("꺾은선 그래프는 :red[**연속적인 데이터**]의 변화를 시각적으로 표현한 그래프로 시간의 흐름에 따른 변화나 추세를 쉽게 파악할 수 있다는 장점이 있다.")
st.write("꺾은선 그래프를 사용하면 시간에 따른 데이터 변화를 예측하거나 데이터의 변화를 이하하는데 도움이 된다.")
st.write("주식가격변화, 인구변화, 기온변화등 데이터의 변화를 꺾은선 그래프로 표현하면 데이터의 변화를 쉽게 파악할 수 있다.")
st.write("기온 데이터의 변화를 꺽은선 그래프로 시각화한 자료를 살펴보고 데이터 시각화의 장점을 이야기해보자")

select = st.selectbox("데이터 선택", ["기온데이터", "인구데이터"])

if select=="기온데이터":
    df = pd.read_csv('./data/기상관측(기상자료개방포털).csv', thousands=',', encoding='cp949')
    df = df[['날짜','평균기온(℃)']]
    df = df.dropna()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce', infer_datetime_format=True)    
    df = df[df['날짜']>='2023-01-01']
    df = df[df['날짜']<='2023-12-31']
    df = df[['날짜','평균기온(℃)']]
    x = df['날짜']
    y = df['평균기온(℃)']
else:
    df = pd.read_csv('./data/인구(kosis).csv', thousands=',', encoding='cp949')
    df = df[['시점','총인구(명)']]
    df = df[df['시점']>=1970]
    df = df[df['시점']<=2024]

    x = df['시점']
    y = df['총인구(명)']


c1, c2 = st.columns(2)

c1.subheader("데이터")
c1.write(df)
c2.subheader("그래프")

plt.rc('font', family='NanumGothic')
plt.rc('axes', unicode_minus=False )

fig, ax = plt.subplots()


ax.plot(x, y)
ax.xaxis.set_major_locator(MaxNLocator(6))
c2.pyplot(fig)

st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("analysis03.py")

if next_btn:
    st.switch_page("graph02.py")