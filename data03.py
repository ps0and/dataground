import streamlit as st
import pandas as pd

st.header("🔧 열 필터")

# CSV 파일에서 데이터프레임 불러오기
df = pd.read_csv('./data/축구선수(kaggle).csv')
df2 = df[['short_name', 'age', 'overall']]

st.write("데이터 프레임의 열 필터링은 원하는 열만 선택하여 새로운 데이터 프레임을 만드는 과정입니다.")
st.write("이 과정에서 우리는 분석에 필요한 정보만 추출합니다.")

st.subheader("코드")
st.code("""df_column_filter = df[['short_name', 'age', 'overall']]""")

st.subheader("실행결과")
st.write(df2)
st.divider()

st.subheader("해보기")
st.write("데이터프레임의 short_name, age, overall, nationality_name 4개의 열을 가져와 df_column_filter에 저장해 보세요.")

# 사용자 코드 입력 받기
df_column_filter=''
code = st.text_area("열 필터를 위한 코드를 작성하고 Ctrl+Enter를 누르세요", '''df_column_filter = df''')

# 기본값으로 df_column_filter를 빈 문자열로 설정


# exec 실행 시 직접 결과를 출력 (예외 처리 추가)
try:
    exec(code)
    st.success("코드가 성공적으로 실행되었습니다.")
except Exception as e:
    st.error(f"코드를 실행하는 동안 오류가 발생했습니다: {e}")

# 실행 결과 출력
st.write(df_column_filter)
