FROM python:3.11.1

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]