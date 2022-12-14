FROM python

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH = "${PYTHONPATH}:/code/src"

CMD ["python -m room_monitor"]