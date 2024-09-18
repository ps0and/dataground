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
        "데이터 전처리": [            
            st.Page("data01.py", title="1. 데이터 불러오기"),
            st.Page("data02.py", title="2. 데이터 확인"),
            st.Page("data03.py", title="3. 열 필터링"),
            st.Page("data04.py", title="4. 행 필터링"),
            st.Page("data05.py", title="5. 결측치 확인"),
            st.Page("data06.py", title="6. 결측치 처리")
        ],
        "데이터 분석":[
            st.Page("analysis01.py", title="1. 평균,중앙,최빈"),
            st.Page("analysis02.py", title="2. 분산과 표준편차"),
            st.Page("analysis03.py", title="3. 상관관계")
        ],
        "데이터 시각화":[
            st.Page("graph01.py", title="1. 꺽은선 그래프"),
            st.Page("graph02.py", title="2. 막대 그래프"),
            st.Page("graph03.py", title="3. 원 그래프"),
            st.Page("graph04.py", title="4. 히스토그램")
        ],        
        "데이터 실습하기" :[
            st.Page("dataVisualization.py", title="데이터 운동장")
        ],
        "인공지능 데이터 분석 기법":
        [
            st.Page("ai1.py", title="1. 회귀분석"),
            #분류분석(로지스틱 회귀, k-NN)
            #클러스터링(K-Means, 계층적 군집화)
            #시계열 분석
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