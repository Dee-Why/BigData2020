# README

(使用的是conda环境里的bdproject，其中重点是tensorflow必须是2.1.0或更新的版本)

prediction.py : 是tensorflow_code，里面仅仅有一个函数，输入文件路径，返回物品名称字符串

checkpoint/ : 里面存着模型参数

5张图片：用来本地测试prediction能不能正常工作

README.md : this file.



项目计划书：
本项目由三部分组成

1. Flask搭建服务器，要能实现访问127.0.0.1:5000从而访问到我们的服务，页面上有按钮可以实现上传本机图片，有确认键激活图片识别程序并保存在cassandra数据库中
2. tensorflow提供图像识别功能，已经写在prediction.py里面了

```python
# prediction.py
from PIL import Image
import numpy as np
import tensorflow as tf

obj_type = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

model_save_path = './checkpoint/fashion.ckpt'

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.load_weights(model_save_path)

def predict_img(img):
    '''
    the core function of the service
    :param img: the image opened by PIL.Image
    :return:  a string, the type of the object in the image
    '''
    img = img.resize((28, 28), Image.ANTIALIAS)
    img_arr = np.array(img.convert('L'))
    img_arr = 255 - img_arr  # 每个像素点= 255 - 各自点当前灰度值
    img_arr = img_arr / 255.0
    x_predict = img_arr[tf.newaxis, ...]

    result = model.predict(x_predict)
    pred = tf.argmax(result, axis=1)

    # print('type(pred): ', type(pred))
    # print('int(pred): ', int(pred))
    # print('prediction: ', obj_type[int(pred)])
    # print('\n')
    return obj_type[int(pred)]

def predict_imgpath(img_path):
    '''
    the core function of the service

    :param img_path: the path to the image that you want to predict
    :return:  a string, the type of the object in the image
    '''
    img = Image.open(image_path)
    return predict_img(img)


if __name__ == '__main__':
    preNum = int(input("input the number of test pictures:"))
    for i in range(preNum):
        image_path = input("the path of test picture:")
        print(predict_imgpath(image_path))

# ./0_t-shirt.jpeg
# ./1_trouser.jpeg
# ./2_pullover.jpeg
# ./3_dress.jpeg
# ./4_coat.jpeg

'''
timestamp  1_trouser.jpeg  Trouser  (cassandra的三个列)
'''



```

3. cassandra数据库可以通过如下代码链接

```python
import logging

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
#from cassandra.cluster import Cluster
#from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "mykeyspace"

def createKeySpace():
   cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
   session = cluster.connect()
   
   try:
       log.info("Creating keyspace...")
       session.execute("""
           CREATE KEYSPACE %s
           WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
           """ % KEYSPACE)

       log.info("setting keyspace...")
       session.set_keyspace(KEYSPACE)

       log.info("creating table...")
       session.execute("""
           CREATE TABLE mytable (
               timestamp text,
               filename text,
               catagory text,
               PRIMARY KEY (timestamp, filename)
           )
           """)
   except Exception as e:
       log.error("Unable to create keyspace")
       log.error(e)

createKeySpace();


```

4. Dockerfile最后的CMD里面要把flask的内容run起来，因为当容器运行的时候flask服务就应该开始工作了