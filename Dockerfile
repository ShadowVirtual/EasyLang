FROM python:3.9-slim

STOPSIGNAL SIGINT

WORKDIR /home/container

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

USER container
ENV USER=container HOME=container

COPY . .

ENTRYPOINT ["/entrypoint.sh"]