#Big Data Audit
By [Kotobukki](https://github.com/kotobukki/).

[![Build Status](https://camo.githubusercontent.com/f8bbfdc05d49bbdad27dba5693bccade8cd36e12/68747470733a2f2f7472617669732d63692e6f72672f6a696d656e6269616e2f446174614d696e696e672e7376673f6272616e63683d6d6173746572)](https://travis-ci.org/kotobukki/BigDataAudit)
[![Support]
(https://camo.githubusercontent.com/4a42460f88f172b10e916fec11857648a8a2f2c8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f706c6174666f726d2d6f73782532466c696e757825324677696e646f77732d677265656e2e737667)](https://travis-ci.org/kotobukki/BigDataAudit)
[![Support]
(https://camo.githubusercontent.com/352488c0cbba0e8f6da11ae0761444dd0c93489c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d322e372d626c75652e737667](https://travis-ci.org/kotobukki/BigDataAudit)

##使用说明
程序的入口文件是main.py, 可以使用下面的命令查看怎么使用
```
$python main.py -h
usage: main.py [-h] {hadoop,spark} ...

This is a tool for detectiong the security problem of hadoop!

positional arguments:
  {hadoop,spark}  commands
    hadoop        check security of hadoop
    spark         check security of spark

optional arguments:
  -h, --help      show this help message and exit
```
主要有两个子功能，Hadoop和Spark检测
##Hadoop检测
同样可以使用`-h`查看使用说明
```
python main.py hadoop -h
usage: main.py hadoop [-h] confFolder

positional arguments:
  confFolder  the dir of hadoop configuration files

optional arguments:
  -h, --help  show this help message and exit
```
`confFolder`是放置hadoop配置文件的文件夹，可以是你安装hadoop时候的conf文件夹，如`/usr/local/hadoop/conf/hadoop/`，也可以将需要的文件copy到指定的目录，copy时候文件的名字要和hadoop.json里的一样，比如下面是系统默认配置好的用于检测已知安全选项的文件，使用json格式
```json
{
  "authentication": {
    "core-site": [
      {
        "hadoop.security.authentication": "kerberos",
        "reason": "Suggest to authenticate user by using kerberos!"
      }
    ]
  },
  "authorization": {
    "core-site": [
      {
        "fs.permissions.enabled": "true",
        "reason": "Suggest to enable the permission control for fs!"
      },
      {
        "hadoop.security.authorization": "true",
        "reason": "Suggest to enable authorization for every user!"
      }
    ]
  },
  "acl": {
    "hdfs-site": [
      {
        "dfs.namenode.acls.enabled": "true",
        "reason": "Suggest to enable acl for user!"
      }
    ]
  },
  "encry": {
    "hdfs-site": [
      {
        "dfs.encryption.key.provider.uri": "*",
        "reason": "Suggest to encrypt data!"
      }
    ]
  }
}
```
json中的core-site等字段，就是要检测的文件名字，下一级则是要检测的配置项，它的父级像`encry`意思是检测加密的安全问题。该文件使用者可以自己进行扩展。

以当前默认的系统配置，测试如下:
```
$ python HDP.py hadoop ./hadoop
[Info]: Begining to check security: authentication
[Info]: >> Check file: core-site.xml
[Pass]: Your hadoop.security.authentication setting is safe!
[Info]: Begining to check security: encry
[Info]: >> Check file: hdfs-site.xml
[Warning]: Suggest to encrypt data! Set: dfs.encryption.key.provider.uri=*
[Info]: Begining to check security: authorization
[Info]: >> Check file: core-site.xml
[Warning]: Suggest to enable authorization for every user! Set: hadoop.security.authorization=true
[Info]: Begining to check security: acl
[Info]: >> Check file: hdfs-site.xml
[Warning]: Suggest to enable acl for user! Set: dfs.namenode.acls.enabled=true
```

##Spark检测
和hadoop检测类似，同样指定配置文件的文件夹路径，不同的是，spark默认的配置文件只有一个`spark-defaults.conf`,不要改名复制到特定的目录里。

和hadoop检测类似提供了一个可以配置的需要检测配置项，在根目录的spark文件夹下，名字为`security.ini`，该文件的section名字是要检测的配置项输入什么问题，key-value以空格隔开。默认的配置，列出了必要的安全配置项。

例子：
```
$ python HDP.py spark ./spark/
[Info]: Start to check the security of spark...
[Warning]: Suggest to add option spark.authenticate = true if your spark runs on standalone mode
[Warning]: Suggest to add option spark.authenticate.secret if your spark runs on yarn mode
[Warning]: Suggest to set option spark.ssl.enable = true
[Warning]: Suggest to set option spark.eventlog.enabled = true

```

