FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .

ADD .env /app

RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

# RUN apt update && apt install curl -y

# 複製專案程式碼
COPY routers ./routers
COPY toolkit ./toolkit
COPY main.py .

RUN rm requirements.txt

EXPOSE 8080

CMD uvicorn main:app --workers 1 --host 0.0.0.0 --port 8080 --timeout-keep-alive 30