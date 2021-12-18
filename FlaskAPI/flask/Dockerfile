FROM python:3.8

ADD . /www
WORKDIR /www

RUN python -m pip install --upgrade pip 
RUN pip install -r requirements.txt
RUN pip install google-cloud-storage
RUN pip install --upgrade google-cloud-bigquery
RUN pip3 install uwsgi

CMD uwsgi uwsgi.ini