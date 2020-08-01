# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import datetime
import prediction
import logging
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
from datetime import timedelta
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp','JPEG','jpeg'])
# 设置数据库的KEYSPACE
KEYSPACE = "mykeyspace"



@app.route('/')
def index():
    return redirect(url_for('upload'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        filename = f.filename
        # user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        time.sleep(1)
        pred_str = prediction.predict_imgpath(upload_path)
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        insert_into_db(filename, pred_str)

        return render_template('upload_ok.html', userinput=pred_str, val1=time.time())


def createKeySpace():
    """ Try to establish Cassandra connection and return simple query results """
    cluster = Cluster([os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR', 'localhost')],
                      port=int(os.environ.get('CASSANDRA_PORT_9042_TCP_PORT', 9042))
                      )
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500

    log.info("Creating keyspace...")
    try:
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
                predictcategory text,
                PRIMARY KEY (timestamp, filename)
            )
            """)
    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)

def insert_into_db(filename, predictcategory):
    """ Try to establish Cassandra connection and return simple query results """
    cluster = Cluster([os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR', 'localhost')],
                      port=int(os.environ.get('CASSANDRA_PORT_9042_TCP_PORT', 9042))
                      )
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500
    try:
        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)

        log.info("inserting...")
        stamp = int(time.time())
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime(stamp))
        # now = int(round(time.time() * 1000))
        # now_str = time.strftime('%Y-%m-%d--%H:%M:%S', time.localtime(now / 1000))
        log.info("timestamp is:", timestamp)
        session.execute("""
            INSERT INTO mytable (timestamp, filename, predictcategory)
            VALUES ('{}', '{}', '{}')""".format(timestamp, filename, predictcategory))

    except Exception as e:
        log.error("insertion failed")
        log.error(e)

if __name__ == '__main__':
    createKeySpace()
    # app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)
