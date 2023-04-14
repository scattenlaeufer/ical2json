FROM python:3.10-slim
WORKDIR /code
ADD ical2json /code/ical2json
COPY poetry.lock pyproject.toml README.md /code/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

EXPOSE 8000/tcp

CMD ["uvicorn", "ical2json.api:app", "--host", "0.0.0.0"]
#CMD ["ls"]
