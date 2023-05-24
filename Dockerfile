FROM python:3.10

COPY create_dict.py create_dict.py
COPY requirements.lock requirements.lock

RUN pip install -r requirements.lock

ENTRYPOINT ["./create_dict.py"]
