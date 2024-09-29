import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.header("📊 히스토그램")
st.write("히스토그램은 :red[**데이터의 분포**]를 시각적으로 표현한 그래프입니다. 연속적인 데이터 값을 여러 구간(bin)으로 나누어, 각 구간에 속하는 데이터 개수를 막대로 표현합니다.")
st.write("히스토그램은 데이터를 쉽게 분포에 따라 분류하고, 특정 값에 데이터가 얼마나 몰려 있는지를 시각적으로 표현할 수 있어, 데이터 분석에서 매우 유용하게 사용됩니다.")
st.write("온도 데이터 또는 임의로 생성한 데이터를 사용하여 히스토그램을 시각화하고, 히스토그램의 장점을 이야기해보자.")

# 데이터 선택
select = st.selectbox("데이터 선택", ["기온 데이터", "임의의 난수 데이터"])

if select == "임의의 난수 데이터":
    # 난수 데이터를 생성
    data = np.random.normal(loc=50, scale=20, size=1000)  # 평균 50, 표준편차 10인 정규분포 데이터
    title = "임의의 난수(평균50, 표준편차20, 데이터1000개)"
    xlabel = "값"
else:
    # 기온 데이터 (예시 데이터를 사용)
    # df = pd.DataFrame({
    #     '날짜': pd.date_range(start='2023-01-01', periods=365),
    #     '기온(°C)': np.random.normal(loc=15, scale=5, size=365)  # 평균 15도, 표준편차 5도
    # })
    df = pd.read_csv('./data/기상관측(기상자료개방포털).csv', encoding='cp949')        
    df = df[['날짜','평균기온(℃)']]
    df = df.dropna()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce', infer_datetime_format=True)    
    df = df[df['날짜']>='2020-01-01']

    data = df['평균기온(℃)']
    title = "2023년 기온 분포"
    xlabel = "평균기온(℃)"

# 두 개의 열로 구분하여 데이터와 그래프를 표시
c1, c2 = st.columns(2)

# 데이터 표시
c1.subheader("데이터")
if select == "임의의 난수 데이터":
    c1.write(pd.DataFrame(data, columns=["값"]))
else:
    c1.write(df)

# 히스토그램 그리기
c2.subheader("그래프")

# 한글 폰트 설정 및 matplotlib 설정
plt.rc('font', family='NanumGothic')
plt.rc('axes', unicode_minus=False)

# 히스토그램 그리기
fig, ax = plt.subplots()

ax.hist(data, bins=20, color='skyblue', edgecolor='black')  # bins: 구간의 수
plt.title(title)
plt.xlabel(xlabel)
plt.ylabel("빈도수")

# Streamlit에서 그래프 출력
c2.pyplot(fig)



st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("graph03.py")

if next_btn:
    st.switch_page("playground.py")