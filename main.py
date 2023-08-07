import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.font_manager as fm
from matplotlib.ticker import MaxNLocator





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

def dataVisualization():
    st.header('데이터 분석 도구')
    fontRegistered()

    st.subheader("1. 데이터 올리기")
    uploaded_file = st.file_uploader("데이터 학습에 사용할 파일을 올려주세요(csv)")
    col1, col2, col3 = st.columns(3)
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file, encoding="cp949", thousands=',')

        행렬전환 = col1.checkbox("행렬 전환")
        if 행렬전환:
            dataframe = dataframe.transpose()
            컬럼번호 = col2.number_input("컬럼명 지정", step=1)
            dataframe.rename(columns=dataframe.iloc[컬럼번호], inplace=True)
            삭제번호 = col3.number_input("삭제할 행 개수 선택", step=1)
            for i in range(삭제번호):
                dataframe = dataframe.drop(dataframe.index[0])

        st.write(dataframe.head())
        컬럼명 = dataframe.columns
        st.subheader("2. 데이터 선택")
        컬럼선택 = st.multiselect('컬럼명을 선택하세요', 컬럼명)
        data = dataframe[컬럼선택]
        st.write("상위 5개 데이터를 보여줍니다.")
        st.write(data.head())
        st.subheader("3. 데이터 시각화")
        차트종류 = st.radio("차트 종류를 선택하세요", ['line', 'bar', 'hist'])

        col1, col2 = st.columns(2)
        컬럼선택.append('index')
        x데이터 = col1.selectbox("x축 데이터", 컬럼선택)
        if 차트종류 == 'line':
            y데이터 = col2.multiselect("y축 데이터", 컬럼선택)
        else:
            y데이터 = col2.selectbox("y축 데이터", 컬럼선택)

        plt.rc('font', family='NanumGothic')

        fig, ax = plt.subplots()

        if x데이터 == 'index':
            x = data.index
        else:
            x = data[x데이터]
        if y데이터 == 'index':
            y = data.index
        else:
            y = data[y데이터]
        if x데이터 == 'index':
            ax.set_xlabel('index')
        else:
            ax.set_xlabel(x데이터)
        if y데이터 == 'index':
            ax.set_ylabel('index')
        else:
            ax.set_ylabel(y데이터)


        ax.yaxis.set_major_locator(MaxNLocator(10))
        ax.xaxis.set_major_locator(MaxNLocator(10))
        if 차트종류 == 'line':
            ax.plot(x, y)
            st.pyplot(fig)
        elif 차트종류 == 'bar':
            ax.bar(x, y)
            st.pyplot(fig)
        else:
            ax.hist(x)
            st.pyplot(fig)
        plt.savefig('./img/fig.png')
        with open('./img/fig.png', 'rb') as file:
            downBtn = st.download_button(
                label = "차트 다운로드",
                data=file,
                file_name = "fig.png",
                mime='image/png'
            )

def dataAi():
    st.write("인공지능")
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
    menu = st.sidebar.selectbox("MENU", ['데이터 분석 도구', '인공지능 분석 도구'])
    
    if menu == '데이터 분석 도구':
        dataVisualization()
    elif menu == '인공지능 분석 도구':
        dataAi()
    else:
        st.header('Data PlayGround')
    
    
    
    


if __name__ == "__main__":
    main()



