FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python -u bot.py & python -m uvicorn bot:web_app --host 0.0.0.0 --port 8000"]
