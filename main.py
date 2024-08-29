import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import io
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
        dataframe = pd.read_csv('./data/' + '인구(kosis)' + '.csv', encoding='cp949', thousands=',')
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file, encoding="cp949", thousands=',')
    else:
        dataframe = pd.read_csv('./data/' + 데이터선택 + '.csv', encoding='cp949', thousands=',')

    col1, col2, col3 = st.columns(3)
    행렬전환 = col1.checkbox("행렬 전환")
    if 행렬전환:
        dataframe = dataframe.transpose()
    컬럼번호 = col2.number_input("변경할 컬럼 번호", step=1, value=0)
    컬럼변경버튼 = col3.button("컬럼명 변경")
    if 컬럼변경버튼:
        dataframe.rename(columns=dataframe.iloc[컬럼번호], inplace=True)
        
    st.subheader("2. 데이터 확인")
    st.write(dataframe.head())
    buffer = io.StringIO()
    dataframe.info(buf=buffer)
    st.write("데이터프레임 정보 확인하기")
    st.write(buffer.getvalue()[190:])
    
    컬럼명 = dataframe.columns
    st.subheader("3. 자료형 변경")
    자료형_c1, 자료형_c2 = st.columns(2)
    
    자료형_컬럼 = 자료형_c1.multiselect('변경할 컬럼을 선택하세요', 컬럼명)
    변경할_자료형 = []
    for value in 자료형_컬럼:
        자료형_변경 = 자료형_c2.selectbox(value, ['int', 'str', 'float'], key=value)
        변경할_자료형.append(자료형_변경)
    자료형_변경_버튼 = 자료형_c1.button("자료형 변경")
    if 자료형_변경_버튼:
        for i, c in enumerate(자료형_컬럼):
            dataframe[c] = dataframe[c].astype(변경할_자료형[i])
    buffer = io.StringIO()
    dataframe.info(buf=buffer)
    st.write("데이터프레임 정보 확인하기")
    st.write(buffer.getvalue()[190:])

    st.subheader("4. 데이터 선택(열)")
    컬럼선택 = st.multiselect('컬럼명을 선택하세요', 컬럼명)
    data = dataframe[컬럼선택]
    st.write("상위 5개 데이터를 보여줍니다.")
    st.write(data.head())

    st.subheader("5. 데이터선택(행)")
    st.write()
    

    행c1, 행c2 = st.columns(2)
    행항목 = 행c1.multiselect('조건을 적용할 열 이름을 선택하세요', 컬럼선택)
    행항목리스트 = []
    for value in 행항목:
        행항목리스트.append(행c2.text_input(value+"에 적용할 조건을 입력하세요"))

    
    for i, value in enumerate(행항목리스트):
        행str = 행항목[i]+value        
        data = data.query(행str)
        

    행필터 = st.button("확인하기")    
    if 행필터:
        st.subheader("전처리 완료!!!")
        st.write(data)

    st.subheader("6. 데이터 시각화")
    차트종류 = st.radio("차트 종류를 선택하세요", ['line', 'bar', 'hist'])

    col1, col2, col3 = st.columns(3)
    컬럼선택.append('index')

    x데이터=''
    y데이터=''
    y2데이터=''

    x데이터 = col1.selectbox("x축 데이터", 컬럼선택)

    if 차트종류 == 'line':
        y데이터 = col2.multiselect("y축 데이터", 컬럼선택)
        y2데이터 = col3.multiselect("y2축 데이터", 컬럼선택)
    elif 차트종류 == 'bar':
        y데이터 = col2.selectbox("y축 데이터", 컬럼선택)   

    plt.rc('font', family='NanumGothic')
    plt.rc('axes', unicode_minus=False )

    fig, ax = plt.subplots()

    if x데이터 == 'index':
        x = data.index
    else:
        x = data[x데이터]
    if 차트종류 == 'line':
        for col in y데이터:
            ax.plot(x, data[col], label=col)  # y데이터의 각 컬럼에 대해 라인을 그리며 레이블 추가
        if y2데이터:
            ax2 = ax.twinx()
            for col in y2데이터:
                ax2.plot(x, data[col], label=col)
            ax2.legend(loc="upper right")
        ax.legend(loc="upper left")  # 범례 추가


    elif 차트종류 == 'bar':
        y = data[y데이터]
        ax.bar(x, y, label=y데이터)
        ax.legend()
    else:
        ax.hist(x, label=x데이터)
        ax.legend()

    if x데이터 == 'index':
        ax.set_xlabel('index')
    else:
        ax.set_xlabel(x데이터)
    if y데이터 == 'index':
        ax.set_ylabel('index')
    else:
        ax.set_ylabel(y데이터)
    if y2데이터:
        if y2데이터 == 'index':            
            ax2.set_ylabel('index')
        else:            
            ax2.set_ylabel(y데이터)
    

    st.write('축 데이터 개수 설정')
    축_개수_설정 = st.checkbox('축 개수 설정하기')
    if 축_개수_설정:
        c1, c2 = st.columns(2)
        x축개수 = c1.number_input("x축 최대 개수", value=10, step=1)
        y축개수 = c2.number_input("y축 최대 개수", value=10, step=1)
        ax.yaxis.set_major_locator(MaxNLocator(y축개수))
        ax.xaxis.set_major_locator(MaxNLocator(x축개수))
    
    차트그리기_버튼 = st.button('차트 그리기')
    if 차트그리기_버튼:
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

    st.subheader('데이터 특성 설정')

    st.subheader('데이터 특성 설정')

    특성 = st.columns(len(data.columns))
    inputs = []
    encoded_inputs = []

    for i, value in enumerate(data.columns):
        fc = 특성[i].radio(value + "특성을 선택하세요", ["일반 숫자", "카테고리(one_hot)"], horizontal=True, key=value)
        
        if fc == "일반 숫자":
            input_layer = tf.keras.layers.Input(shape=(1,), name=value)
            inputs.append(input_layer)
            encoded_inputs.append(input_layer)
        
        elif fc == "카테고리(one_hot)":
            # 문자열 범주형 데이터를 정수로 변환 후 One-hot 인코딩
            input_layer = tf.keras.layers.Input(shape=(1,), dtype=tf.string, name=value)
            lookup = tf.keras.layers.StringLookup(output_mode='int')(input_layer)
            one_hot_encoded = tf.keras.layers.CategoryEncoding(num_tokens=lookup.vocabulary_size(), output_mode="one_hot")(lookup)
            
            inputs.append(input_layer)
            encoded_inputs.append(one_hot_encoded)

    # Concatenate all encoded inputs
    if len(encoded_inputs) > 1:
        concatenated_inputs = tf.keras.layers.Concatenate()(encoded_inputs)
    else:
        concatenated_inputs = encoded_inputs[0]

    # 신경망 모델 생성
    st.subheader("신경망 모델 생성하기")
    신경망col = st.columns(3)
    레이어개수 = 신경망col[0].number_input("신경망 레이어 개수 선택", step=1, value=3)
    손실함수 = 신경망col[1].selectbox("손실함수 선택", ['mean_squared_error', 'binary_crossentropy','categorical_crossentropy','sparse_categorical_crossentropy'])
    학습횟수 = 신경망col[2].number_input("학습 횟수 선택", step=1, value=10)

    x = concatenated_inputs
    for i in range(레이어개수):
        노드개수 = 128 if i < 레이어개수 - 1 else 1
        활성함수 = 'relu' if i < 레이어개수 - 1 else 'sigmoid'
        x = tf.keras.layers.Dense(노드개수, activation=활성함수)(x)

    model = tf.keras.Model(inputs=inputs, outputs=x)

    model.compile(optimizer='adam', loss=손실함수, metrics=['acc'])

    ds_batch = ds.batch(32)
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
    st.subheader("모델을 선택하세요")
    menu = st.selectbox('모델을 선택하세요', ['타이타닉 데이터', '당뇨병 데이터'], label_visibility='collapsed')
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
        new_model = tf.keras.models.load_model('./model/diabetes')
        col1, col2, col3, col4,col5 = st.columns(5)
        # if 데이터선택 == "타이타닉 데이터":

        임신횟수 = col1.number_input('임신횟수를 입력하세요.', value=0, step=1)
        나이 = col2.number_input('나이를 입력하세요', value=20, step=1)
        키 = col3.number_input('키를 입력하세요', value=170, step=1)
        몸무게 = col4.number_input('몸무게를 입력하세요', value=60, step=1)
        혈압 = col5.number_input('혈압을 입력하세요', value=80, step=1)

        bmi = 몸무게/키**2

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
    st.subheader("1) 데이터를 선택할 수 있어요")
    st.write("현재 제공되는 데이터는 타이타닉 데이터와 당뇨병 데이터 2개가 있어요")
    st.subheader("2) 필요한 데이터를 선택할 수 있어요.")
    st.write("필요한 데이터의 열만 선택할 수 있어요")
    st.write("데이터 정보를 통해 결측치를 확인하고 결측치가 있다면 제거해주세요.")
    st.write("예측하고자하는 데이터는 예측항목으로 선택해주세요")
    st.subheader('3) 신경망 모델을 디자인할 수 있어요.')
    st.write('원핫인코딩 기능을 제공합니다.')
    st.write('자신이 원하는 신경망 모델의 레이어 개수와 노드를 선택하세요.')
    st.write('손실함수, 활성함수, 학습횟수를 선택할 수 있어요')
    st.divider()
    st.header('3. 인공지능 놀이터🎠')
    st.subheader("데이터를 입력하여 결과를 예측할 수 있어요!")
    st.write("내가 만약 타이타닉에 탑승했다면?")
    st.write("내가 당뇨병에 걸릴 확률은?")
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



