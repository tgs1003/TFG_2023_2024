FROM python

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

ADD app /usr/app/
RUN python /usr/app/download_model.py

