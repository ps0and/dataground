import streamlit as st
import sqlite3

st.header("회원가입")
c1, c2 = st.columns(2)
uid = c1.text_input("아이디", placeholder="아이디를 입력하세요")
pw = c1.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요.")
pw_check = c1.text_input("비밀번호 확인", type='password', placeholder="비밀번호를 한번더 입력하세요.")
name = c1.text_input("이름", placeholder="이름을 입력하세요")
school = c2.text_input("학교", placeholder="학교를 입력하세요")
grade = c2.text_input("학년", placeholder="학년을 입력하세요")
ban = c2.text_input("반", placeholder="반을 입력하세요")
num = c2.text_input("번호", placeholder="번호를 입력하세요")


btn = st.button("회원가입")

conn = sqlite3.connect('database.db')

c = conn.cursor()

if btn:
    c.execute(f"""INSERT INTO User(uid, pw, name, school, grade, ban, num, progress)
                values('{uid}','{pw}','{name}','{school}',{grade},{ban},{num},0)
""")
    conn.commit()
    st.success("성공")

