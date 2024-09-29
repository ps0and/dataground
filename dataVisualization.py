import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from matplotlib.ticker import MaxNLocator




st.header('🧫데이터 실험실')
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
    if value=='':
        continue
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

colors_ax1 = ['orange', 'blue', 'green', 'red', 'purple']
colors_ax2 = ['pink', 'cyan', 'olive', 'brown', 'gray']

if 차트종류 == 'line':
    for i, col in enumerate(y데이터):
        ax.plot(x, data[col], label=col, color=colors_ax1[i % len(colors_ax1)])  # y데이터의 각 컬럼에 대해 라인을 그리며 레이블 추가
    
    if y2데이터:
        ax2 = ax.twinx()
        for i, col in enumerate(y2데이터):
            ax2.plot(x, data[col], label=col, color=colors_ax2[i % len(colors_ax2)])
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