FROM python:3.8

WORKDIR /up-service
COPY . /up-service

RUN pip install -r requirements.txt

EXPOSE 8061

CMD ["python", "run.py", "8061"]