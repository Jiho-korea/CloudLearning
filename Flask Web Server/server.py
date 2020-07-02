﻿# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_from_directory, escape, session
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
from joblib import dump, load

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/training", methods=['POST'])
def training_model():
    if request.method == 'POST':
        new_file = request.files['csv']  # 요청 파라미터 에서 csv파일 구함
        print("파일이름 : ", new_file.filename, "\n")  # 파일 확인
        new_file.save("csv/"+secure_filename(new_file.filename))  # csv 파일 저장

        #####################################################################

        # 데이터 확인, 분석을 위해 pandas 를 사용
        xy_df = pd.read_csv("csv/" + new_file.filename)
        xy_df = xy_df.dropna(how='all', axis=0)  # 결측치 제거

        # 레이블 인코딩 과정 (문자열(종류)을 대응하는 정수로 변경)
        labelEncoder = LabelEncoder()

        # 레이블 인코딩(문자열 레이블->정수)
        xy_df.iloc[:, [-1]
                   ] = labelEncoder.fit_transform(xy_df.iloc[:, [-1]].values.reshape(-1))

        # fit 한 class 저장
        np.save('model/classes.npy', labelEncoder.classes_)

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
        dump(scaler, 'model/std_scaler.bin', compress=True)

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

        session['result'] = True
        session['trainingscore'] = str(grid_xgb.best_score_*100)[:6]
        session['testscore'] = testscore = str(score*100)[:6]

        return render_template('index.html', result=True, trainingscore=str(grid_xgb.best_score_*100)[:6], testscore=str(score*100)[:6])


@app.route("/test", methods=['POST'])
def test_model():
    # 이곳에선 사용자의 샘플 테스트 시 수행할 코드 작성
    if request.method == 'POST':
        new_file = request.files['csv']  # 요청 파라미터 에서 csv파일 구함
        print("파일이름 : ", new_file.filename, "\n")  # 파일 확인
        new_file.save("csv/"+secure_filename(new_file.filename))  # csv 파일 저장

        # ############################################################ ############################################################

        # test 용 csv 로드
        test_df = pd.read_csv("csv/" + new_file.filename)
        test_df = test_df.dropna(how='all', axis=0)  # 결측치 제거

        x_data = test_df.values  # numpy로 변경

        print(x_data.shape)

        scaler = load('model/std_scaler.bin')
        x_data_scaled = scaler.fit_transform(x_data)

        print("모델 로드\n")
        filename = 'result.model'
        loaded_model = pickle.load(open("model/"+filename, "rb"))

        print("테스트 시작")
        prediction = loaded_model.predict(x_data_scaled)
        print(prediction)

        labelEncoder = LabelEncoder()
        labelEncoder.classes_ = np.load('model/classes.npy', allow_pickle=True)

        print(labelEncoder.inverse_transform(prediction))

        test_df['prediction'] = labelEncoder.inverse_transform(prediction)

        print(test_df)

        test_df.to_csv('./csv/result_test.csv', sep=',',
                       na_rep='NaN', index=False)

#         session['result'] = True
#         session['trainingscore'] = str(grid_xgb.best_score_*100)[:6]
#         session['testscore'] = testscore = str(score*100)[:6]

        if 'result' in session:
            result = '%s' % escape(session['result'])
        if 'trainingscore' in session:
            trainingscore = '%s' % escape(session['trainingscore'])
        if 'testscore' in session:
            testscore = '%s' % escape(session['testscore'])
        print("테스트 끝")
        # ############################################################ ############################################################
        return render_template('index.html', testSuccess=True, result=True, trainingscore=trainingscore, testscore=testscore)


@app.route('/model/<path:filename>', methods=['POST'])
def download(filename):
    return send_from_directory(directory='model', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
