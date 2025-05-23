import streamlit as st
import pandas as pd
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES

#페이지 제목
st.header("🎬 결측치 확인")
st.divider()

st.write("데이터셋에서 누락된 값이 있을 때 이를 처리하는 과정이다. 결측값이 있는 데이터를 그대로 사용하면 분석 결과가 왜곡될 수 있다.")

#데이터 가져오기
df = pd.read_csv('./data/타이타닉(kaggle).csv')
df = df[['Survived','Pclass', 'Gender', 'Age']]
col1, col2, col3 = st.columns([2,1,1])

col1.subheader("데이터 확인하기")
col1.code("df[:10]", language='python')
col1.write(df[:10])
col2.subheader("결측치 확인")
col2.code("df.isnull().sum()")
col2.write(df.isnull().sum())
col3.subheader("결측치가 아닌 데이터 확인")
col3.code("df.notnull().sum()")
col3.write(df.notnull().sum())



st.divider()
#해보기


st.header('해보기')


data = pd.DataFrame({
    '이름': ['지민', '사나', '태연', '민호', '제니'],
    '나이': [28, 22, None, 35, 30],
    '키': [173, None, 160, 182, 163],
    '점수': [85, 90, 78, None, 95]
})

c2, c1 = st.columns([2, 1])

c1.subheader("데이터")
c1.write(data)

c2.subheader("결측치 확인하기")

with c2:    
    code = st_ace(
        placeholder="코드를 작성하세요.",
        language="python",
        theme="twilight",
        keybinding="vscode",
        font_size=14,
        tab_size=4,               
        min_lines=3,
        show_gutter=True,
        value = '''data'''         
    )


# exec 실행 시 직접 결과를 출력 (예외 처리 추가)
try:
    exec(code)
    #st.success("코드가 성공적으로 실행되었습니다.")
except Exception as e:
    c2.error(f"코드를 실행하는 동안 오류가 발생했습니다: {e}")

#실행결과 출력

result = data.copy()



if code == 'data':
    pass
elif code == 'data.isnull().sum()':
    c2.success("정답입니다!!!")    
    c2.balloons()
else:
    c2.error("오답입니다!!! 코드를 확인해보세요.")
c2.write("실행결과")
code = "st.write("+code+")"
exec(code)


st.divider()
c1, c2, c3 = st.columns([1,5,1])
prev_btn = c1.button("이전")
next_btn = c3.button("다음")

if prev_btn:
    st.switch_page("data04.py")

if next_btn:
    st.switch_page("data06.py")
