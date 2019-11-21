FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python","app.py"]