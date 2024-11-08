FROM python:3.10-slim
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt