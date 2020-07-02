import numpy as np
import pandas as pd
import time as time
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import pickle
from sklearn.externals.joblib import dump, load

# 데이터 확인, 분석을 위해 pandas 를 사용
xy_df = pd.read_csv('csv/iris.csv')
xy_df = xy_df.dropna(how='all', axis=0)  # 결측치 제거


# 레이블 인코딩 과정 (문자열(종류)을 대응하는 정수로 변경)
labelEncoder = LabelEncoder()

# 레이블 인코딩(문자열 레이블->정수)
xy_df.iloc[:, [-1]
           ] = labelEncoder.fit_transform(xy_df.iloc[:, [-1]].values.reshape(-1))

np.save('model/classes.npy', labelEncoder.classes_)

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
dump(scaler, 'model/std_scaler.bin', compress=True)

x_train_scaled = scaler.transform(x_train)

x_test_scaled = scaler.transform(x_test)

xgb = XGBClassifier()  # max_depth=3, n_estimators=1000, learning_rate=0.05

parameters = {
    'max_depth': [3, 6, 9],
    'n_estimators': [100, 500, 1000]
}


grid_xgb = GridSearchCV(xgb, param_grid=parameters, cv=3, refit=True)

print("학습 시작")
start = time.time()  # 시작 시간 저장
grid_xgb.fit(x_train_scaled, y_train.reshape(-1))
print("학습 종료")
print("학습 시간 : ", str(time.time() - start)
      [:6], "초", sep="")  # 현재시각 - 시작시간 = 실행 시간

scores_df = pd.DataFrame(grid_xgb.cv_results_)

print(scores_df[['params', 'mean_test_score',
                 'rank_test_score', 'split0_test_score']])

print("최적 파라미터 : ", grid_xgb.best_params_)
print("최고 정확도 : ", grid_xgb.best_score_)

model = grid_xgb.best_estimator_

prediction = model.predict(x_test_scaled)

print("테스트 세트 정확도 : {0:.4f}".format(accuracy_score(prediction, y_test)))

print("모델 저장")
filename = 'result.model'

pickle.dump(model, open("model/"+filename, "wb"))
