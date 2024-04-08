FROM python:3.9-slim-buster
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 4050

ENTRYPOINT ["python", "flask_mod.py"]