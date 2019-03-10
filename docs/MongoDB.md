# Linux安装MongoDB
1. 下载源码包

```shell
cd /opt
curl https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.0.6.tgz
```

2. 解压

```shell
tar -zxvf mongodb-linux-x86_64-rhel70-4.0.6.tgz
```

3. 可执行文件位于解压后的bin目录下,将bin添加到环境变量中

```
export PATH=<mongodb-install-directory>/bin:$PATH
```

<mongodb-install-directory>为MongoDB的安装路径,如/opt/mongodb

4. 进行MongoDB数据库配置

```shell
# 创建数据库目录
mkdir -p <mongodb-install-directory>/data/db
# 创建日志存放目录
mkdir <mongodb-install-directory>/logs
```

```shell
vim <mongodb-install-directory>/bin/mongodb.conf
# 配置信息
dbpath = <mongodb-install-directory>/data/db # 数据库路径
logpath = <mongodb-install-directory>/logs/mongodb.log # 日志输出路径
port = 27017 # 端口号
fork = true # 设置后台运行
```

5. 以守护进程启动MongoDB服务端

```shell
mongod -f <mongodb-install-directory>/bin/mongodb.conf
```
