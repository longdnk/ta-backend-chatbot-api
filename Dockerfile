FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5005

ENTRYPOINT ["python", "main.py"]