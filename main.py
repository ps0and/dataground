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
    데이터선택 = st.selectbox("데이터 선택",
                         ['인구(kosis)', '기상관측(기상자료개방포털)', '장애인건강검진(kosis)', '청소년흡연(kosis)', '타이타닉(kaggle)', '파일 올리기'])
    if 데이터선택 == '파일 올리기':
        uploaded_file = st.file_uploader("데이터 학습에 사용할 파일을 올려주세요(csv)")
        # 고친곳시작
        dataframe = pd.read_csv('./data/' + '인구(kosis)' + '.csv', encoding='cp949', thousands=',')
        # 고친곳끝
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file, encoding="cp949", thousands=',')
    else:
        dataframe = pd.read_csv('./data/' + 데이터선택 + '.csv', encoding='cp949', thousands=',')

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
            label="차트 다운로드",
            data=file,
            file_name="fig.png",
            mime='image/png'
        )


def dataAi():
    st.header("🧪인공지능 실험실")
    st.subheader("데이터 선택")
    데이터선택 = st.selectbox("데이터 선택", ['타이타닉 데이터(kaggle)','당뇨병 데이터(kaggle)'], label_visibility='collapsed')

    if 데이터선택 == '타이타닉 데이터(kaggle)':
        clist = [
            'PassengerID : 탑승객 고유 아이디',
            'Survival : 생존 유무 (사망 : 0, 생존 : 1)',
            'Pclass : 등실의 등급',
            'Name : 이름',
            'Sex : 성별',
            'Age : 나이',
            'Sibsp : 동승한 형제자매, 아내, 남편의 수',
            'Parch : 동승한 부모, 자식의 수',
            'Ticket :티켓 번호',
            'Fare : 티켓의 요금',
            'Cabin : 객실번호',
            'Embarked : 배에 탑승한 항구 이름',
        ]
        c = st.columns(4)
        for i, value in enumerate(clist):
            c[i%4].write(value)

        df = pd.read_csv('./data/타이타닉(kaggle).csv')
    elif 데이터선택 == '당뇨병 데이터(kaggle)':
        clist = [
            'Pregnancies : 임신횟수',
            'Glucose : 포도당 농도',
            'BloodPressure : 혈압',
            'SkinThickness : 피부두께',
            'Insulin : 인슐린',
            'BMI : 체질량지수',
            'DiabetesPedigreeFunction : 당뇨병 혈통 기능',
            'Age : 나이',
            'Outcome : 당뇨병 여부(0: 발병되지 않음, 1: 발병)',
        ]
        c = st.columns(3)
        for i, value in enumerate(clist):
            c[i % 3].write(value)
        df = pd.read_csv('./data/당뇨병(kaggle).csv')
    st.write(df.head())
    st.divider()
    # 고친곳시작
    col1, col3, col2 = st.columns([3, 1, 1])
    col1.subheader("열 선택")
    col1.write("최소 두 개의 데이터(예측 항목과 예측을 위해 학습시킬 데이터)를 선택하세요")
    선택컬럼 = col1.multiselect("열 선택", df.columns, default=[df.columns[1], df.columns[2]], label_visibility='collapsed')
    data = df[선택컬럼]
    col3.subheader("데이터 처리")
    col3.write("결측치 제거 유무를 선택하세요")
    데이터처리 = col3.selectbox("데이터 처리", ['없음', '결측치제거'], label_visibility='collapsed')
    if 데이터처리 == '결측치제거':
        data = data.dropna()
    col2.subheader("예측항목")
    col2.write("예측 항목을 선택하세요")
    target = col2.selectbox('Target Value', data.columns, label_visibility='collapsed')
    targetData = data.pop(target)
    st.write('')

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
    # 고친곳끝
    st.header("")

    ds = tf.data.Dataset.from_tensor_slices((dict(data), targetData))

    st.divider()
    st.subheader('데이터 특성 설정(feature columns)')

    특성 = st.columns(len(data.columns))
    feature_columns = []
    for i, value in enumerate(data.columns):
        fc = 특성[i].radio(value + "특성을 선택하세요", ["일반 숫자", "카테고리(one_hot)"], horizontal=True, key=value)
        if fc == "일반 숫자":
            feature_columns.append(tf.feature_column.numeric_column(value))
        elif fc == "카테고리(one_hot)":
            vocab = data[value].unique()
            cat_c = tf.feature_column.categorical_column_with_vocabulary_list(value, vocab)
            one_hot = tf.feature_column.indicator_column(cat_c)
            feature_columns.append(one_hot)
    st.header("")
    st.subheader("신경망 모델 생성하기")
    신경망col = st.columns(3)
    레이어개수 = 신경망col[0].number_input("신경망 레이어 개수 선택", step=1, value=3)
    손실함수 = 신경망col[1].selectbox("손실함수 선택", ['mean_squared_error', 'binary_crossentropy','categorical_crossentropy','sparse_categorical_crossentropy'])
    학습횟수 = 신경망col[2].number_input("학습 횟수 선택", step=1, value=10)
    컬럼 = st.columns(레이어개수)
    레이어 = []
    레이어.append(tf.keras.layers.DenseFeatures(feature_columns))
    for i in range(레이어개수):
        if i == 레이어개수 - 1:
            노드개수 = 컬럼[i].number_input("노드 개수 선택", step=1, value=1, key='노드개수' + str(i))
            활성함수 = 컬럼[i].radio("활성함수 선택", ['sigmoid', 'tanh', 'relu','softmax'], key='활성함수' + str(i), horizontal=True)
        else:
            노드개수 = 컬럼[i].selectbox("노드 개수 선택", [128, 64, 32], key='노드개수' + str(i))
            활성함수 = 컬럼[i].radio("활성함수 선택", ['sigmoid', 'tanh', 'relu','softmax'], key='활성함수' + str(i), horizontal=True)
        레이어.append(tf.keras.layers.Dense(노드개수, activation=활성함수))

    model = tf.keras.Sequential(레이어)

    model.compile(optimizer='adam', loss=손실함수, metrics=['acc'])

    ds_batch = ds.batch(3)
    st.divider()
    btn = st.button('학습시작')
    if btn:
        history = model.fit(ds_batch, shuffle=True, epochs=학습횟수)

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
        # model.save('./model/diabetes')
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
    menu = st.selectbox('모델을 선택하세요', ['타이타닉 데이터', '당뇨병 데이터'])
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
        생존확률 = round(생존확률, 2) * 100
        생존확률 = str(int(생존확률)) + '%'
        문장 = '당신의 생존확률은 :red[' + 생존확률 + ']입니다.'
        st.header(문장)
    elif menu == '당뇨병 데이터':
        # Pregnancies: 임신횟수
        # Glucose: 포도당
        # 농도
        # BloodPressure: 혈압
        # SkinThickness: 피부두께
        # Insulin: 인슐린
        # BMI: 체질량지수
        # DiabetesPedigreeFunction: 당뇨병
        # 혈통
        # 기능
        # Age: 나이
        # Outcome: 당뇨병
        # 여부(0: 발병되지
        # 않음, 1: 발병)
        new_model = tf.keras.models.load_model('./model/diabetes')
        col1, col2, col3, col4 = st.columns(4)
        # if 데이터선택 == "타이타닉 데이터":
        임신횟수 = col1.number_input('임신횟수를 입력하세요.', value=0, step=1)
        나이 = col2.number_input('나이를 입력하세요', value=20, step=1)
        bmi = col3.number_input('BMI지수를 입력하세요', value=20, step=1)
        혈압 = col4.number_input('혈압을 입력하세요', value=80, step=1)

        예측 = pd.DataFrame({
            'BloodPressure': [혈압],
            'BMI': [bmi],
            'Age': [나이],
            'Pregnancies' : [임신횟수]
        })
        예측 = tf.data.Dataset.from_tensor_slices(dict(예측))
        예측 = 예측.batch(32)
        # 오류나는부분
        예측값 = new_model.predict(예측)
        확률 = 예측값[0][0].item()
        확률 = round(확률, 2) * 100
        확률 = str(int(확률)) + '%'
        문장 = '당뇨병일 확률은 :red[' + 확률 + ']입니다.'
        st.header(문장)

    # 고친곳시작(추가)


