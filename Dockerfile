FROM python:3.10

COPY create_dict.py create_dict.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["./create_dict.py"]
