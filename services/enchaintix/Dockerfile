FROM python:3.9.6-slim

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD src /app

WORKDIR /app

CMD ["python", "app.py"]
