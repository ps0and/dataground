import streamlit as st
import numpy as np
import os
import matplotlib.font_manager as fm
from playground import playground
from tutorial1 import tutorial
from dataVisualization import dataVisualization
from dataAi import dataAi

def unique(list):
    x = np.array(list)
    return np.unique(x)

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)


def setPageInfo():
    st.set_page_config(
        page_title="데이터운동장",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    # 고친곳끝


def main():
    setPageInfo()
    fontRegistered()
    st.sidebar.header("데이터와 함께 놀자! \n 데이터 운동장")
    # 고친곳시작
    menu = st.sidebar.selectbox("MENU", ['이용수칙', '데이터 운동장', '인공지능 실험실', '인공지능 놀이터'])
    st.sidebar.caption('이 페이지에는 네이버에서 제공한 나눔글꼴이 적용되어 있습니다.')
    
    

    if menu == '이용수칙':
        tutorial()
    elif menu == '데이터 운동장':
        dataVisualization()
    elif menu == '인공지능 실험실':
        dataAi()
    elif menu == '인공지능 놀이터':
        playground()
    # 고친곳끝


if __name__ == "__main__":
    main()



