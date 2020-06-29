import tensorflow as tf
import numpy as np
from pandas.io.parsers import read_csv

data = read_csv('pure data.csv', sep=',')

xy = np.array(data, dtype=np.float32)

x_data = xy[:,:-1]
y_data = xy[:,[-1]]
#print(x_data)
#print(y_data)

X = tf.placeholder(tf.float32, shape=[None,1])
Y = tf.placeholder(tf.float32, shape=[None,1])
W = tf.Variable(tf.random_normal([1,1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="bias")

hypothesis = tf.matmul(X,W) + b
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.00000001)
train = optimizer.minimize(cost)

sess = tf.Session()
model = tf.global_variables_initializer()
sess.run(model)

epochs = 5

for e in range(epochs):
    for step in range(100001):
        cost_, hypo_, _ = sess.run([cost,hypothesis,train], feed_dict={X:x_data, Y:y_data})
        if(step % 500 == 0):
            print("#" , step, "손실 비용 : " , cost_)
            print(" - 치킨 가격 ", hypo_[0])


saver = tf.train.Saver()
save_path = saver.save(sess, "./saved.cpkt")
print("학습된 모델을 저장하였습니다.")


'''
x_data = [3100,3480,3770,4000,4110,4320,4580,4860,5210,5580,6030,6470,7530,8350]
y_data = [14000,14920,15540,15980,16146.4,16312.8,16479.2,16645.6,16812,16978.4,17144.8,17311.2,17477.6,17976.8]

W = tf.Variable(tf.random_uniform([1],-100,100))
b = tf.Variable(tf.random_uniform([1],-100,100))
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

H = W*X + b

cost = tf.reduce_mean(tf.square(H - Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.00000001)
train = optimizer.minimize(cost)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(2001):
    cost_, hypo_, _ = sess.run([cost, H, train], feed_dict={X: x_data, Y: y_data})
    if (i% 500 == 0):
        print("#", i, "손실 비용 : ", cost_)
        print(" - 치킨 가격 ", hypo_[0])

print(sess.run(H, feed_dict={X:[8350]}))

'''
