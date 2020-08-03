# BigData2020

if you just want to know about my final product--the containerized webservice of cloth image classification-- you can look at the retry2_docker/ directory and ignore all the rest

the README file in retry2_docker/ will guide you the way.

## explaination in detail

this is the Big Data project  of MIT in the summer of 2020

everything from learning the basic knowledge to the final product are included in this repo, but devided into different directories.

to build the image from my source code, just cd into the `retry2_docker/` directory (which contains the final stable version source code) and use the command below if you can use docker

`docker build -t <any name you like>:<any version number you like> .`

please pay attention to the `.`at the tail of the command above, it means the current directory, which is `retry2_docker/`

the name of the directory is retry2_docker just because it successfully build on my second try. It doesn't means anything else\~

## 我现在能够做到的是

tensorflow_code（作为一个package）：现在已经有了模型和checkpoint文件，写了 *接收文件路径，输出图片类别* 的函数（模型已经训练好，加载checkpoint即可使用）

Flask（上传图片upload）：搭建服务器，其特点是可以通过URL的访问激活函数，并能在URL接受指定的GET,POST,PUT,DEL请求。返回值会显示在网页上

Cassandra（已经容器化）：数据库，使用CQL语言。我可以用cassandra-driver这个python的接口执行cql语句，这样的话存入数据就很简单了



## 任务分析

搭建一个容器（作为服务器），使得用户可以通过POST方法带着自己的图片提出请求，

~用户的图片需要保存在容器的文件系统内，用户的图片在容器中的绝对路径filepath（如有必要，需要打上时间戳防止重名~

~利用filepath调用tensorflow_code，得到预测结果~

直接使用用户的图片进行分类预测

将filepath字符串和预测结果字符串（如有必要还可以将用户的信息也一起）存入cassandra数据库中

现在的问题有：

1. 这些东西最终都要整合到一个容器里，发送到dockerhub



## 做出来的阶段性成果

可以在本地运行flask服务，在localhost的相应端口访问服务

可以在浏览器里上传图片并得到物品分类信息

上传时间，文件名，分类信息会被保存到另一个docker容器里的cassandra数据库中

docker run --name deewhy-cassandra --network deewhy-network -p 9042:9042 -d cassandra:latest

winpty docker run -it --network deewhy-network --rm cassandra cqlsh deewhy-cassandra



## 第三阶段成果

目前来看也是最终结果

已经把flask服务容器化。

只需要在同一个network中先后运行起来cassandra容器和flask服务的容器，并且把flask服务的容器的8987端口映射到本机的某个端口（这里假设映射到本机的8987端口），那么就可以靠本机访问localhost:8987来使用基于flask框架开发的网络服务了。

具体来讲是以下三条指令

```shell
docker network create deewhy-network
docker run --name deewhy-cassandra --network deewhy-network -d cassandra:3.11.7
docker run --name deewhy-webservice --network deewhy-network -p 8987:8987 -d deewhy-webservice-image:v4.2
```

之后打开本机的浏览器，输入`localhost:8987/`即可访问到服务页面