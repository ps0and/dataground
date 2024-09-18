import streamlit as st
import pandas as pd
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES


st.header("🔧 열 필터")
st.divider()

# CSV 파일에서 데이터프레임 불러오기
df = pd.read_csv('./data/축구선수(kaggle).csv')
df2 = df[['short_name', 'age', 'overall']]

st.write("데이터 프레임에 너무 많은 열이 포함되어있다. 분석에 필요하지 않는 열을 제거하는 것을 열 필터라고 한다.")
st.write("분석에 필요한 열 데이터만 추출해보자.")

st.subheader("코드")
st.code("""df_column_filter = df[['short_name', 'age', 'overall']]""", language='python')

st.subheader("실행결과")
st.write(df2)
st.divider()

st.subheader("해보기")
st.write("데이터프레임의 short_name, age, overall, nationality_name 4개의 열을 가져와 df_column_filter에 저장하자.")

# 사용자 코드 입력 받기
df_column_filter=''
# code = st.text_area("열 필터를 위한 코드를 작성하고 Ctrl+Enter를 누르세요", '''df_column_filter = df''')

code = st_ace(
    placeholder="코드를 작성하세요.",
    language="python",
    theme="twilight",
    keybinding="vscode",
    font_size=14,
    tab_size=4,               
    min_lines=3,
    show_gutter=True,
    value = '''df_column_filter = df'''         
)




# 기본값으로 df_column_filter를 빈 문자열로 설정


# exec 실행 시 직접 결과를 출력 (예외 처리 추가)
try:
    exec(code)
except Exception as e:
    st.error(f"코드를 실행하는 동안 오류가 발생했습니다: {e}")

df_result = df[['short_name','age','overall','nationality_name']]

try:
    if df_result.equals(df_column_filter):
        st.success("정답입니다.")
        st.balloons()
    elif code == 'df_column_filter = df':
        st.warning('Ctrl+Enter를 눌러 프로그램을 실행하세요.')
    else:
        st.error("오답입니다.")
except Exception as e:
    st.error("오답입니다.")


# 실행 결과 출력
st.subheader("실행결과 출력")
st.write(df_column_filter)

st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("data02.py")

if next_btn:
    st.switch_page("data04.py")
