FROM ubuntu

WORKDIR /code

COPY . .

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y python3-dev python3-pip

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# TODO: Investigate whether this can be incorporated into requirements.txt. Did an initial
# trial but failed.
RUN pip install --install-option="--force-pi" Adafruit_DHT 

ENV PYTHONPATH = "${PYTHONPATH}:/code/src"

CMD ["python -m dht22_monitor"]