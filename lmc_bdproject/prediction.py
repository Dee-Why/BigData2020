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

def predict_imgpath(img_path):
    '''
    the core function of the service

    :param img_path: the path to the image that you want to predict
    :return:  a string, the type of the object in the image
    '''
    img = Image.open(image_path)
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
