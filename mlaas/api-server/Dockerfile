FROM python:3.6
WORKDIR /ml_api
COPY requirements.txt /ml_api
RUN pip install -r requirements.txt  --index-url https://pypi.org/simple/  --extra-index-url https://pypi.fury.io/datascienceengineer/
COPY ./ml_api_service /ml_api
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:app"]