FROM 3850639cdf7a
# 1.9.0-cuda10.2-cudnn7-runtime
#维护者
LABEL maintainer='wjw'
# 安装miniconda
WORKDIR workspace
RUN cd ..
RUN chmod 777 workspace -R
RUN mkdir -p /workspace/Honey/
RUN mkdir -p /workspace/Weights/

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update -y \
    && apt-get install -y wget gcc g++ \
    && apt-get install -y vim

RUN DEBIAN_FRONTEND=noninteractive apt-get install latexmk -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y texlive-latex-extra -y

ADD ./Honey/ /workspace/Honey/
ADD ./Weights/ /workspace/Weights/
ADD ./Dataset/ /workspace/Dataset/
ADD ./requirements.txt /workspace/requirements.txt

RUN /bin/bash -c "pip install -r /workspace/requirements.txt -i https://pypi.douban.com/simple"         
# 环境设置 
# EXPOSE 8080 
# ENV JAVA_HOME /usr/local/java/jdk-11.0.6/
# ENV PATH $PATH:$JAVA_HOME/bin
