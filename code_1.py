import streamlit as st
from streamlit_ace import st_ace

# Spawn a new Ace editor
content = st_ace(language="python", 
                 placeholder="여기에 코드를 입력하세요.",
                 theme="github",
                 font_size=20,
                 keybinding="vscode", value="""a=1
b=2
a+b
""")

# Display editor's content as you type

content
rows = content.split(" ")
for row in rows:
    exec(row)

st.write(row)
