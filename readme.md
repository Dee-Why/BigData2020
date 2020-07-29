# BigData2020
this is the Big Data project  of MIT in the summer of 2020

everything from learning the basic knowledge to the final product should be included in this repo, but devided into different directorys.



## 我现在能够做到的是

Flask：搭建服务器，其特点是可以通过URL的访问激活函数，并能在URL接受指定的GET,POST,PUT,DEL请求。返回值会显示在网页上

Cassandra（已经容器化）：数据库，使用CQL语言。我可以用python的接口执行cql语句，这样的话存入数据我知道该怎么做了，但是取出数据还不是很清楚

tensorflow_code：现在已经有了可以接收文件路径之输出图片类别的函数（模型已经训练好，每次调用前加载模型即可）



## 我理解的任务是

搭建一个容器（作为服务器），使得用户可以通过POST方法带着自己的图片提出请求

用户的图片需要保存在容器的文件系统内，用户的图片在容器中的绝对路径filepath（如有必要，需要打上时间戳防止重名

利用filepath调用tensorflow_code，得到预测结果

将filepath字符串和预测结果字符串（如有必要还可以将用户的信息也一起）存入cassandra数据库中

现在的问题有：

1. 这些东西最终都要整合到一个容器里，发送到dockerhub么？
2. 如果不是的话，会是一个什么样的结构