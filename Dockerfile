FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY service/ ./service/
COPY wsgi.py ./

# Allow OpenShift to run the container as an arbitrary non-root UID (GID 0)
RUN chown -R 1000:0 /app && chmod -R g=u /app

USER 1000

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level=info", "wsgi:app"]
