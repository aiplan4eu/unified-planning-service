FROM python:3.9

WORKDIR /up-service
COPY . /up-service

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -y install graphviz graphviz-dev

RUN pip install -r requirements.txt
RUN pip install jupyter matplotlib pygraphviz

EXPOSE 8061
EXPOSE 8062

CMD ["./start.sh"]