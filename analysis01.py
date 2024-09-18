import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import pandas as pd
import numpy as np

st.header("평균,중앙,최빈")

st.subheader("1. 평균")
st.write("**평균**은 주어진 데이터의 합을 데이터 개수로 나눈 값으로 전체 데이터의 중심을 나타낸다.")
st.write("평균을 사용하면 데이터를 간결하게 표현할 수 있다. 예를 들면 '중간고사에서 평균 90점을 받았다.' 다양한 과목의 중간고사 성적을 평균점수로 대표할 수 있다. 하지만 평균점수는 극단값(0점이나 100점)이 전체 점수에 큰 영향을 준다는 단점이 있다.")


st.code("df['컬럼명'].mean()", language='python')


st.subheader("2. 중앙값")
st.write("**중앙값**은 데이터를 크기 순으로 정렬했을 때 중간에 위치하는 값이다. 우리반 학생 30명 키의 중앙값은 키가 15번째로 큰 학생의 키가 된다. 중앙값은 평균보다 극단값의 영향을 적게 받는다.")

st.code("df['컬럼명'].median()", language='python')


st.subheader("3. 최빈값")
st.write("**최빈값**은 데이터 중 가장 자주 나타나는 값을 의미하며 분포의 대표적인 값을 찾는데 사용된다. ")

st.code("df['컬럼명'].mode()[0]", language='python')

st.divider()
st.subheader("확인하기")
st.write(":gray[데이터를 더블클릭해서 변경하면 평균값, 중앙값, 최빈값이 변하는 것을 확인할 수 있다.]")
data = {'점수': np.random.normal(loc=60, scale=10, size=10)}
df = pd.DataFrame(data)
df['점수']=np.clip(data['점수'], 0, 100)
df['점수'] = df['점수'].astype(int)
c_1, c_2 = st.columns([1,2])
result = c_1.data_editor(df)

df = result
c_2.write("평균값 : :red[" + str(df['점수'].mean())+"]")
c_2.code("df['점수'].mean()", language='python')

c_2.write("중앙값 : :red[" + str(df['점수'].median())+"]")
c_2.code("df['점수'].median()", language='python')

c_2.write("최빈값 : :red[" + str(df['점수'].mode()[0])+"]")
c_2.code("df['점수'].mode()[0]", language='python')


st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("data06.py")

if next_btn:
    st.switch_page("analysis02.py")
