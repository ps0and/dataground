import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.header("📊 막대 그래프")
st.write("막대 그래프는 :red[**데이터의 비교**]를 시각적으로 표현한 그래프입니다. 주로 범주형 데이터나 특정 시점의 데이터를 비교하는 데 유용합니다.")
st.write("막대 그래프는 여러 데이터 항목의 크기 차이를 직관적으로 보여줄 수 있어 데이터를 쉽게 비교할 수 있습니다.")
st.write("막대 그래프를 사용하면 지역별 인구현황, 매출 현황 등 데이터의 차이를 명확하게 시각화할 수 있습니다.")
st.write("광역시별 인구 현황 또는 장애인건강검진 데이터를 막대 그래프로 시각화한 자료를 살펴보고 막대그래프의 장점을 이야기해보자.")

# 데이터 선택
select = st.selectbox("데이터 선택", ["광역시별 인구현황", "OO전자 5년간 영업이익"])

if select == "OO전자 5년간 영업이익":
    df = pd.DataFrame({
    '연도': [2018, 2019, 2020, 2021, 2022, 2023],    
    '영업이익': [58.89, 27.76, 35.99, 51.63, 43.38, 38.50]
})

    

    x = df['연도']
    y = df['영업이익']
else:
    df = pd.DataFrame({
    '광역시': ['서울특별시', '부산광역시', '대구광역시', '인천광역시', 
             '광주광역시', '대전광역시', '울산광역시', '세종특별자치시'],
    '인구(명)': [9733509, 3411829, 2411410, 2943204, 
              1456717, 1469843, 1116037, 365309]
})

    x = df['광역시']
    y = df['인구(명)']

# 두 개의 열로 구분하여 데이터와 그래프를 표시
c1, c2 = st.columns(2)

c1.subheader("데이터")
c1.dataframe(df)
c2.subheader("그래프")

# 한글 폰트 설정 및 matplotlib 설정
plt.rc('font', family='NanumGothic')
plt.rc('axes', unicode_minus=False)

# 막대 그래프 그리기
fig, ax = plt.subplots()

ax.bar(x, y)  # 막대 그래프 사용

# ax.xaxis.set_major_locator(MaxNLocator(6))  # X축 레이블 개수 제한
plt.xticks(rotation=45)  # X축 레이블 회전

# Streamlit에서 그래프 출력
c2.pyplot(fig)



st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("graph01.py")

if next_btn:
    st.switch_page("graph03.py")