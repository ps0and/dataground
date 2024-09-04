import streamlit as st
import numpy as np
import os
import matplotlib.font_manager as fm

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


def main():
    setPageInfo()
    fontRegistered()

    pages = {
        "알아보기":[
            st.Page("tutorial1.py", title="시작하기"),
            st.Page("tutorial2.py", title="데이터 분석이란?"),
            st.Page("tutorial3.py", title="데이터 전처리란?")
        ],
        "데이터 학습하기": [            
            st.Page("data01.py", title="1. 데이터 불러오기"),
            st.Page("data02.py", title="2. 데이터프레임 확인하기"),
            st.Page("data03.py", title="3. 열 필터링"),
            st.Page("data04.py", title="4. 행 필터링"),
            st.Page("preprocessing.py", title="데이터전처리 학습하기"),
            st.Page("dataVisualization.py", title="데이터 운동장"),
        ],
        "인공지능 학습하기": [
            st.Page("dataAi.py", title="인공지능 실험실"),
            st.Page("playground.py", title="인공지능 놀이터"),
        ],
    }

    pg = st.navigation(pages)
    pg.run()



if __name__ == "__main__":
    main()

