import streamlit as st
import time

st.write("TEST")
with st.spinner('Wait for it...'):
    time.sleep(5)
st.success("Done!")