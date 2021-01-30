FROM python:3-alpine

ENV K8S_VERSION=1.18.2 \
    YQ_VERSION=v4.2.1 \
    YQ_BINARY=yq_linux_amd64 \
    FLASK_APP=/api.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080 \
    WERKZEUG_RUN_MAIN=true \
    MANIFEST_FILE_PATH=/manifest.json

COPY ./api.py ./manifest.json /

RUN pip3 install flask-restful && \
    apk add --no-cache bash curl jq && \
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/v$K8S_VERSION/bin/linux/amd64/kubectl" && \
    mv ./kubectl /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl && \
    curl -LO "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/${YQ_BINARY}.tar.gz" && \
    tar xvzf ${YQ_BINARY}.tar.gz && \
    mv ${YQ_BINARY} /usr/bin/yq && \ 
    chmod +x /usr/bin/yq && \
    rm -rf ${YQ_BINARY}.tar.gz

EXPOSE 8080

CMD ["python3", "-m", "flask", "run"]
