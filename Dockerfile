FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pip==24.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "run.py"]