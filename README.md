本项目是使用neo4j库构建的。只修改了neo4j数据构建的代码。问答代码没来得及修改，py2neo库21年就停止更新。

Neo4j下载网址：

https://we-yun.com/doc/neo4j/

jdk下载网址：

https://www.oracle.com/cn/java/technologies/downloads/archive/

查看当前java版本 java –version

卸载 sudo apt remove openjdk-11-*

安装sudo apt update

sudo apt install openjdk-17-jdk

配置系统以使用新安装的Java版本。使用以下命令设置默认的Java版本：

sudo update-alternatives --config java

查看当前java版本 java –version

neo4j版本一定要和jdk版本对应，否则安装失败

tar -axvf neo4j安装包

切换到解压的文件启动neo4j

./bin/neo4j start

停止neo4j

./bin/neo4j stop

如果无法正常启动需要修改neo4j配置文件

Bolt连接和http连接 

neo4j.conf配置文件修改成下面

# Bolt connector

server.bolt.enabled=true

#server.bolt.tls_level=DISABLED

server.bolt.listen_address=0.0.0.0:7687

#server.bolt.advertised_address=:7687

# HTTP Connector. There can be zero or one HTTP connectors.

server.http.enabled=true

server.http.listen_address=0.0.0.0:7474


连接后默认账户和密码都是neo4j,会让自己修改密码（一定要记着修改后密码）
