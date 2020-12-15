FROM python:3

ENV FLASK_APP=/api.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080

COPY ./api.py ./manifest.json /

RUN pip3 install flask-restful

EXPOSE 8080

CMD ["python3", "-m", "flask", "run"]
