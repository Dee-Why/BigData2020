# Cassandra刘铭超第二天

在docker里安装cassandra只需要三个单词：`docker pull cassandra`

如果卡的话可能需要后面加几个参数，换源：阿里，清华什么的



我的操作记录

## 第一天

### gitbash

```shell
docker pull cassandra
docker images  # 确认images存在
docker network create deewhy-network
docker network ls  # 确认network存在
docker run --name deewhy-cassandra --network deewhy-network -d cassandra:latest
docker ps  # 发现进程deewhy-cassandra
docker run --name deewhy-cassandra-client -d --network deewhy-network -e CASSANDRA_SEED=deewhy-cassandra cassandra:latest
docker ps  # 发现进程deewhy-cassandra-client
docker rm -f deewhy-cassandra-client  # 发现项目里好像不需要cluster特性，所以删
docker ps  # deewhy-cassandra已经被删除
docker run -it --network deewhy-network --rm cassandra cqlsh deewhy-cassandra

出现报错：the input device is not a TTY.  If you are using mintty, try prefixing the command with 'winpty'

winpty docker run -it --network deewhy-network --rm cassandra cqlsh deewhy-cassandra

出现反应：
Connected to Test Cluster at deewhy-cassandra:9042.
[cqlsh 5.0.1 | Cassandra 3.11.6 | CQL spec 3.4.4 | Native protocol v4]
Use HELP for help.
cqlsh>

以下是在cqlsh里面的指令：

CREATE KEYSPACE animalkeyspace
WITH REPLICATION = { 'class' : 'SimpleStrategy' ,
 'replication_factor' : 1 };
# 数据库里最大的就是KEYSPACE
# 使用简单策略，任何数据都备份一份

```

我在这里出了warning问题，这里是问题详情，不过我继续往后做了一些

```shell
cqlsh> CREATE KEYSPACE animalkeyspace
   ... WITH replication = {'class': 'WITH REPLICATION = {'class' : 'SimpleStrategy',
   ... 'replication_factor' : 1};
   ...
   ... ;
   ...   # 这里我按了下ctrl + C
cqlsh> CREATE KEYSPACE animalkeyspace
   ... WITH REPLICATION = { 'class' : 'SimpleStrategy' ,
   ...  'replication_factor' : 1 };
Warning: schema version mismatch detected; check the schema versions of your nodes in system.local and system.peers.  # 这个报错让我感觉很蒙
cqlsh> CREATE KEYSPACE animalkeyspace WITH REPLICATION = { 'class' : 'SimpleStrategy' ,  'replication_factor' : 1 }; # 于是我又运行了一遍
AlreadyExists: Keyspace 'animalkeyspace' already exists  # 不过他说已经有了
cqlsh>

```

然后到这里就不知道该怎么办了

```shell
cqlsh> use animalkeyspace;
cqlsh:animalkeyspace> CREATE TABLE Monkey (
                  ...   identifier uuid,
                  ...   species text,
                  ...   nickname text,
                  ...   population int,
                  ...   PRIMARY KEY ((identifier), species));
Warning: schema version mismatch detected; check the schema versions of your nodes in system.local and system.peers.  # 我觉得就是这个问题，这个warning和上面的一样
cqlsh:animalkeyspace> select * from monkey
                  ... ;
NoHostAvailable:  #
cqlsh:animalkeyspace> Select * from Monkey;
NoHostAvailable:  #
cqlsh:animalkeyspace> INSERT INTO monkey (identifier, species, nickname, population)
                  ... VALUES ( 5132b130-ae79-11e4-ab27-0800200c9a66,
                  ... 'Capuchin monkey', 'cute', 100000);
NoHostAvailable:  # 三连NoHostAvaliable

```

## 第二天

### gitbash 1

然后第二天docker自动更新了（好像是）重试了一遍，然后就成了

