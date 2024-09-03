import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder



st.header("🧪인공지능 실험실")
st.subheader("데이터 선택")
데이터선택 = st.selectbox("데이터 선택", ['타이타닉 데이터(kaggle)','당뇨병 데이터(kaggle)'], label_visibility='collapsed')

if 데이터선택 == '타이타닉 데이터(kaggle)':
    clist = [
        'PassengerID : 탑승객 고유 아이디',
        'Survival : 생존 유무 (사망 : 0, 생존 : 1)',
        'Pclass : 등실의 등급',
        'Name : 이름',
        'Gender : 성별',
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

col1, col2 = st.columns([3, 1])
col1.subheader("열 선택")
col1.write("최소 두 개의 데이터(예측 항목과 예측을 위해 학습시킬 데이터)를 선택하세요")
선택컬럼 = col1.multiselect("열 선택", df.columns, default=[df.columns[1], df.columns[2]], label_visibility='collapsed')
data = df[선택컬럼]



col2.subheader("예측항목")
col2.write("예측 항목을 선택하세요")
target = col2.selectbox('Target Value', data.columns, label_visibility='collapsed')


col1.subheader('데이터 확인(상위 5개 데이터)')
col1.write(data.head())

col2.subheader('Target 데이터')
col2.write(data[target].head())


col1.subheader("데이터 처리")
col1.write("결측치 제거 유무를 선택하세요")

데이터처리 = col1.selectbox("데이터 처리", ['제거하지 않음', '결측치제거','결측치 채우기'], label_visibility='collapsed')
if 데이터처리 == '결측치제거':
    data = data.dropna()
elif 데이터처리 == '결측치 채우기':
    결측_컬럼 = col1.multiselect('컬럼 선택', data.columns)        
    for value in 결측_컬럼:
        처리방법 = col1.selectbox(value+"결측치 처리", ['평균값', '중앙값', '최대값', '최소값', '0'])
        if 처리방법 == '평균값':
            data[value].fillna(data[value].mean(), inplace=True)
        elif 처리방법 == '중앙값':
            data[value].fillna(data[value].median(), inplace=True)
        elif 처리방법 == '최대값':
            data[value].fillna(data[value].max(), inplace=True)
        elif 처리방법 == '최소값':
            data[value].fillna(data[value].min(), inplace=True)
        elif 처리방법 == '0':
            data[value].fillna(0, inplace=True)
    
    
    # data['Age'].fillna(data['Age'].mean(), inplace=True)
    

count = pd.DataFrame(data.count())
count.columns = ['개수']
결측치 = pd.DataFrame(data.isnull().sum())
count['결측치'] = 결측치
col2.subheader('결측치 확인')
col2.write(count)

#x, y 데이터 분리
X = data.drop(target, axis=1)
Y = data[target]

st.write('')



st.header("")
st.divider()
st.subheader('데이터 특성 설정(feature columns)')

try:
    특성 = st.columns(len(data.columns))

    for i, value in enumerate(data.columns):
        fc = 특성[i].radio(value + "특성을 선택하세요", ["일반 숫자", "범주형 데이터"], horizontal=True, key=value)
        if fc == "범주형 데이터":
            X[value] = LabelEncoder().fit_transform(X[value])
            
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X)


    # 신경망 모델 생성
    st.subheader("신경망 모델 생성하기")
    신경망col = st.columns(3)
    레이어개수 = 신경망col[0].number_input("신경망 레이어 개수 선택", step=1, value=3)
    손실함수 = 신경망col[1].selectbox("손실함수 선택", ['mean_squared_error', 'binary_crossentropy','categorical_crossentropy','sparse_categorical_crossentropy'])
    학습횟수 = 신경망col[2].number_input("학습 횟수 선택", step=1, value=10)


    레이어 = [tf.keras.layers.InputLayer(input_shape=(X_train.shape[1],))]

    for i in range(레이어개수):        
        노드개수 = 신경망col[0].number_input(str(i)+"번 레이어의 노드 개수", value=128, step=1)
        활성함수 = 신경망col[1].selectbox(str(i)+"번 레이어의 활성화함수", ['relu', 'sigmoid'])
        레이어.append(tf.keras.layers.Dense(노드개수, activation=활성함수))
        

    btn = st.button("학습시작")
    st.write()
    if btn:
        try:
            model = tf.keras.Sequential(레이어)

            model.compile(optimizer='adam', loss=손실함수, metrics=['acc'])
            history = model.fit(X_train, Y, shuffle=True, epochs=학습횟수, batch_size=32, validation_split=0.2)

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
        except Exception as e:
            st.error(f'예상치 못한 오류가 발생했습니다. {e}')
except ValueError as ve:
    st.error(f'범주형 데이터가 포함되어있습니다. 확인해보세요. {ve}')
except Exception as e:
    st.error(f'예상치 못한 오류가 발생했습니다: {e}')