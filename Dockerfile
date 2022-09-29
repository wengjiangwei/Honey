# python 3.8.8 | torch 1.8.1 | torchvision 0.9.1
FROM fa8e7098ab0f 
RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip

RUN pip install -r /docker/requirement.txt -i https://pypi.douban.com/simple

# -id, Run container in background and print container ID
# docker run --gpus device=0 -p 111:111  -e port=111 -v /home/ldq/output_test:/usr/output_dir  -v /home/ldq/logs_dir:/usr/logs -d jibei:v2.0.10 /$params.release_tag/start_server_jibei.sh