```shell
huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020 (master)
$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
1e5de1ef60e7        bridge              bridge              local
eabeffdc919b        deewhy-network      bridge              local
c2dae2ab99fc        host                host                local
bcdedeb0d0d5        none                null                local

huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020 (master)
$ docker images -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
cassandra           latest              6e1f443aca8c        3 days ago          384MB

huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020 (master)
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020 (master)
$ docker run --name deewhy-cassandra --network deewhy-network -d cassandra:latest
6a518e71ad4bc83d290014d0a955eee8d088add3d372df2770ad036685792529

huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020 (master)
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                         NAMES
6a518e71ad4b        cassandra:latest    "docker-entrypoint.s鈥?   4 seconds ago       Up 3 seconds        7000-7001/tcp, 7199/tcp, 9042/tcp, 9160/tcp   deewhy-cassandra

huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020 (master)
$ winpty docker run -it --network deewhy-network --rm cassandra cqlsh deewhy-cassandra
Connected to Test Cluster at deewhy-cassandra:9042.
[cqlsh 5.0.1 | Cassandra 3.11.6 | CQL spec 3.4.4 | Native protocol v4]
Use HELP for help.
cqlsh> CREATE KEYSPACE animalkeyspace
   ... WITH REPLICATION = { 'class' : 'SimpleStrategy' ,
   ...  'replication_factor' : 1 };
cqlsh> use animalkeyspace;
cqlsh:animalkeyspace> CREATE TABLE Monkey (
                  ... identifier uuid,
                  ... species text,
                  ... nickname text,
                  ... population int,
                  ... PRIMARY KEY ((identifier), species);
SyntaxException: line 6:35 mismatched input ';' expecting ')' (...KEY ((identifier), species)[;])
cqlsh:animalkeyspace> CREATE TABLE Monkey (
                  ... identifier uuid,
                  ... species text,
                  ... nickname text,
                  ... population int,
                  ... PRIMARY KEY ((identifier), species));
cqlsh:animalkeyspace> Select * from Monkey;

 identifier | species | nickname | population
------------+---------+----------+------------

(0 rows)
cqlsh:animalkeyspace> INSERT INTO Monkey (identifier, species, nickname, population)
                  ... VALUES (5132b130-ae79-11e4-ab27-0800200c9a66, 'Capuchin monkey', 'cute', 100000);
cqlsh:animalkeyspace> Select * from Monkey;

 identifier                           | species         | nickname | population
--------------------------------------+-----------------+----------+------------
 5132b130-ae79-11e4-ab27-0800200c9a66 | Capuchin monkey |     cute |     100000

(1 rows)
cqlsh:animalkeyspace>

```

### gitbash 2

获得一个容器里的shell

```shell
huawei@DESKTOP-F0VEIO5 MINGW64 ~/lmc/local_git_repos/BigData2020/learn-cassandra (master)
$ winpty docker exec -it deewhy-cassandra bash  # 就是这行关键指令
root@6a518e71ad4b:/# ls
bin   dev                   etc   lib    media  opt   root  sbin  sys  usr
boot  docker-entrypoint.sh  home  lib64  mnt    proc  run   srv   tmp  var
root@6a518e71ad4b:/#

```

### anaconda prompt

```
conda create -n bdproject python=3.8
pip install cassandra-driver
conda install flask
pip install pyspark  # 这些都是些准备工作
conda install jupyter botebook
```



## 第二天的问题

### 我然后尝试了使用python代码链接docker容器的cassandra数据库

```python
# cas.py
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

               mykey text,

               col1 text,

               col2 text,

               PRIMARY KEY (mykey, col1)

           )

           """)

   except Exception as e:

       log.error("Unable to create keyspace")

       log.error(e)


createKeySpace();
```

然后把dockers里的容器全都删干净，重新按照以下方式运行

```shell
docker run --name deewhy-cassandra -p 9042:9042 -d cassandra:latest
```

运行起来了之后进到conda的bdproject环境里，运行python cas.py

输出了log信息，应该是成功运行了

但是无论是使用

`winpty docker run -it --rm cassandra cqlsh deewhy-cassandra`

还是有病乱求医得使用(因为根本没有用到network...)

`winpty docker run -it --network deewhy-network --rm cassandra cqlsh deewhy-cassandra`

都无法获得`cqlsh>`这个用来写cql语句的prompt了