def tutorial():
    st.title("데이터 운동장에 오신 여러분 환영합니다🎈🎉")
    st.header(' 1. 데이터 운동장⚽')
    st.subheader(" 1) 파일을 선택하거나 올릴수 있어요.")
    st.write('CSV파일을 올릴 수 있어요.')
    st.write('오류있는 데이터가 있는지 잘 확인해주세요.')
    st.subheader(" 2) 데이터를 선택할 수 있어요.")
    st.write("데이터의 행렬을 변경해야할 때는 행렬전환 체크박스를 선택해주세요.")
    st.write("필요한 데이터의 열만 선택할 수 있습니다.")
    st.subheader(" 3) 데이터를 시각화 할 수 있어요.")
    st.write("line, bar, hist 그래프를 그릴 수 있어요.")
    st.write("그래프를 그리기 위해 x, y 데이터를 선택해주세요.")
    st.divider()

    st.header('2. 인공지능 실험실🧪')
    st.subheader("1). 데이터를 선택할 수 있어요")
    st.write("현재 제공되는 데이터는 타이타닉 데이터와 당뇨병 데이터 2개가 있어요")
    st.subheader("2). 필요한 데이터를 선택할 수 있어요.")
    st.write("필요한 데이터의 열만 선택할 수 있어요")
    st.write("데이터 정보를 통해 결측치를 확인하고 결측치가 있다면 제거해주세요.")
    st.write("예측하고자하는 데이터는 예측항목으로 선택해주세요")
    st.subheader('3). 신경망 모델을 디자인할 수 있어요.')
    st.write('원핫인코딩 기능을 제공합니다.')
    st.write('자신이 원하는 신경망 모델의 레이어 개수와 노드를 선택하세요.')
    st.write('손실함수, 활성함수, 학습횟수를 선택할 수 있어요')
    st.divider()
    st.header('3. 인공지능 놀이터🎠')
    st.subheader("데이터를 입력하여 결과를 예측할 수 있어요!")
    st.write("타이타닉 데이터를 학습시켰습니다. 내가 타이타닉에 탑승했다면 살았을까요?")
    st.write("당뇨병 데이터를 학습시켰습니다. 내가 당뇨병에 걸릴 확률은 얼마일까요?")
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



