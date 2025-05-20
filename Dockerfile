FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5000
ENV MYSQL_HOST=localhost
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=
ENV MYSQL_DATABASE=test_db
ENV USE_DB=true

EXPOSE ${PORT:-5000}

CMD ["python", "app.py"]