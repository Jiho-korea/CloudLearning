# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug import secure_filename
import datetime
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)

# 플레이스 홀더를 설정합니다.
X = tf.placeholder(tf.float32, shape=[None, 1])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([1, 1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="bias")
# 가설을 설정합니다.

hypothesis = tf.matmul(X, W) + b

# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.train.Saver()
model = tf.global_variables_initializer()

# 세션 객체를 생성합니다.
sess = tf.Session()
sess.run(model)

# 저장된 모델을 세션에 적용합니다.
save_path = "./model/saved.cpkt"
saver.restore(sess, save_path)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 이곳에선 사용자의 샘플 테스트 시 수행할 코드 작성
        # 파라미터를 전달 받습니다.
        mhw = float(request.form['mhw'])

        # 최저 시급 변수를 선언합니다.
        price = 0

        # 입력된 파라미터를 배열 형태로 준비합니다.
        data = ((mhw), (0))
        arr = np.array(data, dtype=np.float32)

        # 입력 값을 토대로 예측 값을 찾아냅니다.
        x_data = arr[0:1]
        dict = sess.run(hypothesis, feed_dict={X: [x_data]})

        # 결과 배추 가격을 저장합니다.
        price = dict[0]

        return render_template('index.html', price=price)


@app.route("/training", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        new_file = request.files['csv']
        print("파일이름 : ", new_file.filename)
        new_file.save(secure_filename(new_file.filename))

        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
