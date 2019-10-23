FROM python:3.6
WORKDIR /ml_webservice/prediction_engine/
COPY requirements.txt /ml_webservice/prediction_engine/
RUN pip install -r requirements.txt  --index-url https://pypi.org/simple/  --extra-index-url https://pypi.fury.io/datascienceengineer/
COPY prediction_engine /ml_webservice/prediction_engine/
EXPOSE 8080
ENTRYPOINT python3.6 ./app.py
