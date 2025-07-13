FROM python:slim

COPY . /app

WORKDIR /app

# Note: Make sure you run apt-get update before installing new components
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libmariadb-dev

RUN pip install -r requirements.txt

EXPOSE 3500

CMD ["uvicorn", "restapi:app", "--host", "0.0.0.0", "--port", "3500"]