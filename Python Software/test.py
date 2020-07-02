# 저장된 model 을 load 하여 테스트하는 py파일

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pickle

# 데이터 확인, 분석을 위해 pandas 를 사용
test_df = pd.read_csv('iris_test.csv')
test_df = test_df.dropna(how='all', axis=0)  # 결측치 제거

x_data = test_df.values  # 피쳐데이터를 numpy로 추출

print(x_data.shape)

scaler = StandardScaler()

x_data_scaled = scaler.fit_transform(x_data)

print("모델 로드")
filename = 'result.model'
loaded_model = pickle.load(open(filename, "rb"))

prediction = loaded_model.predict(x_data_scaled)
print(prediction)

labelEncoder = LabelEncoder()
labelEncoder.classes_ = np.load('classes.npy', allow_pickle=True)

print(labelEncoder.inverse_transform(prediction))

test_df['prediction'] = labelEncoder.inverse_transform(prediction)

print(test_df)

test_df.to_csv('csv/result_test.csv', sep=',', na_rep='NaN', index=False)
