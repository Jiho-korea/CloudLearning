# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename
import numpy as np
import os
import pandas as pd
import time as time
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import pickle

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 이곳에선 사용자의 샘플 테스트 시 수행할 코드 작성

        # # 파라미터를 전달 받습니다.
        # mhw = float(request.form['mhw'])

        # # 최저 시급 변수를 선언합니다.
        # price = 0

        # # 입력된 파라미터를 배열 형태로 준비합니다.
        # data = ((mhw), (0))
        # arr = np.array(data, dtype=np.float32)

        # # 입력 값을 토대로 예측 값을 찾아냅니다.
        # x_data = arr[0:1]
        # dict = sess.run(hypothesis, feed_dict={X: [x_data]})

        # # 결과 배추 가격을 저장합니다.
        # price = dict[0]
        new_file = request.files['csv']  # 요청 파라미터 에서 csv파일 구함
        print("파일이름 : ", new_file.filename, "\n")  # 파일 확인
        new_file.save("csv/"+secure_filename(new_file.filename))  # csv 파일 저장

        return render_template('index.html', prediction=prediction)


@app.route("/training", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        new_file = request.files['csv']  # 요청 파라미터 에서 csv파일 구함
        print("파일이름 : ", new_file.filename, "\n")  # 파일 확인
        new_file.save("csv/"+secure_filename(new_file.filename))  # csv 파일 저장

        #####################################################################

        # 데이터 확인, 분석을 위해 pandas 를 사용
        xy_df = pd.read_csv(new_file.filename)
        xy_df = xy_df.dropna(how='all', axis=0)  # 결측치 제거

        # 레이블 인코딩 과정 (문자열(종류)을 대응하는 정수로 변경)
        labelEncoder = LabelEncoder()

        # 레이블 인코딩(문자열 레이블->정수)
        xy_df.iloc[:, [-1]
                   ] = labelEncoder.fit_transform(xy_df.iloc[:, [-1]].values.reshape(-1))

        # 레이블 데이터(종류)를 numpy로 추출
        y_data = xy_df.iloc[:, -1].values.reshape(-1, 1)

        x_data = xy_df.iloc[:, :-1].values  # 피쳐데이터를 numpy로 추출

        print(x_data.shape)
        print(x_data[:5, :])  # 피쳐 확인

        # 테스트세트를 분리
        x_train, x_test, y_train, y_test = train_test_split(
            x_data, y_data, test_size=0.2, stratify=y_data)  # 전체 데이터중 30%

        print("학습용 ", x_train.shape, "\t", y_train.shape)  # 학습용 피쳐, 레이블 데이터
        print("테스트용 ", x_test.shape, "\t",
              y_test.shape, "\n")  # 테스트용 피쳐, 레이블 데이터

        scaler = StandardScaler()

        scaler.fit(x_train)

        x_train_scaled = scaler.transform(x_train)

        x_test_scaled = scaler.transform(x_test)

        xgb = XGBClassifier()  # max_depth=3, n_estimators=1000, learning_rate=0.05

        parameters = {
            'max_depth': [3, 6, 9],
            'n_estimators': [100, 500, 1000]
        }

        grid_xgb = GridSearchCV(xgb, param_grid=parameters, cv=3, refit=True)

        print("학습 시작.....")
        start = time.time()  # 시작 시간 저장
        grid_xgb.fit(x_train_scaled, y_train.reshape(-1))
        print("학습 종료", "\n")
        print("학습 시간 : ", str(time.time() - start)
              [:6], "초", sep="")  # 현재시각 - 시작시간 = 실행 시간

        scores_df = pd.DataFrame(grid_xgb.cv_results_)

        print(scores_df[['params', 'mean_test_score',
                         'rank_test_score', 'split0_test_score']])
        print()
        print("최적 파라미터 : ", grid_xgb.best_params_, "\n")
        print("최고 정확도 : ", grid_xgb.best_score_)

        model = grid_xgb.best_estimator_

        prediction = model.predict(x_test_scaled)
        score = accuracy_score(prediction, y_test)
        print("테스트 세트 정확도 : {0:.4f}".format(score), "\n")
        print("모델 저장")
        filename = 'result.model'

        pickle.dump(model, open("model/"+filename, "wb"))

        return render_template('index.html', result=True, trainingscore=str(grid_xgb.best_score_*100)[:6], testscore=str(score*100)[:6])


@app.route('/model/<path:filename>', methods=['POST'])
def download(filename):
    return send_from_directory(directory='model', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
