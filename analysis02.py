import streamlit as st
import pandas as pd
import numpy as np

st.header("분산과 표준편차")
st.write("분산과 표준편차는 데이터의 변동성을 파악해 데이터가 평균으로부터 얼마나 많이 떨어져 있는지 확인하기 위해 사용한다.")

st.subheader("1. 분산")
st.write("각 데이터 값이 평균에서 얼마나 떨어져 있는지를 제곱하여 계산한 값으로 분산이 크면 데이터들이 넓게 퍼져 있고 분산이 작으면 값들이 평균 근처에 모여있다는 것을 의미한다.")

st.code("df['컬럼'].var()", language='python')

st.subheader("2. 표준편차")
st.write("분산의 제곱근으로 데이터의 변동성을 원래 데이터 단위로 표현한 값이다. 표준편차가 클수록 데이터 값들의 변동은 크다.")
st.code("df['컬럼'].std()", language='python')

st.divider()
st.subheader("확인하기")
st.write(":gray[데이터를 더블클릭해서 변경하면 분산과 표준편차가 변하는 것을 확인할 수 있다.]")
data = {'국어': np.random.normal(loc=40, scale=10, size=10),
        '수학': np.random.normal(loc=60, scale=30, size=10)}
df = pd.DataFrame(data)
df['국어']=np.clip(data['국어'], 0, 100)
df['수학']=np.clip(data['수학'], 0, 100)

c_1, c_2 = st.columns([1,1])
result = c_1.data_editor(df)

df = result
c_2.write("국어 분산 : :red[" + str(df['국어'].var())+"]")
c_2.write("수학 분산 : :red[" + str(df['수학'].var())+"]")
c_2.code("""df['국어'].var()
df['수학'].var()""", language='python')

c_2.write("국어 표준편차 : :red[" + str(df['국어'].std())+"]")
c_2.write("수학 표준편차 : :red[" + str(df['수학'].std())+"]")
c_2.code("""df['국어'].std()
df['수학'].std()""", language='python')





st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("analysis01.py")

if next_btn:
    st.switch_page("analysis03.py")