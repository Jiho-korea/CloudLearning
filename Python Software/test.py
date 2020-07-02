# 저장된 model 을 load 하여 테스트하는 py파일

import numpy as np
import pandas as pd
import time as time
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle

# 데이터 확인, 분석을 위해 pandas 를 사용
xy_df = pd.read_csv('iris.csv')
xy_df = xy_df.dropna(how='all', axis=0)  # 결측치 제거


# 레이블 인코딩 과정 (문자열(종류)을 대응하는 정수로 변경)
labelEncoder = LabelEncoder()

# 레이블 인코딩(문자열 레이블->정수)
xy_df.iloc[:, [-1]
           ] = labelEncoder.fit_transform(xy_df.iloc[:, [-1]].values.reshape(-1))

y_data = xy_df.iloc[:, -1].values.reshape(-1, 1)  # 레이블 데이터(종류)를 numpy로 추출

x_data = xy_df.iloc[:, :-1].values  # 피쳐데이터를 numpy로 추출

print(x_data.shape)
print(x_data[:5, :])  # 피쳐 확인

# 테스트세트를 분리
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.2, stratify=y_data)  # 전체 데이터중 30%

print("학습용 ", x_train.shape, "\t", y_train.shape)  # 학습용 피쳐, 레이블 데이터
print("테스트용 ", x_test.shape, "\t", y_test.shape)  # 테스트용 피쳐, 레이블 데이터


scaler = StandardScaler()

scaler.fit(x_train)

x_train_scaled = scaler.transform(x_train)

x_test_scaled = scaler.transform(x_test)

print("모델 로드")
filename = 'result.model'
loaded_model = pickle.load(open(filename, "rb"))

prediction = loaded_model.predict(x_test_scaled)

print("테스트 세트 정확도 : {0:.4f}".format(accuracy_score(prediction, y_test)))
