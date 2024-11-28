# syntax=docker/dockerfile:1
# 第一阶段：解压
FROM ubuntu:20.04 AS builder

ARG HA_TARBALL=hadoop-3.3.6.tar.gz
ARG JAVA_TARBALL=jdk-8u421-linux-x64.tar.gz

# 设置环境变量
ENV HADOOP_HOME=/app/hadoop
ENV JAVA_HOME=/app/java

# 拷贝jdk8和hadoop
COPY ${JAVA_TARBALL} ${JAVA_HOME}/${JAVA_TARBALL}
COPY ${HA_TARBALL} ${HADOOP_HOME}/${HA_TARBALL}

# 解压
RUN tar -zxf ${JAVA_HOME}/${JAVA_TARBALL} --strip-components 1 -C $JAVA_HOME && \
    tar -zxf ${HADOOP_HOME}/${HA_TARBALL} --strip-components 1 -C $HADOOP_HOME  && \
    rm ${JAVA_HOME}/${JAVA_TARBALL} ${HADOOP_HOME}/${HA_TARBALL}

# 第二阶段：安装
FROM ubuntu:20.04 AS final

# 复制builder中的文件
COPY --from=builder /app /app

# 设置环境变量
ENV HADOOP_HOME=/app/hadoop
ENV JAVA_HOME=/app/java
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# 拷贝hadoop配置文件
COPY ./etc/hadoop/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY ./etc/hadoop/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY ./etc/hadoop/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY ./etc/hadoop/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml

# 安装jdk8和hadoop
RUN ln -s $JAVA_HOME/bin/java /bin/java && \
    echo "worker1\nworker2" > $HADOOP_HOME/etc/hadoop/workers && \
    mkdir /app/hdfs && \
    # 向配置文件写入环境变量
    echo export JAVA_HOME=$JAVA_HOME >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo export HADOOP_MAPRED_HOME=$HADOOP_HOME >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo export HDFS_NAMENODE_USER=root >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo export HDFS_DATANODE_USER=root >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo export HDFS_SECONDARYNAMENODE_USER=root >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo export YARN_RESOURCEMANAGER_USER=root >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo export YARN_NODEMANAGER_USER=root >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    # 安装ssh
    sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ssh && \
    apt-get clean && \
    # ssh免密设置
    echo "/etc/init.d/ssh start" >> ~/.bashrc && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys
    
# NameNode WEB UI服务端口
EXPOSE 9870
# nn文件服务端口
EXPOSE 9000
# dfs.namenode.secondary.http-address
EXPOSE 50090
# dfs.datanode.http.address
EXPOSE 50075
# dfs.datanode.address
EXPOSE 50010

