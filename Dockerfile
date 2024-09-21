FROM python:3.11

WORKDIR /code

ENV LINE_API_KEY="qhUkuuhr71IfTAlwiIwpj8Miy9F4C2BRB0fRGiOMyiL"

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /code/
COPY run.sh /code/run.sh

RUN pip install --no-cache-dir --upgrade git+https://github.com/GITSangwoo/mnist.git@0.4/worker

CMD ["sh", "run.sh"]
