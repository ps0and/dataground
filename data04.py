import streamlit as st
import pandas as pd

st.header("🎬 행 필터링")
st.divider()

df = pd.read_csv('./data/축구선수(kaggle).csv')
st.subheader("1. 열 필터링 결과")
df = df[['short_name', 'age', 'overall','nationality_name']]

st.write(df)

st.subheader("2. 특정 조건을 만족하는 데이터 추출하기")
st.write("우리나라 선수들만 추출해보자!!")
df_korean = df[df['nationality_name']=='Korea Republic']

#st.write(df['nationality_name'].unique())
st.code("""df_korean = df[df['nationality_name']=='Korea Republic']""")

st.write(df_korean)

st.divider()

st.header("💻 해보기")
st.write(" -축구강국 브라질의 축구선수들을 확인해보자!")

# 사용자 코드 입력 받기
df_brazil=''
code = st.text_area("코드를 작성하고 Ctrl+Enter를 누르세요", '''df_brazil = df''')


# exec 실행 시 직접 결과를 출력 (예외 처리 추가)
try:
    exec(code)
    st.success("코드가 성공적으로 실행되었습니다.")
except Exception as e:
    st.error(f"코드를 실행하는 동안 오류가 발생했습니다: {e}")

# 실행 결과 출력
st.subheader("실행결과 확인")
st.write(df_brazil)

df_result = df[df['nationality_name']=='Brazil']
try:
    if df_result.equals(df_brazil):
        # st.write("정답입니다.")
        st.toast("정답입니다.")
        st.balloons()
    else:
        st.toast("오답입니다.")
        # st.write("오답입니다.")
except Exception as e:
    # st.write("오답입니다.")
    st.toast("오답입니다.")

