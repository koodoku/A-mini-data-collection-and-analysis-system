FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование требований и установка py-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_generator.py .

CMD ["python", "data_generator.py"]