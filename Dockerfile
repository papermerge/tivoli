from python:3.10

ENV APP_DIR=/tivoli_app

WORKDIR ${APP_DIR}

RUN pip install --upgrade poetry

RUN python3 -m venv .venv

COPY poetry.lock pyproject.toml ${APP_DIR}
RUN poetry install

COPY ./tivoli ${APP_DIR}/tivoli

CMD ["poetry", "run", "uvicorn", "tivoli.main:app", "--host", "0.0.0.0", "--port", "3000"]
