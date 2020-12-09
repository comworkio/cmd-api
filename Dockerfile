FROM python:3

ENV FLASK_APP=/api.py

COPY ./api.py /

RUN pip3 install flask-rest-api

EXPOSE 8080

CMD ["python -m flask run --host=0.0.0.0"]
