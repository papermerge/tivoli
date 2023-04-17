from python:3.10

WORKDIR /code

RUN pip install --upgrade poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY ./tivoli /code/tivoli

CMD ["poetry", "run", "uvicorn", "tivoli.main:app", "--host", "0.0.0.0", "--port", "80"]
