import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.font_manager as fm
from matplotlib.ticker import MaxNLocator
import tensorflow as tf




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
    st.header('⚽데이터 운동장')
    st.subheader("1. 데이터 올리기")

    데이터선택 = st.selectbox("데이터 선택", ['인구(kosis)','기상관측(기상자료개방포털)','장애인건강검진(kosis)','청소년흡연(kosis)','타이타닉(kaggle)', '파일 올리기'])
    if 데이터선택 == '파일 올리기':
        uploaded_file = st.file_uploader("데이터 학습에 사용할 파일을 올려주세요(csv)")
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file, encoding="cp949", thousands=',')
    else:
        dataframe = pd.read_csv('./data/'+데이터선택+'.csv', encoding='cp949', thousands=',')

    col1, col2, col3 = st.columns(3)
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
    st.header("🧪인공지능 실험실")
    st.subheader("데이터 선택")
    데이터선택 = st.selectbox("데이터 선택", ['타이타닉 데이터(kaggle)','파일 올리기'],label_visibility='collapsed')
    if 데이터선택 == '파일 올리기':
        uploaded_file = st.file_uploader("데이터 학습에 사용할 파일을 올려주세요(csv)")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, encoding="cp949", thousands=',')
    elif 데이터선택 == '타이타닉 데이터(kaggle)':
        df = pd.read_csv('./data/타이타닉(kaggle).csv')

    st.write(df.head())
    col1, col3, col2 = st.columns([3, 1, 1])
    col1.subheader("열 선택")
    선택컬럼  = col1.multiselect("열 선택", df.columns, label_visibility='collapsed')
    data = df[선택컬럼]
    col3.subheader("데이터 처리")
    데이터처리 = col3.selectbox("데이터 처리", ['없음','결측치제거'], label_visibility='collapsed')
    if 데이터처리 == '결측치제거':
        data = data.dropna()
    col2.subheader("예측항목")
    target = col2.selectbox('Target Value', data.columns, label_visibility='collapsed')
    targetData = data.pop(target)
    col1.header("")
    col2.header("")
    col3.header("")
    col1.subheader('데이터 확인(상위 5개 데이터)')
    col1.write(data.head())
    col3.subheader('데이터 정보')
    count = pd.DataFrame(data.count())
    count.columns = ['개수']
    결측치 = pd.DataFrame(data.isnull().sum())
    count['결측치'] = 결측치
    col3.write(count)
    col2.subheader('Target 데이터')
    col2.write(targetData.head())

    st.header("")
    ds = tf.data.Dataset.from_tensor_slices((dict(data), targetData))
    
    st.subheader('데이터 특성 설정(feature columns)')

    특성 = st.columns(len(data.columns))
    feature_columns = []
    for i, value in enumerate(data.columns):
        fc = 특성[i].radio(value + "특성을 선택하세요", ["일반 숫자", "카테고리(one_hot)"], horizontal=True, key=value)
        if fc == "일반 숫자":
            feature_columns.append(tf.feature_column.numeric_column(value))
        elif fc == "카테고리":
            vocab = data[value].unique()
            cat_c = tf.feature_column.categorical_column_with_vocabulary_list(value, vocab)
            one_hot = tf.feature_column.indicator_column(cat_c)
            feature_columns.append(one_hot)
    st.header("")
    st.subheader("신경망 모델 생성하기")
    레이어개수 = st.number_input("신경망 레이어 개수 선택", step=1 ,value=3)

    컬럼 = st.columns(레이어개수)
    레이어 = []
    레이어.append(tf.keras.layers.DenseFeatures(feature_columns))
    for i in range(레이어개수):
        if i == 레이어개수-1:
            노드개수 = 컬럼[i].number_input("노드 개수 선택", step=1, value=1, key='노드개수' + str(i))
            활성함수 = 컬럼[i].radio("활성함수 선택", ['sigmoid', 'tanh', 'relu'], key='활성함수' + str(i), horizontal=True)
        else:
            노드개수 = 컬럼[i].selectbox("노드 개수 선택", [128,64,32], key='노드개수'+str(i))
            활성함수 = 컬럼[i].radio("활성함수 선택",['sigmoid', 'tanh', 'relu'], key='활성함수'+str(i), horizontal=True)
        레이어.append(tf.keras.layers.Dense(노드개수, activation=활성함수))
    model = tf.keras.Sequential(레이어)



    손실함수 = st.selectbox("손실함수 선택", ['mean_squared_error', 'binary_crossentropy'])
    model.compile(optimizer='adam', loss=손실함수, metrics=['acc'])

    ds_batch = ds.batch(32)
    btn = st.button('학습시작')
    if btn:
        history = model.fit(ds_batch, shuffle = True, epochs=20)

        plt.rc('font', family='NanumGothic')
        fig, ax = plt.subplots()
        ax.set_title('학습 정확도')
        ax.set_ylabel('정확도')
        ax.set_xlabel('학습 횟수')
        ax.yaxis.set_major_locator(MaxNLocator(10))
        ax.xaxis.set_major_locator(MaxNLocator(10))
        ax.plot(history.history["acc"])

        st.pyplot(fig)
        plt.savefig('./img/fig.png')
        model.save('./model/titanic')
        with open('./img/fig.png', 'rb') as file:
            downBtn = st.download_button(
                label="차트 다운로드",
                data=file,
                file_name="fig.png",
                mime='image/png'
            )



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
def playground():
    st.header('🎠인공지능 놀이터')
    # new_model = tf.keras.models.load_model('./model/my_model.h5')
    menu = st.selectbox('가지고 올 모델을 선택하세요',['타이타닉 데이터'])
    if menu == '타이타닉 데이터':
        new_model = tf.keras.models.load_model('./model/titanic')

        col1, col2, col3 = st.columns(3)
        # if 데이터선택 == "타이타닉 데이터":
        나이 = col1.number_input('나이를 입력하세요.', value=30, step=1)
        # 나이 = np.float32(나이)
        객실등급 = col2.number_input('객실 등급을 입력하세요', value=2, step=1)
        # 객실등급 = np.float32(객실등급)
        성별 = col3.selectbox('성별을 선택하세요', ['male', 'female'])

        # 예측하기 = st.button("생존 확률은?")
        # if 예측하기:
        예측 = pd.DataFrame({
            'Age': [나이],
            'Pclass': [객실등급],
            'Gender': [성별]
        })
        예측 = tf.data.Dataset.from_tensor_slices(dict(예측))
        예측 = 예측.batch(32)
        # 오류나는부분
        예측값 = new_model.predict(예측)
        생존확률 = 예측값[0][0].item()
        생존확률 = round(생존확률, 2)*100
        생존확률 = str(int(생존확률))+'%'
        문장 = '당신의 생존확률은 :red['+생존확률+']입니다.'
        st.header(문장)
def main():
    setPageInfo()
    fontRegistered()
    st.sidebar.header("매천고등학교")
    menu = st.sidebar.selectbox("MENU", ['데이터 운동장', '인공지능 실험실','인공지능 놀이터'])
    st.sidebar.caption('이 페이지에는 네이버에서 제공한 나눔글꼴이 적용되어 있습니다.')
    if menu == '데이터 운동장':
        dataVisualization()
    elif menu == '인공지능 실험실':
        dataAi()
    elif menu == '인공지능 놀이터':
        playground()

    
    
    
    


if __name__ == "__main__":
    main()



