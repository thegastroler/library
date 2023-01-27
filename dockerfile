FROM python:3.9-slim-buster
ENV PYTHONBUFFERED=1
ENV POETRY_VERSION=1.2.2
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false
COPY . /app
WORKDIR /app
RUN poetry install --no-interaction --no-ansi -vvv
EXPOSE 8000