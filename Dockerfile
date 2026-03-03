FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY README.md README.md
COPY src/ src/
RUN uv sync

COPY create_dict.py create_dict.py
ENTRYPOINT ["uv", "run", "./create_dict.py"]
