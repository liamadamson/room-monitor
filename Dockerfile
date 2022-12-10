FROM python:3.11.1-slim-buster

WORKDIR /code

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/bin/bash"]