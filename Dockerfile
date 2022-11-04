FROM 3850639cdf7a
# 1.9.0-cuda10.2-cudnn7-runtime
#维护者
LABEL maintainer='wjw'
RUN apt-get update
COPY requirements.txt .

RUN /bin/bash -c "pip install --upgrade pip -i https://pypi.douban.com/simple"
RUN /bin/bash -c "pip install -r requirements.txt -i https://pypi.douban.com/simple"         
RUN mkdir  Honey
COPY * /Honey

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update -y \
    && apt-get install -y wget gcc g++ \
    && apt-get install -y vim

RUN DEBIAN_FRONTEND=noninteractive apt-get install latexmk -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y texlive-latex-extra -y

# 环境设置 
# EXPOSE 8080 
# ENV JAVA_HOME /usr/local/java/jdk-11.0.6/
# ENV PATH $PATH:$JAVA_HOME/bin
