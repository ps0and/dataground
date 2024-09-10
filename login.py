import streamlit as st
import sqlite3

conn=sqlite3.connect("database.db")
c = conn.cursor()


st.header("로그인")
id = st.text_input("아이디")
pw = st.text_input("비밀번호", type="password")
btn = st.button("로그인")

if btn:
    c.execute(f"select * from User where uid='{id}'")
    rows = c.fetchall()
    row = rows[0]
    if row[1] == id and row[2] == pw:
        st.write("로그인 성공")
        st.switch_page("tutorial1.py")
    else:
        st.error("로그인 실패")

        