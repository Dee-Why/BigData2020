FROM python:3.6.11-slim

WORKDIR /app

ADD . /app

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "run_service.py"]