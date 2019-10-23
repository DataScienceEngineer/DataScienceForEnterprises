FROM python:3.6
WORKDIR /ml_worker
COPY requirements.txt /ml_worker
RUN pip install -r requirements.txt  --index-url https://pypi.org/simple/  --extra-index-url https://pypi.fury.io/datascienceengineer/
COPY ml_worker_service /ml_worker
ENTRYPOINT celery -A tasks worker --loglevel=info