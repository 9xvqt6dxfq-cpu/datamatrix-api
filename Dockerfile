FROM python:3.12-slim

# Установка Poppler
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        poppler-utils \
        libgl1 \
        libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Рабочая папка
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY app.py .

# Порт
EXPOSE 5000

# Запуск
CMD ["python", "app.py"]